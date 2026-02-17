"""
URL configuration for the products API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.views import ProductViewSet, create_checkout

# Create router for ViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

app_name = 'products_api'

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', create_checkout, name='checkout'),
]
