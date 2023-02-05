from django.shortcuts import render
from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .serializers import CategorySerializer, ImageSerializer, ProductSerializer, RatingSerializer, ReviewSerializer, Sub_CategorySerializer
from .models import Category, Images, Product, Rating, Review, Sub_Category
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema 
from rest_framework import status, filters
from custom_permissions import VendorCrudPermission
# Create your views here.

class ProductCRUD(viewsets.ModelViewSet):
    search_fields = ['title','description','category__title','sub_category__title']
    filter_backends = (filters.SearchFilter,)#filter
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,VendorCrudPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_authenticated:
            if self.request.user.is_vendor and hasattr(self.request.user, 'vendor'):
                self.perform_create(serializer)
            else:
                # return Response(s'User need to be a Vendor to create product', status=status.HTTP_401_UNAUTHORIZED)
                return Response('User need to be a Vendor to create product')
        else:
            return Response('serializer.data', status=status.HTTP_401_UNAUTHORIZED)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor.name)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ImagesCRUD(viewsets.ViewSet):
    # queryset = Images.objects.all()
    serializer_class = ImageSerializer


    def list(self, request, products_pk=None):
        queryset = Images.objects.filter(product=products_pk)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, products_pk=None):
        queryset = Images.objects.filter(product=products_pk)
        client = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(client)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=ImageSerializer, query_serializer=ImageSerializer)
    def create(self, request, *args, **kwargs):
        print(kwargs)
        request.data['product'] = kwargs['products_pk']
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_queryset(self):
    #     print(self.request.method)
    #     return Images.objects.filter(id=self.kwargs['pk'])

class ReviewCRUD(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Review.objects.filter(product=kwargs['products_pk'])
        # print(queryset)
        # client = get_object_or_404(queryset)
        # serializer = ImageSerializer(client)
        # return Response(serializer.data)

        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, pk=None, products_pk=None):
        queryset = Review.objects.filter(product=products_pk)
        client = get_object_or_404(queryset, pk=pk)
        serializer = ReviewSerializer(client)
        return Response(serializer.data)

class CategoriesCRUD(viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        """_summary_
        
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        # queryset = Category.objects.all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj_queryset = self.get_object()
        print(obj_queryset)
        queryset = Product.objects.filter(category=obj_queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class SubCategoriesCRUD(viewsets.GenericViewSet):
    queryset = Sub_Category.objects.all()
    serializer_class = Sub_CategorySerializer
    
    def list(self, request, *args, **kwargs):
        # queryset = Category.objects.all()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        obj_queryset = self.get_object()
        print(obj_queryset)
        queryset = Product.objects.filter(sub_category=obj_queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)