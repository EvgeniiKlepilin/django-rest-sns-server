from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from socialnetwork.likes.models import Like
from socialnetwork.likes.serializers import LikeSerializer, LikeAggregateSerializer
from datetime import datetime
from django.utils import timezone
from socialnetwork.likes.utils import daterange
from django.db.models import Count

class LikeList(generics.GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        likes = self.get_queryset()

        date_from_param = request.query_params.get('date_from', None)
        date_to_param = request.query_params.get('date_to', None)
        by_day_param = request.query_params.get('by_day', None)

        date_from = None
        date_to = None

        tz_date_from = None
        tz_date_to = None

        if date_from_param:
            date_from = datetime.strptime(date_from_param, '%Y-%m-%d')
            tz_date_from = timezone.make_aware(date_from)
        if date_to_param:
            date_to = datetime.strptime(date_to_param, '%Y-%m-%d')
            tz_date_to = timezone.make_aware(date_to)

        if tz_date_from and tz_date_to:
            likes = self.get_queryset().filter(created__range=(date_from, date_to))
        elif tz_date_from and tz_date_to is None:
            likes = self.get_queryset().filter(created__range=(date_from, timezone.now()))
        elif tz_date_from is None and tz_date_to:
            likes = self.get_queryset().filter(created__date=tz_date_to)

        if by_day_param:
            likes = likes.extra(select={'date': 'date(created)'}).values('date').annotate(Count('id'))

        page = self.paginate_queryset(likes)

        if page is not None:
            serializer = LikeAggregateSerializer(page, many=True) if by_day_param else self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)