from django.contrib import admin

from .models import Categories, Genres, Titles, GenresTitle


class CategoriesAdmin(admin.ModelAdmin):
    pass


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'get_genres')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(GenresTitle)
