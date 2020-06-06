from django.shortcuts import render
from .models import Video
from .serializers import VideoSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from groups.models import InfGroup

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request):
        serializer = VideoSerializer(data=request.data)
        infgroup = InfGroup.objects.get(name=request.data['group'])
        #import pdb;pdb.set_trace()
        if serializer.is_valid():
            serializer.save(group=infgroup)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, partial=True):
        instance = self.get_object()
        serializer = VideoSerializer(instance, data=request.data)
        infgroup = InfGroup.objects.get(name=request.data['group'])
        if serializer.is_valid():
            serializer.save(group=infgroup)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)