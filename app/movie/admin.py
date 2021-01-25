from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movies,Genre


admin.site.register(Movies)
admin.site.register(Genre)