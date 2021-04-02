from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ProductDetails, OrderDetail, Checkout, HandlePayment


urlpatterns = [
    path('product/<int:product_id>', ProductDetails.as_view(), name='product_details'),
    path('buy/', OrderDetail.as_view(), name='payment_details'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('checkout/payment-status/', csrf_exempt(HandlePayment.as_view()), name='payment-handle'),
]
