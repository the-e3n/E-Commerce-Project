from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cms_admin.models import User
from shop.models import Order
from .helpers import validate_data, validate_pass_uname, is_valid_oldpass, confirm_pass, validate_pass_only,\
    user_total_spend

from .models import Address
from .forms import UserForm, UserAddressForm


# Login Page
class Login(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin_home')

            return redirect('home')
        return render(request, 'users/account_form.html', )

    @staticmethod
    def post(request):
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

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {}
        context['register'] = True
        return render(request, 'users/account_form.html', context=context)

    @staticmethod
    def post(request):
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

    @staticmethod
    def get(request):
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
class UserEditAccount(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['addrs'] = Address.objects.filter(user=request.user)
        print(context['addrs'])
        form = UserForm(instance=request.user)
        context['form'] = form
        return render(request, 'users/user_profile.html', context)

    @staticmethod
    def post(request):
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


class UserEditAddress(View):
    @staticmethod
    def get(request, addrid=None):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['addrid'] = addrid
        if addrid is not None:
            try:
                address = Address.objects.get(id=addrid)
                if address.user == request.user:
                    context['form'] = UserAddressForm(instance=address)
                    return render(request, 'users/user_edit_address.html', context)
                else:
                    messages.error(request, 'You are not at this address')
                    return redirect('user_profile')
            except Address.DoesNotExist:
                messages.error(request, 'Address Not Found with this id')
                return redirect('user_profile')
        else:
            messages.error(request, 'Not a valid address id')
            return redirect('user_profile')

    @staticmethod
    def post(request, addrid=None):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        if addrid is not None:
            try:
                address = Address.objects.get(id=addrid)
                if address.user == request.user:
                    form = UserAddressForm(instance=address, data=request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Address Updated Successfully')
                        return redirect('user_profile')
                    else:
                        messages.error(request, 'Not valid form data')
                    return render(request, 'users/user_edit_address.html', context)
                else:
                    messages.error(request, 'You are not at this address')
                    return redirect('user_profile')
            except Address.DoesNotExist:
                messages.error(request, 'Address Not Found with this id')
                return redirect('user_profile')
        else:
            messages.error(request, 'Not a valid address id')
            return redirect('user_profile')


class UserCreateAddress(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        form = UserAddressForm()
        context['form'] = form
        return render(request, 'users/user_create_address.html', context)


    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address saved Successfully')
        else:
            messages.error(request, 'Invalid Form')
        return redirect('user_profile')


def user_delete_addr(request, addrid=None):
    if not request.user.is_authenticated:
        messages.error(request, 'Login Required !')
        return redirect('home')
    context = {}
    if addrid is not None:
        try:
            address = Address.objects.get(id=addrid)
            if address.user == request.user:
                address.delete()
                messages.success(request, 'Address Deleted Succesfully')
                return redirect('user_profile')
            else:
                messages.error(request, 'You are not at this address')
                return redirect('user_profile')
        except Address.DoesNotExist:
            messages.error(request, 'Address Not Found with this id')
            return redirect('user_profile')
    else:
        messages.error(request, 'Not a valid address id')
        return redirect('user_profile')


class UserOrders(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        context['orders'] = request.user.order_set.all()
        return render(request, 'users/user_orders.html', context=context)


class UserOrderDetails(View):

    @staticmethod
    def get(request, orderid=None):
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




# Allow the user to change the user password, After Validating
class ChangePassword(View):

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        return redirect('profile')

    @staticmethod
    def post(request):
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


def error404(request, exception):
    return render(request, 'error404.html')

# Logout Function
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    request.session.flush()
    messages.success(request, 'Logged Out Successfully')
    return redirect('login')


