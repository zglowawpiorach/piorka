"""
REST API views for products and Stripe checkout.
"""

import logging
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from home.models import Product, ProductStatus
from home.api.serializers import ProductSerializer, CheckoutRequestSerializer
from home.stripe_sync import StripeSync

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Product model.

    - Lookup by slug (not id)
    - Default: only ACTIVE products
    - Query param ?status=sold returns sold products
    - Query param ?status=all returns all products
    """
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filter queryset based on status query parameter.

        Returns:
            - ACTIVE products by default
            - SOLD products if ?status=sold
            - All products if ?status=all
        """
        queryset = Product.objects.prefetch_related('images__image')
        status_filter = self.request.query_params.get('status', 'active')

        if status_filter == 'sold':
            return queryset.filter(status=ProductStatus.SOLD)
        elif status_filter == 'all':
            return queryset.all()
        else:  # default to active
            return queryset.filter(status=ProductStatus.ACTIVE)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_checkout(request):
    """
    Create a Stripe Checkout Session for a product.

    POST /api/v1/checkout/

    Request body:
    {
        "product_id": 123,
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/shop",
        "customer_email": "customer@example.com"  // optional
    }

    Response:
    {
        "checkout_url": "https://checkout.stripe.com/...",
        "session_id": "cs_..."
    }

    Errors:
    - 400: Invalid request data
    - 404: Product not found or not buyable
    """
    serializer = CheckoutRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid request', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    product_id = serializer.validated_data['product_id']
    success_url = serializer.validated_data['success_url']
    cancel_url = serializer.validated_data['cancel_url']
    customer_email = serializer.validated_data.get('customer_email')

    # Get product
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if product is buyable
    if not product.is_buyable:
        return Response(
            {'error': 'Product is not available for purchase'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Create checkout session
    result = StripeSync.create_checkout_session(
        product=product,
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
    )

    if result['success']:
        return Response({
            'checkout_url': result['checkout_url'],
            'session_id': result.get('session_id'),
        }, status=status.HTTP_200_OK)
    else:
        logger.error(f"Checkout creation failed: {result.get('error')}")
        return Response(
            {'error': 'Failed to create checkout session', 'details': result.get('error')},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
