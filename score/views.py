from django.shortcuts import render
from .models import Score, Logo
from tests.models import Test
from tests.serializers import TestSerializer
from students.models import Student
from .serializers import ScoreSerializer, LogoSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .getrank import *

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def create(self, request):
        serializer = ScoreSerializer(data=request.data['data'], many=True)
        #import pdb;pdb.set_trace()
        #test = Test.objects.get(id=request.data['data'][0]['test_id'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        instance = self.get_object()
        serializer = ScoreSerializer(instance, data=request.data)
        test = Test.objects.get(id=request.data['test'])
        student = Student.objects.get(name=request.data['student'], owner=request.user)
        percent = getPercent(request.data['score'], test.average, test.std_dev)
        percent = round(percent, 1)
        rank = getRank(percent, test.cand_num)
        rank = int(round(rank, 0))
        if(rank==0): rank=1
        rating = getRating(percent)
        z = getZ(request.data['score'], test.average, test.std_dev)
        prob_dens = getProbDens(z)
        if serializer.is_valid():
            serializer.save(percent=percent, rank=rank, rating=rating, test=test, student=student, z=z, prob_dens=prob_dens, owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=False, list=True, methods=['POST'])
    def getlist(self, request):
        data = request.data['data']
        test = Test.objects.get(id=data[0]['test'])
        #import pdb; pdb.set_trace()
        for i in range(len(data)):
            serializer = ScoreSerializer(data=data[i])
            student = Student.objects.get(name=data[i]['student'], owner=request.user)
            percent = getPercent(data[i]['score'], test.average, test.std_dev)
            percent = round(percent, 1)
            rank = getRank(percent, test.cand_num)
            rank = int(round(rank, 0))
            if(rank==0): rank=1
            rating = getRating(percent)
            z = getZ(data[i]['score'], test.average, test.std_dev)
            prob_dens = getProbDens(z)
            try:
                score = Score.objects.get(student=student, test=test)

            except Score.DoesNotExist:
                if serializer.is_valid():
                    serializer.save(percent=percent, rank=rank, rating=rating, test=test, student=student, z=z, prob_dens=prob_dens, owner=request.user)
                    test.student.add(student)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, list=True, methods=['GET'])
    def getmyscore(self, request):
        score = Score.objects.filter(owner=request.user)
        serializer = ScoreSerializer(score, many=True)
        return Response(serializer.data)

    @action(detail=False, list=True, methods=['POST'])
    def getstdscore(self, request):
        student = Student.objects.get(id=request.data['id'])
        score = Score.objects.filter(student=student)
        test = Test.objects.filter(student=student)
        serializer = ScoreSerializer(score, many=True)
        testserializer = TestSerializer(test, many=True)
        data = {'score': serializer.data, 'test': testserializer.data}
        return Response(data)

    @action(detail=False, list=True, methods=['POST'])
    def findscore(self, request):
        #import pdb;pdb.set_trace()
        student = Student.objects.get(id=request.data['id'])
        test = Test.objects.filter(student=student)
        if request.data['grade'] is not "":
            test = test.filter(grade=request.data['grade'])
        if request.data['test_type'] is not "":
            test = test.filter(test_type=request.data['test_type'])
        if request.data['subject'] is not "":
            test = test.filter(subject=request.data['subject'])
        testserializer = TestSerializer(test, many=True)
        score = Score.objects.filter(test__in=test, student=student)
        serializer = ScoreSerializer(score, many=True)
        data = {'score': serializer.data, 'test': testserializer.data}
        return Response(data)

    @action(detail=False, list=True, methods=['POST'])
    def gettestscore(self, request):
        test = Test.objects.get(id=request.data['test_id'])
        score = Score.objects.filter(owner=request.user, test=test)
        serializer = ScoreSerializer(score, many=True)
        return Response(serializer.data)

class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

    def create(self, request):
        try:
            logo = Logo.objects.get(owner=request.user)
            logo.delete()
            serializer = LogoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Logo.DoesNotExist:
            serializer = LogoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, list=True, methods=['GET'])
    def getmylogo(self, request):
        try:
            logo = Logo.objects.get(owner=request.user)
            serializer = LogoSerializer(logo)
            return Response(serializer.data)
        except Logo.DoesNotExist:
            return Response("no logo exist")