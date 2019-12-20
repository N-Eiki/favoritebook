from django.contrib import admin
from .models import RecommendedBook
from .models import comment
# Register your models here.
admin.site.register(RecommendedBook)
admin.site.register(comment)
