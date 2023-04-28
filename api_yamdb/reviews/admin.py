from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'genre', 'category', 
                    'author')
    search_fields = ('name', 'description')
    list_filter = ('year', 'name', 'genre', 'category')
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Title, TitleAdmin)
