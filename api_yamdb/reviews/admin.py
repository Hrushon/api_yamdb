from django.contrib import admin

from .models import Category, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'genre')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle)
admin.site.register(Review, ReviewAdmin)
