from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
# from django_countries.fields import CountryField

# Create your models here.

class OrderItem(models.Model):
    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * (self.product.price-self.product.discount_price)

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    @property
    def is_payed(self):
        try:
            return self.order_set.all()[0].payment.is_payed
        except: 
            return False
    # @property
    # def order_id
    # @property
    # def ordered(self):
    #     if self.order_set.ordered:
    #         return True
    #     return False


class Order(models.Model):
    ref_code = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE,
                             )
    products = models.ManyToManyField(OrderItem, 
                                    limit_choices_to={'user':user.primary_key}
                                    )
    start_date = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField('Payment', 
                                    on_delete=models.SET_NULL, 
                                    blank=True, 
                                    null=True
                                    )
    coupon = models.ForeignKey(
        'store.Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    #order related booleans
    ordered_date = models.DateTimeField(null=True, blank=True)
    order_place = models.BooleanField(default=False)
    order_confirmed = models.BooleanField(default=False)
    ready_for_delivery = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    # address = 

    @property
    def address(self):
        return self.user.address_set.values()
    


    def __str__(self):
        return self.user.email


    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return round(total,2)
    
    # def on_delivered(self):
    # @property
    # def address(self):
    #     # return 
    #     # print(dir(self.user))
    #     return self.user.address_set
    # @property
    # def if_ordered(self):
    #     if self.ordered:
    #         Order.objects.create(user=self.user)
    #         return True
    #     return
    @property
    def option(self):
        return self.payment.option
    total = property(get_total)

PAYMENT_OPTION = (
    ('O', 'Online'),
    ('D', 'On Delivery'),
)

class Payment(models.Model):
    ref_id = models.CharField(max_length=50, null=True, unique=True)
    user = models.ForeignKey('authentication.User',
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(null=True)
    option = models.CharField(choices=PAYMENT_OPTION, max_length=1, null=True, blank=True)
    authorization = models.CharField(max_length=60, null=True)
    is_payed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.email

    def check_payment_status(self):

        from paystackapi.paystack import Paystack
        from paystackapi.transaction import Transaction
        try:
            response = Transaction.verify(reference=self.ref_id)
        except (TimeoutError, ConnectionError) as e:
            print(e)
        print(response)
        
        if response['status']==True:
            # instance = Payment.objects.get(ref_id=self.ref_id)
            self.is_payed = True
            self.save()
            return True
        else:
            return

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=25, default='Nigeria')#CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Viewed(models.Model):
    user = models.ForeignKey('authentication.User',
                            on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField('store.Product')
    times = models.PositiveSmallIntegerField()

class BookMarked(models.Model):
    user = models.ForeignKey('authentication.User',
                            on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField('store.Product')

# @post_save(Order, sender=settings.AUTH_USER_MODEL)
# def signal_receiver(sender,instance=None,created=None, **kwargs):
#     print(sender,kwargs)
