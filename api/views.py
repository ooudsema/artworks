from django.shortcuts import render

from artworks.models import Artwork, ArtworkSubject
from api.serializers import ArtworkSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class ArtViewSet(viewsets.ModelViewSet):
	queryset = Artwork.objects.select_related('ArtworkSubject').order_by('artwork_title')
	serializer_class = ArtworkSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		art = self.get_object(pk)
		self.perform_destroy(self, art)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()


