from django.shortcuts import render, redirect
from .models import Product
from django.views import View
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
# Create your views here.


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
        except Product.DoesNotExist:
            messages.error(request, 'Invalid Product ID')
            return redirect('home')
        return render(request, 'shop/product-page.html', context)