from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
                  # path('slp_admin/', slp_admin.site.urls),

                  path('merchant/<int:id>', views.merchant, name='merchant'),
                  path('add_merchant', views.add_merchant, name='add_merchant'),
                  path('view_merchant', views.view_merchant, name='view_merchant'),
                  path('delete_merchant/<int:id>', views.delete_merchant, name='delete_merchant'),
                  path('merchant_status', views.merchant_status, name='merchant_status'),
                  path('add_products', views.add_products, name='add_products'),
                  path('products', views.products, name='products'),
                  path('view_products/<int:id>', views.view_products, name='view_products'),
                  path('delete_product/<int:id>', views.delete_product, name='delete_product'),
                  path('edit_product/<int:id>', views.edit_product, name='edit_product'),
                  path('edit_product_tech_file', views.edit_product_tech_file, name='edit_product_tech_file'),
                  path('edit_product_guide_file', views.edit_product_guide_file, name='edit_product_guide_file'),
                  path('edit_product_video_file', views.edit_product_video_file, name='edit_product_video_file'),
                  path('edit_product_safety_file', views.edit_product_safety_file, name='edit_product_safety_file'),
                  path('edit_product_certificate_file', views.edit_product_certificate_file, name='edit_product_certificate_file'),
                  path('dashboard', views.dashboard, name='slpdashboard'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

