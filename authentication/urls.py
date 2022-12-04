from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('ordered-item', views.AddItemToCart, basename='ordered-item')
# router.register('order-create', views.OrderCreate, basename='order-cruds')

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='auth-reg'),
  
]

# urlpatterns += router.urls
