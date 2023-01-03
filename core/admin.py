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
    list_display = ('ref_code','id','user','ordered_date','payment','order_place','order_confirmed','ready_for_delivery','being_delivered','delivered','refund_requested')
    list_filter = ('order_place','order_confirmed','ready_for_delivery','being_delivered','delivered','refund_requested')
    list_per_page = 10
    actions = [
        'order_being_delivered',
        'order_delivered',
        'order_confirmed',
        'order_ready_for_delivery',
        'refund_granted'
    ]
    def order_being_delivered(self, request, queryset):
        queryset.update(begin_delivered=True)

    def order_delivered(self, request, queryset):
        queryset.update(delivered=True)
    
    def order_confirmed(self, request, queryset):
        queryset.update(order_confirmed=True)
    
    def order_ready_for_delivery(self, request, queryset):
        queryset.update(ready_for_delivery=True)

    def refund_granted(self, request, queryset):
        queryset.update(refund_granted=True)
    
    

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Address)
admin.site.register(BookMarked)
