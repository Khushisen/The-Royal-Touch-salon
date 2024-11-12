from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index, name="index"),
    path("contact/",views.contact, name="contact"),
    path("gallery/",views.gallery, name="gallery"),
    path("services/",views.services, name="services"),
    path("about/",views.about, name="about"),
    path("products/",views.products, name="products"),
    path("cart/",views.cart,name='cart'),
    path("checkout/",views.checkout,name = 'checkout'),
    path("payment-success/",views.payment_success,name='payment_success'),
    path("order-confirmation/",views.order_confirmation,name='order_confirmation'),
    path("add-to-cart/<int:product_id>/",views.add_to_cart,name='add_to_cart'),
    path("update-cart/<int:product_id>/",views.update_cart,name='update_cart'),
    path("remove-from-cart/<int:product_id>/",views.remove_from_cart,name='remove_from_cart'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
