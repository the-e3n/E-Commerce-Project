from django.shortcuts import render,redirect
from django.views import View
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from shop.models import Product, Order
from .helpers import validate_data, validate_pass_uname, is_valid_oldpass, confirm_pass, validate_pass_only, user_total_spend, admin_total_orders

from .forms import UserForm, AdminUserChangeForm, AdminOrderDetailsForm, AdminAddUserForm
# Create your views here.


# Index View



# Login Page
class Login(View):


    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin_home')

            return redirect('home')
        return render(request, 'users/account_form.html', )

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {}
        user = auth.authenticate(request, username=request.POST['uname'].lower(), password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged In')
        else:
            messages.error(request, 'Incorrect Username/Password')
        return redirect(to='login')


# View to render Account sign in/signup Page
class Register(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {}
        context['register'] = True
        return render(request, 'users/account_form.html', context=context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {}
        context['register'] = True
        try:
            if validate_data(request):
                if validate_pass_uname(request):
                    if User.objects.get(email=request.POST['email']):
                        messages.error(request, 'Email  Already in Use')
                    if User.objects.get(username=request.POST['uname']):
                        messages.error(request, 'Username Already Taken')
                else:
                    messages.error(request, 'Please Ensure That Username >= 4 and Password >= 6')
            else:
                messages.error(request, 'Please Enter Valid Details')
        except User.DoesNotExist:
            if request.POST['pass1'] == request.POST['pass2']:
                user = User.objects.create_user(email=request.POST['email'],
                                                password=request.POST['pass2'],
                                                username=request.POST['uname'].lower(),
                                                first_name=request.POST['first_name'].capitalize(),
                                                last_name=request.POST['last_name'],
                                                )
                user.save()
                messages.success(request, 'Registration Successful ! , You Can Login Now')
                return redirect('login')
            else:
                messages.error(request, 'Passwords don\'t Match')
                return render(request, 'users/account_form.html', context=context)
        return render(request, 'users/account_form.html', context=context)


# List all orders of a user. If user is admin redirect to admin dashboard
class UserDashboard(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        else:
            context = {}
            orders = request.user.order_set.all()
            context['total_spend'] = user_total_spend(orders)
            context['orders'] = orders

            return render(request, 'users/user_dashboard.html', context=context)


# Allow the user to edit ones profile
class EditAccount(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        form = UserForm(instance=request.user)
        context['form'] = form
        return render(request, 'users/user_profile.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        user = request.user
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid():
                form.save()
        else:
            messages.error(request, 'Invalid Details')
        context['form'] = form
        return render(request, 'users/user_profile.html', context)


class UserOrders(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['orders'] = request.user.order_set.all()
        return render(request, 'users/user_orders.html', context=context)


class OrderDetails(View):

    def get(self, request, orderid=None):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        if orderid is not None:
            try:
                order = request.user.order_set.get(id=orderid)
                context['order'] = order
            except Order.DoesNotExist:
                messages.error(request, 'Specified order Not Found')
                return redirect('user_orders')
        return render(request, 'users/user_order_details.html', context=context)


# Admin Dashboard For Listing All User On front Page.
# Only Allow Admin Users To View This Page
class AdminDashboard(View):

    def get(self, request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        context = {}
        users = User.objects.filter(is_admin=False)
        context['users'] = users
        context['total_orders'] = admin_total_orders(users)
        return render(request, 'admin/admin_dashboard.html', context=context)


class AdminAddNewUser(View):

    def get(self, request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('login')
        context = {}
        form = AdminAddUserForm()
        context['form'] = form
        return render(request, 'admin/admin_addnewuser.html', context)

    def post(self, request):
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

    def get(self, request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        return redirect('admin_dashboard')


class AdminAllUsers(View):

    def get(self, request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'You Seems To Enter The Wrong Place')
            return redirect('home')
        context = {}
        users = User.objects.filter(is_admin=False)
        context['users'] = users
        return render(request, 'admin/admin_users.html', context=context)

# Allow The Admin To Edit Only The User account
class AdminEditAccount(View):

    def get(self, request, user_name=None):
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
            else:
                user = User.objects.get(username=user_name)
                orders = user.order_set.all()
        except User.DoesNotExist:
            if user_name is not None:
                messages.error(request, 'Invalid User Name')
                return redirect('admin_edit_account')
        form = AdminUserChangeForm(instance=user)
        context['form'] = form
        context['orders'] = orders
        return render(request, 'admin/admin_userprofile.html', context)

    def post(self, request, user_name):
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
        return render(request, 'admin/admin_userprofile.html', context)


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


# List All Orders to admin
class AdminOrders(View):

    def get(self, request):
        if not request.user.is_authenticated and request.user.is_admin:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['orders'] = Order.objects.all()
        return render(request, 'admin/admin_orders.html', context=context)

    def post(self, request):
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

    def get(self, request, orderid=None):
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

    def post(self, request, orderid):
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


# Allow the user to change the user password, After Validating
class ChangePassword(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        return redirect('profile')

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('profile')
        context = {}

        if is_valid_oldpass(request):
            if confirm_pass(request):
                if validate_pass_only(request):
                    user = request.user
                    user.set_password(request.POST['pass2'])
                    user.save()
                    print(user)
                    messages.success(request, 'Passwords changed successfully')
                    return redirect('profile')
                else:
                    messages.error(request, 'Please Ensure That Your New Password is >= 6 and only Contains A-Z,a-z,0-9 and @_&%$')
                    return redirect('profile')
            else:
                messages.error(request, 'Passwords dont match')
                return redirect('profile')
        else:
            messages.error(request, 'Incorrect Old Password')
            return redirect('profile')


# Logout Function
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    request.session.flush()
    messages.success(request, 'Logged Out Successfully')
    return redirect('login')


