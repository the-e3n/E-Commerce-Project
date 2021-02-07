from django.urls import path
from .views import Register, Login, logout, UserDashboard, EditAccount, ChangePassword, AdminDashboard,\
    AdminEditAccount, AdminOrders, UserOrders, OrderDetails, AdminOrderDetails, AdminAllUsers, AdminHome, \
    AdminAddNewUser, admin_delete_userprofile, admin_delete_order

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('dashboard/', UserDashboard.as_view(), name='user_dashboard'),
    path('user/orders/<int:orderid>', OrderDetails.as_view(), name='order_details'),
    path('user/orders/', UserOrders.as_view(), name='user_orders'),
    path('amin/', AdminHome.as_view(), name='admin_home'),
    path('amin/dashboard', AdminDashboard.as_view(), name='admin_dashboard'),
    path('amin/edit/<user_name>', AdminEditAccount.as_view(), name='admin_edit_account'),
    path('amin/edit/', AdminEditAccount.as_view(), name='admin_edit_account'),
    path('amin/user/', AdminAllUsers.as_view(), name='admin_users'),
    path('amin/createuser/', AdminAddNewUser.as_view(), name='admin_createuser'),
    path('amin/deleteuser/<user_name>', admin_delete_userprofile, name='admin_deleteuser'),
    path('amin/deleteorder/<orderid>', admin_delete_order, name='admin_deleteorder'),
    path('amin/orders/', AdminOrders.as_view(), name='admin_orders'),
    path('amin/order/<int:orderid>', AdminOrderDetails.as_view(), name='admin_order_details'),
    path('amin/order/', AdminOrderDetails.as_view(), name='admin_order_details'),
    path('account/edit', EditAccount.as_view(), name='user_profile'),
    path('account/pass', ChangePassword.as_view(), name='user_change_password'),
    path('logout/', logout, name='search'),
    path('logout/', logout, name='logout'),
]
