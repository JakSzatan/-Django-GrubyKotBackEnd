from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ApointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Apointment
        fields = '__all__'