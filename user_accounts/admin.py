from django.contrib import admin

# Register your models here.
from user_accounts.models import *


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name','mobile', 'is_customer', 'is_staff', 'is_superuser',
                    'created_date']
    list_filter = ['email']


admin.site.register(User, UserAdmin)
