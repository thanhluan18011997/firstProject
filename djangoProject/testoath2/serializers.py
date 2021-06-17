from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class Userserializer(ModelSerializer):
    class Meta:
        model=User
        fields = ('username', 'email', "first_name", "last_name")

