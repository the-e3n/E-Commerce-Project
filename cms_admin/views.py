from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from cms_app.helpers import admin_total_orders
from .models import User
from .forms import AdminUserChangeForm, AdminOrderDetailsForm, AdminAddUserForm, AdminNewProductForm, \
    AdminEditProductForm
from shop.models import Product, Order


# Admin Dashboard For Listing All User On front Page.
# Only Allow Admin Users To View This Page
class AdminDashboard(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        context = {}
        users = User.objects.filter(is_admin=False).order_by('-date_joined')
        context['users'] = users
        context['total_orders'] = admin_total_orders(users)
        return render(request, 'admin/admin_dashboard.html', context=context)


class AdminAddNewUser(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        form = AdminAddUserForm()
        context['form'] = form
        return render(request, 'admin/admin_addnewuser.html', context)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        try:
            user = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            context = {}
            form = AdminAddUserForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Added New User')
            else:
                messages.error(request, 'Wrong details')
            return redirect('admin_createuser')


class AdminHome(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        return redirect('admin_dashboard')


class AdminAllUsers(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        context = {}
        users = User.objects.filter(is_admin=False).order_by('-date_joined')
        context['users'] = users
        return render(request, 'admin/admin_users.html', context=context)


# Allow The Admin To Edit Only The User account
class AdminEditAccount(View):

    @staticmethod
    def get(request, user_name=None):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        try:
            if user_name is None:
                user = request.user
                orders = user.order_set.all()
                if user.is_admin and user.is_authenticated:
                    context['self_profile'] = True
                    addrs = None
            else:
                user = User.objects.get(username=user_name)
                orders = user.order_set.all()
                addrs = user.address_set.all()
        except User.DoesNotExist:
            messages.error(request, f'Invalid User Name{user_name}')
            return redirect('admin_edit_account')
        form = AdminUserChangeForm(instance=user)
        context['form'] = form
        context['orders'] = orders
        context['addrs'] = addrs
        return render(request, 'admin/admin_userprofile.html', context)

    @staticmethod
    def post(request, user_name):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        try:
            user = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            pass
        context = {}
        form = AdminUserChangeForm(instance=user, data=request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated User Settings')
        else:
            messages.error(request, 'Invalid Details')
        context['form'] = form
        return render(request, 'admin/admin_products.html', context)


def admin_delete_userprofile(request, user_name):
    if not request.user.is_authenticated and request.user.is_admin:
        messages.error(request, 'Login Required !')
        return redirect('login')
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        messages.error(request, 'Invalid Username')
        return redirect('admin_users')
    else:
        user.delete()
        messages.success(request, f'{user.username} deleted successfully ')
        return redirect('admin_users')


class AdminProducts(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        context = {}
        products = Product.objects.all()
        context['products'] = products
        return render(request, 'admin/admin_products.html', context=context)


class AdminAddNewProduct(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        form = AdminNewProductForm()
        context['form'] = form
        return render(request, 'admin/admin_new_product.html', context)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        form = AdminNewProductForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added New Product Successfully')
        else:
            messages.error(request, 'Invalid Form Data')
        return redirect('admin_create_product')


class AdminEditProduct(View):

    @staticmethod
    def get(request, product_id=None):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        try:
            if product_id is not None:
                product = Product.objects.get(id=product_id)
            else:
                messages.error(request, 'No Product id found')
                return redirect('admin_products')
        except Product.DoesNotExist:
            messages.error(request, 'Invalid Product Id')
            return redirect('admin_products')
        form = AdminEditProductForm(instance=product)
        context['form'] = form
        context['product_id'] = product_id
        return render(request, 'admin/admin_edit_product.html', context)

    @staticmethod
    def post(request, product_id=None):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, f'No Product found with id {product_id}')
            return redirect('admin_products')
        context = {}
        form = AdminEditProductForm(instance=product, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Product Information')
        else:
            messages.error(request, 'Invalid Product information')
        context['form'] = form
        context['product_id'] = product_id
        return render(request, 'admin/admin_edit_product.html', context)




def admin_delete_product(request, product_id):
    if not request.user.is_authenticated and request.user.is_admin:
        messages.error(request, 'Login Required !')
        return redirect('login')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, f'Invalid Product Id {product_id}')
        return redirect('admin_products')
    else:
        product.delete()
        messages.success(request, f'{product.name} deleted successfully ')
        return redirect('admin_products')


# List All Orders to admin
class AdminOrders(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['orders'] = Order.objects.all()
        return render(request, 'admin/admin_orders.html', context=context)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        try:
            order = Order.objects.get(id=request.POST['orderid'])
            if not order.status:
                order.status = True
                order.save()
                messages.success(request, 'Order marked as Completed')
            else:
                messages.error(request, 'Already Completed')
        except Order.DoesNotExist:
            messages.error(request, 'Specified order Not Found')
            return redirect('admin_orders')
        return redirect('admin_orders')


class AdminOrderDetails(View):

    @staticmethod
    def get(request, orderid=None):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        if orderid is not None:
            try:
                order = Order.objects.get(id=orderid)
                context['orderid'] = orderid
                form = AdminOrderDetailsForm(instance=order)
            except Order.DoesNotExist:
                messages.error(request, 'Specified order Not Found')
                return redirect('admin_orders')
            context['form'] = form
        return render(request, 'admin/admin_order_details.html', context=context)

    @staticmethod
    def post(request, orderid):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        try:
            order = Order.objects.get(id=orderid)
            context['orderid'] = orderid
            form = AdminOrderDetailsForm(instance=order, data=request.POST)
        except Order.DoesNotExist:
            messages.error(request, 'Specified order Not Found')
            return redirect('admin_orders')
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Updated Successfully')
            context['form'] = AdminOrderDetailsForm(instance=order)
        return render(request, 'admin/admin_order_details.html', context=context)


def admin_delete_order(request, orderid):
    if not request.user.is_authenticated and request.user.is_admin:
        messages.error(request, 'Login Required !')
        return redirect('login')
    context = {}
    try:
        order = Order.objects.get(id=orderid)
        order.delete()
        messages.success(request, 'Order Deleted Successfully')
    except Order.DoesNotExist:
        messages.error(request, 'Specified order Not Found')
        return redirect('admin_orders')
    return redirect('admin_orders')
