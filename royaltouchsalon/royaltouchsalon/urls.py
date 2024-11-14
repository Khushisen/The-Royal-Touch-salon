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
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
