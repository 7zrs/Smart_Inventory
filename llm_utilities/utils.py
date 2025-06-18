import json
from django.core.exceptions import ValidationError
import google.generativeai as genai
from django.conf import settings
import requests

def send_to_llm(user_input):
    """
    Sends the user input to Gemini AI and returns the structured response.
    Handles ambiguity, invalid inputs, and ensures consistent JSON output.
    """
    MAIN_PROMPT = """
    Analyze this prompt: '{user_input}' and determine the user's intention. Use the following guidelines:

    1. **For Search**:  
    - If the user is looking for information, interpret it as a `GET` request.  
    - Example: "Find products with low stock" → Make a `GET` request to `/api/products/?stock_level__lt=10`.  
    - Support filters like `name`, `unit`, or `stock_level`.

    2. **For Add**:  
    - If the user wants to add a new item, interpret it as a `POST` request.  
    - Example: "Add a new product named Laptop with unit pieces" → Make a `POST` request to `/api/products/` with the payload:  
        ```json
        {{
        "name": "Laptop",
        "unit": "pieces"
        }}
        ```

    3. **For Update**:  
    - If the user wants to modify an existing item, interpret it as a `PUT` or `PATCH` request.  
    - Example: "Change the unit of Laptop to kilograms" → Make a `PUT` request to `/api/products/{{id}}/` with the payload:  
        ```json
        {{
        "unit": "kilograms"
        }}
        ```

    4. **For Delete**:  
    - If the user wants to remove an item, interpret it as a `DELETE` request.  
    - Example: "Remove the product named Laptop" → Make a `DELETE` request to `/api/products/{{id}}/`.

    5. **For Show**:  
    - If the user wants to view data, interpret it as a `GET` request.  
    - Example: "Show all products" → Fetch data from `/api/products/`.  
    - Support filters like `name`, `unit`, or `stock_level`.

    6. **Schema Details**:  
    - Here’s what you need to know about the schemas:  
        - **Product Schema**:  
        ```json
        {{
            "id": "integer",  // Auto-generated unique identifier
            "name": "string",  // Name of the product
            "unit": "string",  // Unit of measurement (e.g., pieces, kilograms)
            "notes": "string",  // Optional notes about the product
            "purchased_amount": "integer",  // Total purchased amount (calculated field)
            "sold_amount": "integer",  // Total sold amount (calculated field)
            "stock_level": "integer"  // Current stock level (calculated field: purchased_amount - sold_amount)
        }}
        ```  
        - **Purchase Schema**:  
        ```json
        {{
            "id": "integer",  // Auto-generated unique identifier
            "date": "date",  // Date of purchase
            "supplier": "string",  // Optional supplier name
            "product": "integer (foreign key)",  // ID of the associated product
            "amount": "integer",  // Quantity purchased
            "notes": "string"  // Optional purchase-specific notes
        }}
        ```  
        - **Sale Schema**:  
        ```json
        {{
            "id": "integer",  // Auto-generated unique identifier
            "date": "date",  // Date of sale
            "customer": "string",  // Optional customer name
            "product": "integer (foreign key)",  // ID of the associated product
            "amount": "integer",  // Quantity sold
            "notes": "string"  // Optional sale-specific notes
        }}
        ```

    7. **Multiple Tasks**:  
    - If the user input implies multiple tasks, return a list of actions.  
    - Example: "Add a product named Laptop with unit pieces and update its notes to 'High priority'" → Return:  
        ```json
        [
        {{
            "intent": "add",
            "api_action": "POST /api/products/",
            "payload": {{"name": "Laptop", "unit": "pieces"}},
            "confirmation_message": "You are about to add a new product named Laptop with unit pieces. Do you want to proceed?"
        }},
        {{
            "intent": "update",
            "api_action": "PUT /api/products/{{id}}/",
            "payload": {{"notes": "High priority"}},
            "confirmation_message": "You are about to update the notes of Laptop to 'High priority'. Do you want to proceed?"
        }}
        ]
        ```

    8. **Confirmation for Changes**:  
    - If the action modifies data (e.g., add, update, delete), include a confirmation message.  
    - Example: "You are about to add a new product named Laptop with unit pieces. Do you want to proceed?"  
    - Wait for a "Yes" or "No" response before executing the action.

    9. **Ambiguity Handling**:  
    - If the input is unclear or incomplete, respond with: "I’m not sure what you mean. Could you clarify?"

    10. **Response Structure**:  
        - Always return the response in the following JSON format:  
        ```json
        [
            {{
            "intent": "add",  // Possible values: "search", "add", "update", "delete", "show"
            "api_action": "POST /api/products/",  // The corresponding API action
            "payload": {{
                "name": "Laptop",
                "unit": "pieces"
            }},
            "confirmation_message": "You are about to add a new product named Laptop with unit pieces. Do you want to proceed?"
            }}
        ]
        ```

    Return the interpreted intent, the corresponding API action, and any necessary details for execution.
    """
    # Format the prompt with the user input
    prompt = MAIN_PROMPT.format(user_input=user_input)

    # Configure the Gemini API
    genai.configure(api_key=settings.GEMINAI_API_KEY)

    # Load the correct Gemini model
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    try:
        # Generate a response from the LLM
        response = model.generate_content(prompt)

        # Extract the raw LLM output
        llm_output = response.text

        # Log the raw LLM response for debugging purposes
        print("Raw LLM Output:", llm_output)

        # Parse the LLM output into a structured JSON format
        try:
            structured_response = json.loads(llm_output)

            # Check if the response contains an error (e.g., ambiguity handling)
            if isinstance(structured_response, dict) and "error" in structured_response:
                raise ValidationError(structured_response["error"])

            # Ensure the response is always a list (even for single tasks)
            if not isinstance(structured_response, list):
                structured_response = [structured_response]

            return structured_response

        except json.JSONDecodeError:
            # Handle cases where the LLM response is not valid JSON
            raise ValidationError("I’m not sure what you mean. Could you clarify?")

    except Exception as e:
        # Catch any unexpected errors and provide a meaningful message
        raise ValidationError(f"An error occurred while processing your request: {str(e)}")
    

