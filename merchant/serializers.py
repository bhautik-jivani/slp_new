from rest_framework import serializers
from slp_admin.models import Merchant

# Create your serializer here


class MerchantAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['email', 'name', 'phone']

