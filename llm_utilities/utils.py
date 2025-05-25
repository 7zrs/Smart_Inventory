import google.generativeai as genai
import json
from django.conf import settings

def send_to_llm(user_input):
    """
    Sends the user input to Gemini AI and returns the structured response.
    """
    MAIN_PROMPT = """
    Analyze this prompt: '{user_input}' and determine the user's intention. Use the following guidelines:

    1. **For Search**: Interpret as a GET request.
    2. **For Add**: Interpret as a POST request.
    3. **For Update**: Interpret as a PUT/PATCH request.
    4. **For Delete**: Interpret as a DELETE request.
    5. **For Show**: Interpret as a GET request with optional filters.
    6. Include schema details and confirmation messages as needed.

    Return the interpreted intent, API action, payload, and confirmation message in JSON format.
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