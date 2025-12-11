
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from store.serializers import CustomerSerializer , ProductSerializer
from store.models import Customer, Product
from django.shortcuts import get_object_or_404



# Create your views here.


class productsListView(viewsets.ModelViewSet):
   queryset = Product.objects.all()
   serializer_class = ProductSerializer
   
   def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]




class CustomerViewSet(viewsets.GenericViewSet):
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        address = request.data.get('address')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name = first_name,
            last_name = last_name
        )
        
        Customer.objects.create(user=user, address=address)
        
        return Response({'message': 'User registered successfully'}, status=201)
    

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
