from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MerchantAddSerializer
from rest_framework import status


# Create your API here


@api_view(['POST'])
def add_merchant(request):
    if request.method == 'POST':
        print("hello ad merchant")
        serializer = MerchantAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            # return render(request,'merchant/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

