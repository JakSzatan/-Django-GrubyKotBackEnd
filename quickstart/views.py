import json

from django.contrib.auth.models import User, Group
from django.core import serializers
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_get_username_from_payload
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.views import verify_jwt_token

from quickstart.models import Apointment
from quickstart import models
from rest_framework import viewsets, status
from rest_framework import permissions
from quickstart.serializers import UserSerializer, GroupSerializer,ApointmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows persons to be viewed or edited.
    """
    queryset = models.Apointment.objects.all()
    serializer_class = ApointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def Register(request):
    if request.method == "POST":
        data=json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data["first_name"],
            last_name=data["last_name"])
        user.save()
    if User.objects.get(username=data['username']):
       return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def GetTattoo(request):
    if request.method == "GET":
        tattoo=User.objects.filter(groups__exact=2).values("first_name", "id")
        post_list = list(tattoo)
        return JsonResponse(post_list,safe=False)

@api_view(['POST'])
def GetApointments(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tattoo=Apointment.objects.filter(tattoo_artist=data["artist"]).values("dateStart","dateEnd","type")
        post_list = list(tattoo)
        return JsonResponse(post_list,safe=False)

@api_view(['GET'])
def GetYourData(request):
    if request.method == "GET":
        payload = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
        user=jwt_get_username_from_payload(payload)
        clinett=User.objects.get(username=user)
        List1=Apointment.objects.filter(tattoo_artist=clinett).values("dateStart","dateEnd","type")
        List2 = Apointment.objects.filter(client=clinett).values("dateStart", "dateEnd", "type")
        post_list = list(List2)+list(List1)
        return JsonResponse(post_list,safe=False)

def GetYou(request):
    if request.method == "GET":
        payload = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
        user=jwt_get_username_from_payload(payload)
        clinet=User.objects.filter(username=user).values("first_name","last_name")
        return JsonResponse(list(clinet),safe=False)

# def ChangeUserSomething(request):
#     if request.method == "POST":
#         payload = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
#         username = jwt_get_username_from_payload(payload)
#         user = User.objects.get(username=username)
#         user.username = newusername
#         user.save()

@api_view(['POST'])
def RegisterApointment(request):
    if request.method == "POST":
        data=json.loads(request.body)
        payload = jwt_decode_handler(request.META.get('HTTP_AUTHORIZATION'))
        user=jwt_get_username_from_payload(payload)
        clinet=User.objects.get(username=user)
        apointment = Apointment.objects.create(
        tattoo_artist=User.objects.get(pk=data["artist"]),
        client = clinet,
        dateStart = data["dateStart"],
        dateEnd =data["dateEnd"] ,
        type = data["type"]
        ) 
        apointment.save()
    if Apointment.objects.last() == apointment:
       return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

