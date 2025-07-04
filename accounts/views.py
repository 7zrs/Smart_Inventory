from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token


User = get_user_model()

# Add these endpoints:
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role(request):
    """Endpoint for Streamlit to check if user is admin"""
    return Response({
        "is_admin": request.user.is_staff,  
        "username": request.user.username
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt  # Temporary for testing - remove in production
def create_user(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)
    
    User.objects.create_user(username=username, password=password)
    return Response({"status": "success"}, status=201)

@api_view(['POST'])
@permission_classes([IsAdminUser])
@csrf_exempt  # Temporary for testing - remove in production
def delete_user(request):
    username = request.data.get('username')
    
    if not username:
        return Response({"error": "Username required"}, status=400)
    
    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({"status": "success"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    """Endpoint to get list of all users (for admin)"""
    users = User.objects.all().values_list('username', flat=True)
    return Response(list(users))

@csrf_exempt
def user_login(request):
    """
    Authenticate a user and log them in.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def user_logout(request):
    """
    Log out the current user.
    """
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logout successful'})

def get_csrf(request):
    return JsonResponse({"csrftoken": get_token(request)})