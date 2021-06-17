from django.contrib import admin

# Register your models here.
from testoath2.models import CustomUser, Role, Scope

admin.site.register((CustomUser,Role,Scope))
