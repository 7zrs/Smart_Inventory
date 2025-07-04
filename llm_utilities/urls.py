from django.urls import path
from .views import ProcessUserInputView, ExecuteTasksView

urlpatterns = [
    path('api/process-input/', ProcessUserInputView.as_view(), name='process-user-input'),
    path('api/execute-tasks/', ExecuteTasksView.as_view(), name='execute-tasks'),
]