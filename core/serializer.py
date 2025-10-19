from rest_framework import serializers
from .models import tasks,message
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class taskserializer(serializers.ModelSerializer):
    class Meta:
        model=tasks
        fields=['title','task_status','description','priority','IS_COMPLETED','is_important','id','due_date']
        read_only_fields = ['is_due','completed_at']

class messageserializer(serializers.ModelSerializer):
    class Meta:
        model=message
        fields=['hedder','content','is_read','timestamp']

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username','password','email']
        extara_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username,
                                        password=password,
                                        **validated_data
                                    )
        return user
