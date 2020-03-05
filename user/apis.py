"""API file fro User Module"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from slp_admin import models
from . import serializers


class QRCodeApi(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """API ViewSet for QR Scan and QR Scanned Listing"""
    serializer_class = serializers.QRCodeSerializer
    queryset = models.ScannedQRCode.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        status_header = {
            "status_code": 200,
            "status": "success",
            "message": "QR Code Scanned.",
            "data": serializer.data
        }
        return Response(status_header)
