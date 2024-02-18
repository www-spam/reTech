from django.contrib import admin
from .models import User
from .models import Post

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'user_password')

admin.site.register(User, UserAdmin)



admin.site.register(Post)