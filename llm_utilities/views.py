from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import process_user_input
from .serializers import UserInputSerializer
from .utils import confirm_and_execute_tasks
from .serializers import TaskConfirmationSerializer

class ProcessUserInputView(APIView):
    def post(self, request):
        """
        Accepts user input, processes it, and returns the tasks for confirmation.
        """
        # Validate the incoming data
        serializer = UserInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the user input
        user_input = serializer.validated_data['user_input']

        # Process the user input and get tasks
        tasks = process_user_input(user_input)

        # Return the tasks for confirmation
        return Response(tasks, status=status.HTTP_200_OK)
    

class ExecuteTasksView(APIView):
    def post(self, request):
        """
        Accepts confirmed tasks, executes them, and returns the results.
        """
        # Validate the incoming data
        serializer = TaskConfirmationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the confirmed tasks
        confirmed_tasks = serializer.validated_data['tasks']

        # Execute the tasks
        try:
            confirm_and_execute_tasks(confirmed_tasks)
            return Response({"message": "Tasks executed successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)