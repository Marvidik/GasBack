from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404
from .models import LastLogin

# Create your views here.

@api_view(['POST'])
def login(request):
    # Get the user from the request data
    user = get_object_or_404(User, username=request.data['username'])

    # Check if the user's password matches
    if not user.check_password(request.data['password']):
        return Response({"details": "Info Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get the user's token or generate one if it doesn't exist
    token, created = Token.objects.get_or_create(user=user)
    
    # Log the login time for the user in the LastLogin model
    LastLogin.objects.create(worker=user, date=now())

    # Serialize the user data
    serializer = UserSerializer(instance=user)

    # Return the user's data along with the token and login time
    return Response({
        "user": serializer.data,
        "token": token.key,
        "login_time": now().strftime("%Y-%m-%d %H:%M:%S")
    }, status=status.HTTP_200_OK)

#The registration API
@api_view(['POST'])
def register(request):
    #Getting the data from the user 
    serializer=UserSerializer(data=request.data)
    #Checking if the data is valid and storing the information if it is 
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)

        return Response({"token":token.key,"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_last_login(request):
    try:
        # Get all users
        users = User.objects.all()
        
        # Prepare a list to hold user last login data
        user_logins = []

        for user in users:
            try:
                # Get the latest login entry for the user
                last_login = LastLogin.objects.filter(worker=user).latest('date')
                user_logins.append({
                    "username": user.username,
                    "last_login": last_login.date.strftime("%Y-%m-%d %H:%M:%S")
                })
            except LastLogin.DoesNotExist:
                # If no login records exist for this user, add a default message
                user_logins.append({
                    "username": user.username,
                    "last_login": "No login records found"
                })

        return Response(user_logins, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)