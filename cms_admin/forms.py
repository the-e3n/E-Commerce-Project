from django import forms
from shop.models import Order, Product, User


class AdminUserChangeForm(forms.ModelForm):
    """
    Form to change a given instance of a given user with supplied post data
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_staff', 'is_admin', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'mx-3'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'mx-3'}),
        }


class AdminAddUserForm(forms.ModelForm):
    """
    Form to add a new user via admin panel
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'is_staff', 'is_admin', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'mx-3'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'mx-3'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),

        }


class AdminNewProductForm(forms.ModelForm):
    """
    Form to add a new Product via admin panel
    """
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AdminEditProductForm(forms.ModelForm):
    """
    Form to Edit a new Product via admin panel
    """
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AdminOrderDetailsForm(forms.ModelForm):
    """
    Form to change given instance of a Order
    """
    class Meta:
        model = Order
        user_set = User.objects.filter(is_admin=False)
        product_set = Product.objects.all()
        fields = ['product', 'customer', 'status']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'mx-3'})
        }
