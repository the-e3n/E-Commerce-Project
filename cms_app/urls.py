from django.urls import path
from .views import (Register, Login, logout, UserDashboard, UserEditAccount, UserOrders, UserOrderDetails,
    ChangePassword, UserEditAddress, user_delete_addr, UserCreateAddress)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('dashboard/', UserDashboard.as_view(), name='user_dashboard'),
    path('orders/<int:orderid>', UserOrderDetails.as_view(), name='order_details'),
    path('orders/', UserOrders.as_view(), name='user_orders'),
    path('account/edit', UserEditAccount.as_view(), name='user_profile'),
    path('address/create', UserCreateAddress.as_view(), name='create_user_address'),
    path('address/edit/<int:addrid>', UserEditAddress.as_view(), name='edit_user_address'),
    path('address/delete/<int:addrid>', user_delete_addr, name='delete_user_address'),
    path('account/pass', ChangePassword.as_view(), name='user_change_password'),
    path('logout/', logout, name='logout'),
    path('logout/', logout, name='search'),
]
