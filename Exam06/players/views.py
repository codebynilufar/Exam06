from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        country = self.request.query_params.get('country')
        min_rating = self.request.query_params.get('min_rating')
        search = self.request.query_params.get('search')
        if country:
            qs = qs.filter(country__iexact=country)
        if min_rating:
            qs = qs.filter(rating__gte=int(min_rating))
        if search:
            qs = qs.filter(nickname__icontains=search)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
