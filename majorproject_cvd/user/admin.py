from django.contrib import admin
from .models import UserRegistrationModel, UserTextDataModel

# Register your models here.
admin.site.register(UserRegistrationModel)
admin.site.register(UserTextDataModel)
