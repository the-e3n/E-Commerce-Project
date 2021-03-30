# Helpers For Login Systems
# Import
from cms_admin.models import User

# Constants
VALID_PASSWORD_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@%&_'


def check_user_login(user):
    """
    check user login
    :param user:
    :return:
    """
    print(user)
    return not user.is_authenticated


def validate_data(request):
    """
    Validate If All the form data sent is available
    :param request:
    :return:
    """
    if request.POST['email'] and request.POST['pass1'] and request.POST['pass2'] and request.POST['first_name'] \
            and request.POST['uname'] and request.POST['last_name']:
        return True
    else:
        return False


def validate_pass_uname(request):
    """
    Checks if the username and password meet the length requirement
    :param request:
    :return:
    """
    if len(request.POST['pass2']) >= 6 and len(request.POST['uname']) >= 4:
        return True
    else:
        return False


def validate_pass_only(request):
    """
    Check If the password contains valid chars and valid length
    :param request:
    :return:
    """
    password = request.POST["pass2"]
    if len(password) >= 6:
        score = 0
        for i in password:
            if i in VALID_PASSWORD_CHARS:
                score += 1
        if score == len(password):
            return True
    return False



def is_valid_oldpass(request):
    """
    Check if the current logged in user current password is correct
    :param request:
    :return:
    """
    if request.user.check_password(request.POST['oldpass']):
        return True
    else:
        return False


def confirm_pass(request):
    """
    Checks if both supplied password are same
    :param request:
    :return:
    """
    if request.POST['pass1'] == request.POST['pass2']:
        return True
    else:
        return False

def username_exist(request):
    """
    Check if a given username already exist in database
    :param request:
    :return:
    """
    try:
        User.objects.get(username=request.POST['username'].lower())
    except User.DoesNotExist:
        return False
    return True


def user_total_spend(iterable):
    """
    Calculate the total spend
    :param iterable:
    :return:
    """
    total = 0
    for order in iterable:
        total += order.product.price

    return total


def admin_total_orders(users):
    total = 0
    for user in users:
        total += len(user.order_set.all())
    return total