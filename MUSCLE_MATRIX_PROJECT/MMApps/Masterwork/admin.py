from django.contrib import admin
from django.contrib.auth.models import User,Group

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

"""
By adding admin.site.unregister(User) and admin.site.unregister(Group) in your Django admin.py file, you are removing the User and Group
models from the Django admin interface.
"""


