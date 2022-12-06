from django.shortcuts import render
from core.models import Product
from core.models import ReviewCategory


from .serializers import ProductSerializer
from rest_framework.renderers import JSONRenderer
# Create your views here. 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class StudentApi(APIView):
    
    def get(self,request,pk=None,format=None):
        try:
            id=pk
            if id is not None:
                stu=Product.objects.get(id=id)           
                serializer=ProductSerializer(stu)
                return Response({'data':serializer.data,'status':status.HTTP_200_OK})
            
            stu=Product.objects.all()
            serializer=ProductSerializer(stu,many=True)
            return Response({'data':serializer.data,'status':status.HTTP_200_OK})
        
        except Product.DoesNotExist:
            msg={"msg":"not found"}
            return Response({'msg':msg,'status':status.HTTP_404_NOT_FOUND})
    
    
    @csrf_exempt
    def post(self,request,format=None):
        
        data=None
        if request.data is not None:
            data={
                'name':request.data['name'],
                'category':ReviewCategory.objects.get(name=request.data['category']).id,
                'product_code':request.data.get('product_code','rwewe'),
                'description':request.data['description'],
                'short_description':request.data['short_description'],
                'price':request.data['price'],

            }
            
            print(data)
            serializer=ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'status':status.HTTP_201_CREATED,'msg':'data created'})
            
        return Response({'data':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})
    
    
     
    def put(self,request,pk,format=None):
        try:
            id=pk
            stu=Product.objects.get(pk=id)
        except Product.DoesNotExist:
            msg={"msg":"not found"}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)
            
        serializer=ProductSerializer(stu,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'complete data updated','status':status.HTTP_205_RESET_CONTENT})
        return Response({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})
    
    def patch(self,request,pk,format=None):
        try:
            id=pk
            stu=Product.objects.get(pk=id)
        except Product.DoesNotExist:
            msg={"msg":"not found"}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(stu,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'partial data updated','status':status.HTTP_205_RESET_CONTENT})
        return Response({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})
   
    def delete(self,request,pk,format=None):
        try:
            id=pk
            stu=Product.objects.get(pk=id)
        except Product.DoesNotExist:
            msg={"msg":"not found"}
            return Response(msg,status=status.HTTP_404_NOT_FOUND)
        stu.delete()
        return Response({'msg':'data deleted','status':status.HTTP_204_NO_CONTENT})
