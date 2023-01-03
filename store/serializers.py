from urllib import request
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import *
from rest_framework.utils import model_meta
# from rest_framework_

class CustomerHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'products-crud-detail'
    # queryset = Review.objects.all()

    # def get_url(self, obj, view_name, request, format):
    #     # print(f'----{obj.pk}----')
    #     if hasattr(obj, 'pk') and obj.pk in (None, ''):
    #         print('-----no attribute-----')
    #         return None
    #     url_kwargs = {
    #         # 'product_pk': getattr(obj, 'product_pk'),
    #         'pk': getattr(obj, 'pk')
    #     }
    #     return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'product_id': view_kwargs['product_pk'],
           'id': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class ImageSerializer(serializers.ModelSerializer):
    image1 = serializers.CharField()
    image2 = serializers.CharField()
    image3 = serializers.CharField()
    image4 = serializers.CharField()
    image5 = serializers.CharField()
    class Meta:
        model = Images
        fields = ['image1','image2','image3','image4','image5']
        # depth = 1

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate1','rate2','rate3','rate4','rate5']


class Sub_CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Sub_Category
        fields = '__all__'
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    # sub_category = Sub_CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['title','image','sub_category']
        depth = 1
class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.StringRelatedField(many=False,read_only=True)
    # images = serializers.HyperlinkedIdentityField(many=False, view_name='products-crud-detail', read_only=True)
    # images_set = serializers.PrimaryKeyRelatedField(many=False, queryset=Images)
    # reviews = serializers.HyperlinkedRelatedField(
    #                             required=False,
    #                             # queryset=Review,
    #                             # many=True,
    #                             view_name='products-crud-detail',
    #                             read_only=True,
    #                             # lookup_field='id'
    #                             )
    reviews = serializers.SerializerMethodField(read_only=True)
    bookmarked = serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(many=False)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     for key, value in data.items():
    #         try:
    #             if not value:
    #                 data[key] = "null"
    #         except KeyError:
    #             pass
    #     return data


    def get_reviews(self, obj):
        view_name = 'review-crud-list'
        request = self.context.get('request')
        try:
            if hasattr(obj, 'pk'):
                return request.build_absolute_uri(reverse(view_name, kwargs={'products_pk':obj.pk}))
            else:
                return
        except:
            return

    def get_bookmarked(self,obj):
        try:
            user = self.context.get('request').user
            is_authenticated = user.is_authenticated
            if is_authenticated:
                # print(obj.bookmarked_set.filter(user=user))
                if obj.bookmarked_set.filter(user=user):
                    print('True')
                    return True
                else:
                    print('False')
                    return False
            else:
                return False
        except AttributeError:
            return False

        # print('/'*10,obj,'*'*10)
        
    class Meta:
        """
        title = models.CharField(max_length=50)
        vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
        price = models.FloatField()
        discount_price = models.FloatField(blank=True,null=True)
        description = models.CharField(max_length=150)

        """
        model = Product
        fields =  ['pk','title','price','discount_price','discount_percent','vendor','rate','images','reviews','category','sub_category','bookmarked']
        depth = 1

    def create(self, validated_data):
        # vendor = validated_data.pop('vendor')
        images = validated_data.pop('images')
        print(validated_data)
        # reviews = validated_data.pop('review')
        validated_data['vendor'] = Vendor.objects.get(id=1)
        product = Product.objects.create(**validated_data)
        image_instance = Images.objects.create(product=product,**images)
        rating = Rating.objects.create(product=product)

        return product

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
    
