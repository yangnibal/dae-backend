from django.shortcuts import render
from .models import Group, InfGroup
from students.models import Student
from .serializers import GroupSerializer, InfGroupSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, list=True, methods=['GET'])
    def getmygroup(self, request):
        group = Group.objects.filter(owner=request.user)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])
    def getstdgroup(self, request):
        student = Student.objects.get(owner=request.user, name=request.data['name'])
        group = Group.objects.get(owner=request.user, student=student)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

class InfGroupViewSet(viewsets.ModelViewSet):
    queryset = InfGroup.objects.all()
    serializer_class = InfGroupSerializer

    def create(self, request):
        serializer = InfGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)