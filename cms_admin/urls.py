from django.urls import path
from .views import AdminDashboard, AdminEditAccount, AdminOrders, AdminOrderDetails, AdminAllUsers, AdminHome, \
    AdminAddNewUser, AdminProducts, AdminEditProduct, AdminAddNewProduct, admin_delete_product,\
    admin_delete_userprofile, admin_delete_order



urlpatterns = [
    path('', AdminHome.as_view(), name='admin_home'),
    path('dashboard', AdminDashboard.as_view(), name='admin_dashboard'),
    path('edit/<user_name>', AdminEditAccount.as_view(), name='admin_edit_account'),
    path('users/', AdminAllUsers.as_view(), name='admin_users'),
    path('users/edit/', AdminEditAccount.as_view(), name='admin_edit_account'),
    path('users/create/', AdminAddNewUser.as_view(), name='admin_createuser'),
    path('users/delete/<user_name>', admin_delete_userprofile, name='admin_deleteuser'),
    path('products/', AdminProducts.as_view(), name='admin_products'),
    path('products/edit/<int:product_id>', AdminEditProduct.as_view(), name='admin_edit_product'),
    path('products/create', AdminAddNewProduct.as_view(), name='admin_create_product'),
    path('products/delete/<product_id>', admin_delete_product, name='admin_delete_product'),
    path('deleteorder/<orderid>', admin_delete_order, name='admin_deleteorder'),
    path('orders/', AdminOrders.as_view(), name='admin_orders'),
    path('order/<int:orderid>', AdminOrderDetails.as_view(), name='admin_order_details'),
    path('order/', AdminOrderDetails.as_view(), name='admin_order_details'),

    ]