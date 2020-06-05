from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student
from tests.models import Test
from groups.models import Group
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        group = Group.objects.get(owner=request.user, name=request.data['group'])
        if serializer.is_valid():
            serializer.save(owner=request.user, group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        instance = self.get_object()
        group = Group.objects.get(owner=request.user, name=request.data['group'])
        serializer = StudentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, group=group)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, list=True, methods=['GET'])
    def getmystd(self, request):
        mystd = Student.objects.filter(owner=request.user)
        serializer = StudentSerializer(mystd, many=True)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])#학년 그룹 이름
    def findstd(self, request):
        student = Student.objects.filter(owner=request.user)
        if request.data['group'] is not "":
            group = Group.objects.get(name=request.data['group'])
            student = student.filter(group=group)
        if request.data['grade'] is not "":
            student = student.filter(grade=request.data['grade'])
        if request.data['name'] is not "":
            student = student.filter(name=request.data['name'])
        #import pdb; pdb.set_trace()
        
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, list=True, methods=['POST'])
    def getteststd(self, request):
        test = Test.objects.get(id=request.data['test_id'])
        serializer = StudentSerializer(test.student, many=True)
        return Response(serializer.data)
    