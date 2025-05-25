from django.test import TestCase
from llm_utilities.utils import send_to_llm

class LLMLogicTestCase(TestCase):
    def test_send_to_llm(self):
        """
        Test the send_to_llm function with a sample user input.
        """
        # Define the user input
        user_input = "Add a new product named Laptop with unit pieces"

        try:
            # Call the send_to_llm function
            response = send_to_llm(user_input)

            # Print the response for debugging purposes
            print("LLM Response:", response)

            # Assert that the response contains the expected keys
            self.assertIn("intent", response)
            self.assertIn("api_action", response)
            self.assertIn("payload", response)

            # Optionally, validate specific values in the response
            self.assertEqual(response["intent"], "add")
            self.assertEqual(response["api_action"], "POST /api/products/")
            self.assertEqual(response["payload"]["name"], "Laptop")
            self.assertEqual(response["payload"]["unit"], "pieces")

        except Exception as e:
            # Fail the test if an exception occurs
            self.fail(f"send_to_llm raised an exception: {e}")