from django.test import TestCase
from llm_utilities.utils import send_to_llm

class LLMResponseTestCase(TestCase):
    def test_send_to_llm_response(self):
        """
        Test the send_to_llm function to ensure it returns a valid AI response.
        """
        # Define the user input
        user_input = "Add a new product named Laptop with unit pieces"

        try:
            # Call the send_to_llm function
            response = send_to_llm(user_input)

            # Print the response for debugging purposes
            print("AI Response:", response)

            # Assert that the response is not None
            self.assertIsNotNone(response, "send_to_llm returned None")

            # Assert that the response is a list
            self.assertIsInstance(response, list, "send_to_llm did not return a list")

            # Validate the first task in the list
            if response:
                first_task = response[0]
                self.assertIn("intent", first_task)
                self.assertIn("api_action", first_task)
                self.assertIn("payload", first_task)

                # Optionally, validate specific values in the task
                self.assertEqual(first_task["intent"], "add")
                self.assertEqual(first_task["api_action"], "POST /api/products/")
                self.assertEqual(first_task["payload"]["name"], "Laptop")
                self.assertEqual(first_task["payload"]["unit"], "pieces")

        except Exception as e:
            # Fail the test if an exception occurs
            self.fail(f"send_to_llm raised an exception: {e}")