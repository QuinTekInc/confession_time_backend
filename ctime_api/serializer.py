

from rest_framework import serializers
from confessions.models import *


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



class UserSentConfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSentConfession
        fields = '__all__'

    pass


class ConfessionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfessionReport
        fields = '__all__'



class SavedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedUser
        fields = '__all__'



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
    
    pass


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    pass
