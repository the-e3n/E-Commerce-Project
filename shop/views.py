from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, PaymentDetails, Order
from django.views import View
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from .paytm import checksum
import os

from django.contrib import sessions
# Create your views here.


mid = "dTsKxA83677813579578"
key = "qpzGkE8gjzSyRT1v"
website = "WEBSTAGING"
client_id = "ONLINE_BIT"
try:
    callback_url = os.environ['CALLBACK_URL']
except KeyError:
    callback_url = 'http://localhost:8000/shop/checkout/payment-status/'

class Home(View):

    def get(self, request):
        if request.user.is_anonymous or request.user.is_authenticated:
            context = {}
            context['user'] = request.user
            context['products'] = Product.objects.all()
            paginator = Paginator(context['products'], 9)
            try:
                page_number = request.GET.get('page')
                context['page_obj'] = paginator.get_page(page_number)
            except EmptyPage:
                context['page_obj'] = paginator.get_page(1)
            return render(request, 'index.html', context=context)
        elif request.user.is_admin:
            redirect('admin_home')

    def post(self, request):
        pass


class ProductDetails(View):
    @staticmethod
    def get(request, product_id):
        context = {}
        try:
            context['product'] = Product.objects.get(id=product_id)
            request.session['product_id'] = product_id
        except Product.DoesNotExist:
            messages.error(request, 'Invalid Product ID')
            return redirect('home')
        return render(request, 'shop/product-page.html', context)


class OrderDetail(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context ={}
        return render(request, 'shop/payment_details.html', context)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            messages.error(request, 'Login Required !')
            return redirect('home')
        context = {}
        try:
            product = Product.objects.get(id=request.session['product_id'])
            order = Order.objects.create(customer=request.user, product=product)
            order.save()
            payment = PaymentDetails(
                customer=request.user,
                amount=product.price,
                product=product,
                address=request.POST['address'],
                order=order
            )
            payment.save()
            request.session['payment_id'] = payment.id
        except Product.DoesNotExist:
            messages.error(request, 'Invalid Product ID')
            return redirect('home')
        return redirect('checkout')


class Checkout(View):

    @staticmethod
    def get(request):
        context={}
        payment = PaymentDetails.objects.get(id=request.session['payment_id'])
        context['payment'] = payment

        # Sending Params for Payment Processing
        params = {
            "MID": mid,
            "ORDER_ID": str(request.session['payment_id']),
            "CUST_ID": str(payment.customer.id),
            "TXN_AMOUNT": str(payment.amount),
            "CHANNEL_ID": "WEB",
            "WEBSITE": "WEBSTAGING",
            'CALLBACK_URL': callback_url,
        }
        params['CHECKSUMHASH'] = (checksum.generate_checksum(param_dict=params, merchant_key=key))
        context['params'] = params
        return render(request, 'shop/checkout.html', context)


class HandlePayment(View):

    @staticmethod
    def post(request):
        context = {}
        response = request.POST
        if response['STATUS'] == 'TXN_SUCCESS':
            messages.success(request, f'Your Transaction with Transaction ID {response["TXNID"]} is successfull')
            payment = PaymentDetails.objects.get(id=request.POST['ORDERID'])
            payment.status = 'done'
            payment.order.status = True
            payment.order.save()
            payment.save()
            response = {
                'Order ID': response['ORDERID'],
                'Transaction ID': response['TXNID'],
                'Transaction Amount': response['TXNAMOUNT'],
                'Transaction Date': response['TXNDATE'],
                'Transaction Status': 'Successful',
                'Bank Transaction ID': response['BANKTXNID'],
            }
        elif response['STATUS'] == 'TXN_FAILURE':
            messages.error(request, f'Your Transaction failed because "{response["RESPMSG"]}"')
            response = {
                'Order ID': response['ORDERID'],
                'Transaction ID': response['TXNID'],
                'Transaction Amount': response['TXNAMOUNT'],
                'Transaction Date': response['TXNDATE'],
                'Transaction Status': 'Failed',
            }
        context['response'] = response
        return render(request, 'shop/payment-handle.html', context)

