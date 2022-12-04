import random
import string

from django.conf import settings
from itertools import product
from django.shortcuts import render, get_object_or_404
from store.models import Product
from .models import Order, OrderItem, Payment, Address
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer, AddressSerializer
from custom_permissions import UserOrderCrudPermission
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from datetime import datetime
from django.db.models.query import QuerySet


from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
# Create your views here.

paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

def create_ref_code(k=20):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))


class OrderCRUD(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, UserOrderCrudPermission]
    def list(self, request):
        # print(request.user)
        queryset = Order.objects.filter(user=request.user, ordered=False)
        client = get_object_or_404(queryset)
        serializer = OrderSerializer(client)
        return Response(serializer.data)

class OrderItemCRUD(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, UserOrderCrudPermission]

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(user=self.request.user)
        return queryset




    def retrieve(self, request, pk=None, order_pk=None):
        queryset = OrderItem.objects.filter(user=request.user)
        client = get_object_or_404(queryset, pk=pk)
        serializer = OrderItemSerializer(client)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        order = Order.objects.get(id=kwargs['order_pk'], user=request.user)
        order_serialized_instance = OrderSerializer(order) 

        return Response(order_serialized_instance.data)    

    def destroy(self, request, *args, **kwargs):
        print(args, kwargs)
        instance = OrderItem.objects.filter(id=kwargs['pk'], user=request.user)
        print(instance)
        order = Order.objects.get(id=kwargs['order_pk'], user=request.user)
        self.perform_destroy(instance)
        order_serialized_instance = OrderSerializer(order) 
        return Response(order_serialized_instance.data)


# class PaymentCRUD(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer


class AddressCRUD(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, UserOrderCrudPermission]

class PaymentCRUD(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # permission_classes = [permissions.IsAuthenticated, UserOrderCrudPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def perform_create(self, serializer):
        print(self.request.user.email, self.request.data)
        email = self.request.user.email
        data = self.request.data
        # amount = int(data['amount'])
        print(data)
        order = Order.objects.get(ref_code=data['ref_id'], ordered=False)
        print(order.total)
        total = int(order.total)*100
        # print(order.products, dir(order.products))

        # try:
        if data['option']=='O':
            response = Transaction.initialize(reference=data['ref_id'],
                                    # authorization_code='authorization_code',
                                    email=email,
                                    amount=total,
                                    channels=['card', 'ussd'])
        else:
            response = {
                'status': True,
                'data': {
                    'authorization_url': '',
                    'access_code': '',
                    'reference': data['ref_id']
                }
            }
        
        print(response)
        
        if response['status']==True:
            authorization_url = response['data']['authorization_url']
            access_code = response['data']['access_code']
            reference = response['data']['reference']
            # return Response(response)
            instance = serializer.save(user=self.request.user,
                            authorization=authorization_url,
                            ref_id=reference,
                            amount=total,
                            option=data['option'])
            order.ordered = True
            for item in order.products.all():
                item.ordered=True
                item.save()
            order.payment = instance
            order.save()
        # elif response['ref_id']==
        else:
            # instance = Payment.objects.get(ref_id=self.request.data['reference'])
            return Response(response)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def OrderedItemCreate(request, item_pk):
    queryset = Product.objects.all()
    item = get_object_or_404(queryset, pk=item_pk)
    ordereditem = OrderItem.objects.get_or_create(product=item,user=request.user,ordered=False)
    ordereditem[0].quantity += 1
    ordereditem[0].save()
    order = Order.objects.get_or_create(user=request.user, ordered=False)
    print(dir(order[0]))
    order[0].ref_code = create_ref_code()
    order[0].products.add(ordereditem[0])
    order[0].save()
    return Response(OrderSerializer(order[0]).data)

@api_view(['POST'])
def PaymentVerify(request, payment_ref):

    response = Transaction.verify(reference=payment_ref)
    print(response)
    
    if response['status']==True:
        instance = Payment.objects.get(ref_id=payment_ref)
        instance.is_payed = True
        instance.save()

    return Response(response)