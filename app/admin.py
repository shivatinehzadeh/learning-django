from django.contrib import admin
from .models import Book,Category,Suggestion,Profile,Reserve
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('name','brand')
    list_filter = ('name',)
    search_fields = ('name','brand')
admin.site.register(Book,PostAdmin)


class CatogaryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
admin.site.register(Category,CatogaryAdmin)

class suggestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
admin.site.register(Suggestion,suggestAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)
admin.site.register(Profile,ProfileAdmin)

class ReserveAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)
admin.site.register(Reserve,ReserveAdmin)


