from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment)
admin.site.register(Review)