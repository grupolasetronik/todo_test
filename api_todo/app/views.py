from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from app.serializers import TodoSerializer
from app.models import Todo
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class TodoListAndCreate(APIView):
    

    @swagger_auto_schema(operation_description="Listar os todos.",responses={200: TodoSerializer(many=True),400:"Bad Request"})
    def get(self,request):
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo,many=True)
        return Response(serializer.data)


    @swagger_auto_schema(operation_description="Criar novo Todo",request_body=TodoSerializer,responses={201: TodoSerializer(many=True),400:"Bad Request"})
    def post(self, request,format=None):
        serializer = TodoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TodoDetailChangeAndDelete(APIView):
    
    def get_object(self, pk):
	    try:
		    return Todo.objects.get(pk = pk)
	    except:
		    raise NotFound()
    @swagger_auto_schema(operation_description="Ver todo específico",responses={200:TodoSerializer})
    def get(self,request,pk):
	    todo = self.get_object(pk)		
	    serializer = TodoSerializer(todo)
	    return Response(serializer.data)
    @swagger_auto_schema(operation_description="Editar todo",request_body=TodoSerializer,responses={200:TodoSerializer})
    def put(self, request, pk):
	    todo = self.get_object(pk)
	    serializer = TodoSerializer(todo, data = request.data)
	    if serializer.is_valid():
	        serializer.save()
        	return Response(serializer.data)
	    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(operation_description="Deletar Todo",responses={204:'No Content'})
    def delete(self,request,pk):
	    todo = self.get_object(pk)
	    todo.delete()
	    return Response(status.HTTP_204_NO_CONTENT)