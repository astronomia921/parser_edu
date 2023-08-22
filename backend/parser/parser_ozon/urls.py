from django.urls import path
from .views import ProductListView, ProductDetailView, ScrapeProductView

app_name = 'api'

urlpatterns = [
    path('v1/products/',
         ProductListView.as_view(),
         name='product-list'),
    path('v1/products/<int:pk>/',
         ProductDetailView.as_view(),
         name='product-detail'),
    path('v1/products/scrape/',
         ScrapeProductView.as_view(),
         name='scrape-product'),
]
