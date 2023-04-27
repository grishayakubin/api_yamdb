from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'genre')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
