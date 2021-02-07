from django import forms
from shop.models import Order, Product, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password', 'is_active', 'is_admin', 'is_staff',
                  'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserForm(forms.ModelForm):
    """
    Form for new user creation
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


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
