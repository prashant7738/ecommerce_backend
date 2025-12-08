from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', views.productsListView, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls))
]
