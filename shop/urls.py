from django.urls import path
from .views import Home, ProductDetails


urlpatterns = [
    path('product/<int:product_id>', ProductDetails.as_view(), name='product_details'),
]