def parse_and_store_tasks(llm_response):
    """
    Parses the LLM response and stores tasks in a list for execution.
    """
    tasks = []

    # Iterate through each task in the LLM response
    for task in llm_response:
        intent = task.get("intent")
        api_action = task.get("api_action")
        payload = task.get("payload", {})
        confirmation_message = task.get("confirmation_message")

        # Validate required fields
        if not intent or not api_action:
            raise ValueError("Invalid task format: Missing 'intent' or 'api_action'.")

        # Store the task details
        tasks.append({
            "intent": intent,
            "api_action": api_action,
            "payload": payload,
            "confirmation_message": confirmation_message
        })

    return tasks

def confirm_and_execute_tasks(tasks):
    """
    Executes the API requests for the given tasks.
    """
    for task in tasks:
        api_action = task["api_action"]
        payload = task["payload"]

        # Execute the API request
        execute_api_request(api_action, payload)
        print(f"Executed: {api_action} with payload {payload}")

def execute_api_request(api_action, payload):
    """
    Executes the API request based on the provided action and payload.
    """
    method, endpoint = api_action.split(" ", 1)  # Split into HTTP method and endpoint
    base_url = "http://127.0.0.1:8000/api/"  # Replace with your actual API base URL

    try:
        if method == "GET":
            response = requests.get(base_url + endpoint, params=payload)
        elif method == "POST":
            response = requests.post(base_url + endpoint, json=payload)
        elif method in ["PUT", "PATCH"]:
            response = requests.put(base_url + endpoint, json=payload)
        elif method == "DELETE":
            response = requests.delete(base_url + endpoint)

        # Check for errors in the API response
        if response.status_code not in [200, 201, 204]:
            raise Exception(f"API request failed: {response.text}")

    except Exception as e:
        raise Exception(f"Error executing API request: {str(e)}")
    
# Main Function to Orchestrate the Workflow
def process_user_input(user_input):
    """
    Processes the user input by sending it to the LLM, parsing tasks,
    and returning the tasks for confirmation.
    """
    try:
        #Send the user input to the LLM
        llm_response = send_to_llm(user_input)

        # Parse and store the tasks from the LLM response
        tasks = parse_and_store_tasks(llm_response)

        # Return the parsed tasks for confirmation in the frontend
        return tasks

    except ValidationError as e:
        # Handle validation errors (e.g., ambiguous input or invalid JSON)
        print(f"Validation Error: {str(e)}")
        return []

    except ValueError as e:
        # Handle value errors (e.g., missing required fields in tasks)
        print(f"Value Error: {str(e)}")
        return []

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {str(e)}")
        return []