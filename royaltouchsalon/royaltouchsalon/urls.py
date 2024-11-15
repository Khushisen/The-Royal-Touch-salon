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
    path("signup/",views.signup_view, name="signup"),
    path("login/",views.login_view, name="login"),
    path("logout/",views.logout_view, name="logout"),
    path("add-to-cart/<int:product_id>",views.add_to_cart,name="add_to_cart"),
    path("buy-now/<int:product_id>",views.buy_now,name="buy_now"),
    path("view-cart/",views.view_cart,name="view_cart"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
