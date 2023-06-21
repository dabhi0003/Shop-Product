from django.contrib import admin
from .models import User,Category,Product,UserProfile,UserProduct
from django.contrib.admin import ModelAdmin

# @admin.register(UserDetails)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ["password","phone_no", "email", "last_name", "first_name", "username"][::-1]
class UserAdmin(ModelAdmin):
        list_display = ('id', 'email', 'username', 'first_name', 'last_name' ,'phone','acivation_status')
        list_filter = ('is_superuser',)
        fieldsets = [
                (None, {'fields': ('email', 'password',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'username','phone','acivation_status',)}),
                ('Permissions', {'fields': ('is_superuser',)}),
        ]

        add_fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ( 'is_student','phone','acivation_status'),
                }),
        )
        search_fields = ('username',)
        ordering = ('id',)
        filter_horizontal = ()
admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["type", "name"][::-1]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["category", "discription", "price", "name"][::-1]


@admin.register(UserProfile)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ["ifsc", "branch", "account_number", "bank_name", "address", "user"][::-1]


@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ["product", "user"][::-1]
