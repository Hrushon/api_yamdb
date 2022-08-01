from django.contrib import admin

from .models import Categories, Genres, Titles, GenresTitle, Review


class CategoriesAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')

class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'get_genres')


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(GenresTitle)
admin.site.register(Review, ReviewAdmin)
