from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from app1.forms import ContactForm, CheckoutForm
from django.contrib import messages
from .models import Booking,Product,Order
from django.conf import settings
import datetime
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.contrib.auth.views import LoginView

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

class CustomLoginView(LoginView):
    template_name = 'login.html'

def index(request):
    return render(request,'index.html')

def services(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        message = request.POST.get('message')

        #validation for appointment date
        try:
            appointment_date = datetime.datetime.strptime(appointment_date, '%Y-%m-%d').date()
            appointment_time = datetime.datetime.strptime(appointment_time, '%H:%M').time()

            if appointment_date < datetime.date.today():
                messages.error(request,"Appointment date cannot be in the past!")
                return redirect('services')
            
            #check if time slot is already booked
            if Booking.objects.filter(appointment_date = appointment_date,appointment_time=appointment_time,service=service).exists():
                messages.error(request,"This time slot is not available. Please choose another one")
            else:
                booking = Booking(
                    customer_name=customer_name,
                    email=email,
                    phone = phone,
                    service= service,
                    appointment_date = appointment_date,
                    appointment_time = appointment_time,
                    message=message
                )
                booking.save()

                #send mail notification to the admin
                send_mail(
                    subject="New home service booking",
                    message = f"new booking by {booking.customer_name} for {booking.service} on {booking.appointment_date} at {booking.appointment_time}.\n\nDetails:\n"
                    f"Name: {booking.customer_name}\nEmail: {booking.email}\nPhone: {booking.phone}\nService: {booking.service}\nMessage: {booking.message}",
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                )

                messages.success(request,"Your appointment has been booked successfully!")
                return redirect('services')
        
        except ValueError:
            messages.error(request,"invalid date or time format.")
        
    return render(request,'services.html')
    
def about(request):
    return render(request,'about.html')

def gallery(request):
    return render(request,'gallery.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_mail(
                f'New contact message from {contact.name}',
                contact.message,contact.email,['khushisen9001@gmail.com'],fail_silently=False,
            )
            messages.success(request,'Your message has been sent succesfully!')
            return redirect('contact')
    else:
        form=ContactForm()
    return render(request,'contact.html',{'form':form})


def products(request):
    products = Product.objects.all()
    return render(request,'products.html',{'products':products})

def cart(request):
    cart = request.session.get('cart',{})
    total_price = sum(float(item['price'])* item['quantity'] for item in cart.values())
    return render(request,'cart.html',{'cart': cart, 'total_price' : total_price})

def add_to_cart(request,product_id):
    product = get_object_or_404(Product, id = product_id)
    cart = request.session.get('cart',{})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'name': product.name, 'price': str(product.price), 'quantity': 1}

    request.session['cart'] = cart
    messages.success(request,f"{product.name} has been added to your cart.")
    return redirect('cart')

def update_cart(request,product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity',1))
        cart = request.session.get('cart',{})

        if str(product_id) in cart:
            if quantity > 0:
                cart[str(product_id)]['quantity'] = quantity
                messages.success(request,f"Quantity updated to {quantity}")
            else:
                cart.pop(str(product_id))
                messages.success(request,"Item removed from cart.")

        request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request,product_id):
    cart = request.session.get('cart',{})

    if str(product_id) in cart:
        cart.pop(str(product_id))
        messages.success(request,"Item removed from cart.")
    request.session['cart']=cart
    return redirect('cart')
@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                address = form.cleaned_data['address'],
                postal_code = form.cleaned_data['postal_code'],
                total_price = total_price,
            )

            razorpay_order = razorpay_client.order.create({
                'amount': int(total_price * 100),
                'currency' : 'INR',
                'payment_capture': '1'
            })

            order.razorpay_order_id = razorpay_order['id']
            order.save()

            return render(request,'checkout.html',{
                'form':form,
                'order': order,
                'razorpay_order_id':order.razorpay_order_id,
                'razorpay_key': settings.RAZORPAY_API_KEY,
                'total_price':total_price,
            })
    else:
        form = CheckoutForm()
    return render(request,'checkout.html',{'form':form,'cart':cart,'total_price': total_price})

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        try:
            order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
            order.payment_status = True
            order.save()
            return redirect('checkout')
        except Order.DoesNotExist:
            return redirect('checkout')
    return redirect('checkout')
def order_confirmation(request):
    return render(request,'order_confirmation.html')