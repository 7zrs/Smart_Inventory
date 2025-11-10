from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token


User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_user_role(request):
    """Endpoint for Streamlit to check if user is admin"""
    return Response(
        {"is_admin": request.user.is_staff, "username": request.user.username}
    )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_user(request):
    """Create a new user (admin only)"""
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)

    User.objects.create_user(username=username, password=password)
    return Response({"status": "success"}, status=201)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def delete_user(request):
    """Delete a user (admin only)"""
    username = request.data.get("username")

    if not username:
        return Response({"error": "Username required"}, status=400)

    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({"status": "success"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_users(request):
    """Endpoint to get list of all users (for admin)"""
    users = User.objects.all().values_list("username", flat=True)
    return Response(list(users))


@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf(request):
    """Get CSRF token"""
    return JsonResponse({"csrftoken": get_token(request)})


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    """Authenticate a user and log them in."""
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login successful"})
        else:
            return JsonResponse(
                {"status": "error", "message": "Invalid credentials"}, status=400
            )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def user_logout(request):
    """Log out the current user."""
    logout(request)
    return JsonResponse({"status": "success", "message": "Logout successful"})
