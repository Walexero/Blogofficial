from django.contrib import admin
from .models import Post,Shop,Comment,Cart,Cartitem

# Register your models here.
admin.site.register(Post)
admin.site.register(Shop)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Cartitem)

