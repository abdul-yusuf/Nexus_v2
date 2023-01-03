from django.urls import path, include
from .views import CategoriesCRUD, ImagesCRUD, ProductCRUD, ReviewCRUD, SubCategoriesCRUD
# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('products', ProductCRUD, basename='products-crud')
router.register('categories', CategoriesCRUD, basename='categories-view')
router.register('sub-categories', SubCategoriesCRUD, basename='categories-view')
# router.register('images', ImagesCRUD, basename='images-crud')

review_router = NestedDefaultRouter(router,'products',lookup='products')
review_router.register('review', ReviewCRUD, basename='review-crud')

urlpatterns = [
    # path('',include(router.urls), name='router-1'),
    # path('',include((review_router.urls,'review-router'))),
]

urlpatterns+=router.urls
urlpatterns+=review_router.urls
