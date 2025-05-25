from django.urls import path
from .views import ProcessUserInputView

urlpatterns = [
    path('process-input/', ProcessUserInputView.as_view(), name='process_user_input'),
]