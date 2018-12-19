from django.shortcuts import render

from artworks.models import Artwork, ArtworkSubject, Subject
from api.serializers import SubjectSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class ArtViewSet(viewsets.ModelViewSet):
	queryset = Subject.objects.order_by('subject_name')
	serializer_class = SubjectSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		art = self.get_object(pk)
		self.perform_destroy(self, art)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


