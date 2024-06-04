from rest_framework import serializers

from apps.activity.models import CampusActivity, CampusActivityRequest


class CampusActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusActivity
        fields = '__all__'


class CampusActivityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusActivityRequest
        fields = '__all__'
