from rest_framework import serializers
from slp_admin import models


class QRCodeSerializer(serializers.ModelSerializer):
    """Serializer for QR Code create and list data"""
    class Meta:
        model = models.ScannedQRCode
        fields = ('user', 'merchant', 'product')
