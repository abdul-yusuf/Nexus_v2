from django.contrib import admin
from .models import *

# Register your models here.
class ImageInline(admin.StackedInline):
    model = Images

class RatingInline(admin.StackedInline):
    model  = Rating
    readonly_fields = ('rate1','rate2','rate3','rate4','rate5')

class ReviewInline(admin.TabularInline):
    model = Review
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'description', 'category', 'sub_category')
    list_filter = ('vendor', 'category', 'sub_category')
    inlines = [
        ImageInline,
        RatingInline,
        ReviewInline
    ]



admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor)
# admin.site.register(Images)
# admin.site.register(Rating)
# admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Sub_Category)
