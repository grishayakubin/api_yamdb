from django.contrib import admin

from .models import Categories, Genres, Titles


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'genre')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')


admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Titles, TitlesAdmin)
