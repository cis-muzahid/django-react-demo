from django.contrib import admin
from dummy_data.models import CustomUser, DummyData
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DummyData)
