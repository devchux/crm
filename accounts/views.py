from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import authenticated_user, allowed_user, admin_only, admin_customer

# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }

    return render(request, 'accounts/dashboard.html', context)

@authenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration successful, you can now login in as {username}')
            return redirect('login')
    return render(request, 'accounts/register.html', {'form':form})

@authenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_roles=["customer"])
def user(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@admin_customer
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@admin_customer
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    user = customer.user 
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'accounts/delete_customer.html', {'customer': customer })

@login_required(login_url='login')
def createOrder(request, pk):
    CreateOrderSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = CreateOrderSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = CreateOrderSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Order was successfully created')
            return redirect(f'/customer/{pk}/')
    return render(request, 'accounts/create_order.html', {'formset': formset})

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accounts/update_order.html', {'form': form})

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete_order.html', {'order': order})

@login_required(login_url='login')
@allowed_user(allowed_roles=["customer"])
def accounts_settings(request):
    user = request.user.customer
    form = UserProfileForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'{user.name} was updated successfully')
            return redirect('settings')
    context = {'form':form}
    return render(request, 'accounts/settings.html', context)