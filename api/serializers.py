from rest_framework import serializers
from rest_framework.authtoken.models import Token
from myapp.models import User, Tasks


class SignInSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["token", ]

    def get_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0].key
class TaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = "__all__"
    

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = ["id", "headline", "body", "assigned_at", "deadline","is_active"]


class TaskSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
