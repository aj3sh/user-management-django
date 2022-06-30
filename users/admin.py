from django.contrib import admin

from .models import User

# registering custom User model to Django admin
admin.site.register(User)