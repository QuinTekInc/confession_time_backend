

from rest_framework import serializers
from .models import User, Confession, SavedUser, Reports, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
    pass


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        pass
    pass


class ConfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Confession
        fields = '__all__'
    pass

class SavedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedUser
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
