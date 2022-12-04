from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from core.models import Payment
from .views import OrderCRUD, OrderItemCRUD, OrderedItemCreate, PaymentCRUD, AddressCRUD, PaymentVerify

router = DefaultRouter()
router.register('order',OrderCRUD,basename='order-crud')
router.register('payment',PaymentCRUD,basename='payments-crud')
router.register('address',AddressCRUD,basename='address-crud')
# router.register('ordered-item/<int:item_pk>', OrderedItemCreate)

item_router = NestedDefaultRouter(router, 'order', lookup='order')
item_router.register('item', OrderItemCRUD, basename='order-item-crud')

urlpatterns = [
    path('ordered-item/<int:item_pk>/', OrderedItemCreate, name='ordered-item-create'),
    path('verify/payment/<str:payment_ref>/', PaymentVerify, name='verify-payment')
]

urlpatterns+=router.urls
urlpatterns+=item_router.urls
