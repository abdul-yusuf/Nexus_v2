from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.

class UserAdmin(BaseUserAdmin):
    # fields = ('username', 'email', 'phone_no', 'nationality', 'state_of_origin', 'business_state', 'local_govt', 'specialization', 'password')
    list_display = ('username','email','is_superuser','is_vendor')
    list_filter = ('is_superuser', 'is_vendor', 'is_staff' )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name','last_name')}),
        ('Permissions', {'fields': ('is_superuser','is_active', 'is_staff', 'groups', 'user_permissions', 'is_vendor')}),
        ('Vendor Info', {'fields': ()}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    actions = ['make_vendor']

    def make_vendor(self, request, queryset):
        queryset.update(is_vendor=True)
    # readonly_fields = 


admin.site.register(User, UserAdmin)