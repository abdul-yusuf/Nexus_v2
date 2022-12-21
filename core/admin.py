from django.contrib import admin
from .models import *
# from 
# Register your models here.

class PaymentInline(admin.StackedInline):
    model = Order

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','user','ordered','is_payed')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ref_id','id','user','amount','option','timestamp','is_payed')
    list_filter = ('user','option','is_payed')
    inlines = [
            PaymentInline
        ]
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_code','id','user','ordered_date','payment','ordered','being_delivered','received','refund_requested')
    actioin = [
        'order_being_delivered',
        'order_received'
    ]
    def order_being_delivered(self, queryset):
        queryset.update(begin_delivered=True)

    def order_received(self, queryset):
        queryset.update(received=True)

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Address)