
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from store.serializers import CustomerSerializer , ProductSerializer, OrderSerializer, OrderItemSerializer
from store.models import Customer, Product, Order , OrderItem
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


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        order = get_object_or_404(Order, customer=customer, complete=False)
        return OrderItem.objects.filter(order=order)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, user=request.user)

        order, _ = Order.objects.get_or_create(customer=customer, complete=False)

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product
        )

        if created:
            order_item.quantity = quantity
        else:
            order_item.quantity += quantity

        order_item.save()
        

        serializer = OrderItemSerializer(
            order_item,
            context={'request': request}
        )
        return Response(serializer.data, status=201)