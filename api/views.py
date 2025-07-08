from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.contrib.auth import authenticate, get_user_model
from api.serializers import LoginSerializer  # adjust this import path if needed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    if UserProfile.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    # ✅ Use .copy() to make request.data mutable
    data = request.data.copy()

    # ✅ Check if password is present
    if 'password' not in data:
        return Response({'error': 'Password is required'}, status=400)

    # ✅ Hash the password
    data['password'] = make_password(data['password'])

    serializer = UserProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return Response({"error": "User does not exist"}, status=401)

        if check_password(password, user.password):  # ✅ Compare hashed password
            return Response({"message": "Login successful"}, status=200)
        else:
            return Response({"error": "Invalid password"}, status=401)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=205)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_all_profiles(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

@csrf_exempt
def create_profile(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')

        # Check if a profile for this email already exists
        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Profile already exists'}, status=400)

        profile = UserProfile(
            name=data.get('name'),
            email=email,
            age=data.get('age'),
            city=data.get('city'),
            education=data.get('education'),
            profession=data.get('profession'),
            interests=data.get('interests'),
            photo=request.FILES.get('photo')
        )
        profile.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=405)


class ProfileDetailView(APIView):
    def get(self, request, email):
        try:
            profile = UserProfile.objects.get(email=email)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UpdateProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, email):
        try:
            profile = UserProfile.objects.get(email=email)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully"})
            else:
                # 👉 Check if 'photo' field caused the error
                if 'photo' in serializer.errors:
                    return Response(
                        {"error": "Image upload failed. Please re-upload your photo."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
