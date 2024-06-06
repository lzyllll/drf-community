from django.db import transaction
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.activity.models import CampusActivity, CampusActivityRequest
from apps.activity.serializers import CampusActivitySerializer, CampusActivityRequestSerializer


# Create your views here.

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = CampusActivity.objects.all()
    serializer_class = CampusActivitySerializer
    permission_classes = []

    @action(detail=True, methods=['post'])
    def end_activity(self,request,pk=None):
        partial = True
        instance = self.get_object()

        serializer = self.get_serializer(instance, data={'end_date': timezone.now()}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ActivityRequestViewSet(viewsets.ModelViewSet):
    queryset = CampusActivityRequest.objects.all()
    serializer_class = CampusActivityRequestSerializer
    permission_classes = []

    @transaction.atomic()
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        activity_request:CampusActivityRequest = self.get_object()
        # 同意请求，保存
        activity_request.status = CampusActivityRequest.APPROVED
        activity_request.save()
        # 添加到成员
        activity:CampusActivity = activity_request.activity
        user = activity_request.user

        # todo 可能之后会修改为初始化活动的同时会加入请求
        # 额，可能初始化活动，参加者没有请求，所以，如果participants存在，就不添加成员了，只同意请求
        if not activity.participants.filter(id=user.id).exists():
            activity.participants.add(user)

        return Response({'status': 'request approved'}, status=status.HTTP_200_OK)

    # 可以单独设置，但我已经直接通过view.action判断了，就不必了
    # 在action加入选项 permission_classes=[permissions.IsAuthenticated]
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        activity_request: CampusActivityRequest = self.get_object()
        # 拒绝，保存
        activity_request.status = CampusActivityRequest.REJECTED
        activity_request.save()
        return Response({'status': 'request rejected'}, status=status.HTTP_200_OK)
