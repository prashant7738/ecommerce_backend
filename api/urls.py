from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', views.productsListView, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('orderitem', views.OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls))
]
