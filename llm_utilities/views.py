from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_to_llm
import requests

class ProcessUserInputView(APIView):
    def post(self, request):
        """
        Processes user input by sending it to the LLM and executing the corresponding API action.
        """
        user_input = request.data.get("input")
        if not user_input:
            return Response({"error": "Input is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Send input to the LLM
            llm_response = send_to_llm(user_input)

            # Extract details from the LLM response
            intent = llm_response.get("intent")
            api_action = llm_response.get("api_action")
            payload = llm_response.get("payload", {})
            confirmation_message = llm_response.get("confirmation_message")

            # If confirmation is required, return the message
            if confirmation_message:
                return Response({
                    "confirmation_required": True,
                    "message": confirmation_message,
                    "api_action": api_action,
                    "payload": payload,
                }, status=status.HTTP_200_OK)

            # Execute the API action
            base_url = "http://127.0.0.1:8000/api/"  # Replace with your actual API base URL
            method = api_action.split(" ")[0].lower()
            endpoint = api_action.split(" ")[1]

            if method == "get":
                response = requests.get(base_url + endpoint, params=payload)
            elif method == "post":
                response = requests.post(base_url + endpoint, json=payload)
            elif method == "put" or method == "patch":
                response = requests.put(base_url + endpoint, json=payload)
            elif method == "delete":
                response = requests.delete(base_url + endpoint)

            # Return the API response
            return Response(response.json(), status=response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)