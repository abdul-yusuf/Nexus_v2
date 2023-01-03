import random
import string

from rest_framework import serializers
from .models import OrderItem, Order, Payment, Address
from store.serializers import ProductSerializer
from rest_framework.utils import model_meta


class Order_setSerializer(serializers.ModelSerializer):
    # products = OrderItemSerializer(many=True, read_only=True)
    # payment = PaymentSerializer(many=False, read_only=True)
    # coupon = CouponSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','ref_code','start_date','ordered_date','payment','coupon','order_place','order_confirmed','ready_for_delivery','being_delivered','delivered','refund_requested','refund_granted','option','address']
        # fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    order_set = Order_setSerializer(many=True, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','user','ordered','product','quantity','is_payed','order_set']
        # depth = 1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(many=False, read_only=True)
    # coupon = CouponSerializer(many=True, read_only=True)
    # address = AddressSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','ref_code','user','products','start_date','ordered_date','payment','coupon','order_place','order_confirmed','ready_for_delivery','being_delivered','delivered','refund_requested','refund_granted','total','address']
        # fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        validated_data['ref_code'] = create_ref_code()
        try:
            coupon = validated_data.pop('coupon')
            products = validated_data.pop('products')
            payment = validated_data.pop('payment')
            user = validated_data.pop('user')
        except:
            pass
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        images = validated_data.pop('images')
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance



def create_ref_code(k=20):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))
