from django.urls import path
from .views import ProductDetectionView

urlpatterns = [
    path('detect/', ProductDetectionView.as_view(), name='product-detection'),
]