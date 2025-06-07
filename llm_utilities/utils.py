import google.generativeai as genai
import json
from django.conf import settings

def send_to_llm(user_input):
    """
    Sends the user input to Gemini AI and returns the structured response.
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
     {
       "name": "Laptop",
       "unit": "pieces"
     }
     ```

3. **For Update**:  
   - If the user wants to modify an existing item, interpret it as a `PUT` or `PATCH` request.  
   - Example: "Change the unit of Laptop to kilograms" → Make a `PUT` request to `/api/products/{id}/` with the payload:  
     ```json
     {
       "unit": "kilograms"
     }
     ```

4. **For Delete**:  
   - If the user wants to remove an item, interpret it as a `DELETE` request.  
   - Example: "Remove the product named Laptop" → Make a `DELETE` request to `/api/products/{id}/`.

5. **For Show**:  
   - If the user wants to view data, interpret it as a `GET` request.  
   - Example: "Show all products" → Fetch data from `/api/products/`.  
   - Support filters like `name`, `unit`, or `stock_level`.

6. **Schema Details**:  
   - Here’s what you need to know about the schemas:  
     - **Product Schema**:  
       ```json
       {
         "id": "integer",  // Auto-generated unique identifier
         "name": "string",  // Name of the product
         "unit": "string",  // Unit of measurement (e.g., pieces, kilograms)
         "notes": "string",  // Optional notes about the product
         "purchased_amount": "integer",  // Total purchased amount (calculated field)
         "sold_amount": "integer",  // Total sold amount (calculated field)
         "stock_level": "integer"  // Current stock level (calculated field: purchased_amount - sold_amount)
       }
       ```  
     - **Purchase Schema**:  
       ```json
       {
         "id": "integer",  // Auto-generated unique identifier
         "date": "date",  // Date of purchase
         "supplier": "string",  // Optional supplier name
         "product": "integer (foreign key)",  // ID of the associated product
         "amount": "integer",  // Quantity purchased
         "notes": "string"  // Optional purchase-specific notes
       }
       ```  
     - **Sale Schema**:  
       ```json
       {
         "id": "integer",  // Auto-generated unique identifier
         "date": "date",  // Date of sale
         "customer": "string",  // Optional customer name
         "product": "integer (foreign key)",  // ID of the associated product
         "amount": "integer",  // Quantity sold
         "notes": "string"  // Optional sale-specific notes
       }
       ```

7. **Multiple Tasks**:  
   - If the user input implies multiple tasks, return a list of actions.  
   - Example: "Add a product named Laptop with unit pieces and update its notes to 'High priority'" → Return:  
     ```json
     [
       {
         "intent": "add",
         "api_action": "POST /api/products/",
         "payload": {"name": "Laptop", "unit": "pieces"},
         "confirmation_message": "You are about to add a new product named Laptop with unit pieces. Do you want to proceed?"
       },
       {
         "intent": "update",
         "api_action": "PUT /api/products/{id}/",
         "payload": {"notes": "High priority"},
         "confirmation_message": "You are about to update the notes of Laptop to 'High priority'. Do you want to proceed?"
       }
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
        {
          "intent": "add",  // Possible values: "search", "add", "update", "delete", "show"
          "api_action": "POST /api/products/",  // The corresponding API action
          "payload": {
            "name": "Laptop",
            "unit": "pieces"
          },
          "confirmation_message": "You are about to add a new product named Laptop with unit pieces. Do you want to proceed?"
        }
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
    # Generate a response
    response = model.generate_content(prompt)

    # Extract the LLM output
    llm_output = response.text

    # Log the raw LLM response for debugging
    print("Raw LLM Output:", llm_output)

    # Convert the LLM output into a structured format (e.g., JSON)
    try:
        structured_response = json.loads(llm_output)  # Assuming the LLM returns JSON
    except json.JSONDecodeError:
        raise Exception("Gemini AI response is not in valid JSON format.")

    return structured_response