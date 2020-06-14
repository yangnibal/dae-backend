from django.shortcuts import render
from .models import Test
from students.models import Student
from .serializers import TestSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from students.models import Student

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    
    def create(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        instance = self.get_object()
        serializer = TestSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, list=True, methods=['POST'])
    def addstd(self, request):
        test = Test.objects.get(id=request.data['id'])

    @action(detail=False, list=True, methods=['GET'])
    def getstd(self, request):
        test = Test.objects.get(id=request.data['id'])
        

    @action(detail=False, list=True, methods=['GET'])
    def getmytest(self, request):
        test = Test.objects.filter(owner=request.user)
        serializer = TestSerializer(test, many=True)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])
    def findtest(self, request):
        test = Test.objects.filter(owner=request.user)
        if request.data['grade'] is not "":
            test = test.filter(grade=request.data['grade'])
        if request.data['test_type'] is not "":
            test = test.filter(test_type=request.data['test_type'])
        if request.data['subject'] is not "":
            test = test.filter(subject=request.data['subject'])
        #import pdb; pdb.set_trace()

        serializer = TestSerializer(test, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, list=False, methods=['POST'])
    def deletestd(self, request, pk):
        test = self.get_object(pk)
        student = Student.objects.get(name=request.data['std_name'])
        test.student.remove(student)
        return Response(status=status.HTTP_204_NO_CONTENT)