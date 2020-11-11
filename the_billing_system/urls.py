from django.contrib import admin
from django.urls import path

from billing import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.index),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('add_product/', views.add_product, name='add_product'),
    path('remove_all/', views.remove_all, name='remove_all'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
