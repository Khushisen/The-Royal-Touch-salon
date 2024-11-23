from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request,'Passwords do not match!')
            return render(request,'signup.html')
        
        if User.objects.filter(username = username).exists():
            messages.error(request,'Username already exists!')
            return render(request,'signup.html')
        
        user = User.objects.create_user(username = username,password = password1)
        user.save()
        
        login(request,user)
        messages.success(request,'Signup successful! You are now logged in.')
        return redirect('products')
    else:
        return render(request,'signup.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('products')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('products')

def product_list(request):
    products = Product.objects.all()
    return render(request,'products.html',{'products':products})

@login_required
def add_to_cart(request,product_id):
    if not request.user.is_authenticated:
        messages.error(request,'You need to login to add items to the cart.')
        return redirect('login')
    
    product = get_object_or_404(Product, id = product_id)
    cart_item,created = Cart.objects.get_or_create(user = request.user,product=product)
    if created:
        messages.success(request,f'{product.product_name} has been added to your cart.')
    else:
        cart_item.quantity +=1
        cart_item.save()
        messages.info(request,f'Quantity of {product.product_name} has been updated.')
    return redirect('view_cart')

@login_required
def view_cart(request):
    if not request.user.is_authenticated:
        messages.error(request,'You need to login to view your cart.')
        return redirect('login')
    
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request,'view_cart.html',{'cart_items' : cart_items, 'total_amount':total_amount})

def remove_from_cart(request,cart_item_id):
    if not request.user.is_authenticated:
        messages.error(request,'You need to log in to manage your cart.')
        return redirect('login')
    cart_item = get_object_or_404(Cart, id=cart_item_id,user=request.user)
    cart_item.delete()
    messages.success(request,f'{cart_item.product.product_name} has been removed from your cart.')
    return redirect('view_cart')


@login_required
def order_confirmation(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        for item in cart_items:
            Order.objects.create(user=request.user,product=item.product,address=address)
        cart_items.delete()
        return redirect('order_success')
    return render(request,'order_confirmation.html')


@login_required
def order_success(request):
    return render(request,'order_success.html')