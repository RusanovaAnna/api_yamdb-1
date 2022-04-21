from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year',
        'description', 'category', 'genre',
    )
    search_fields = ('name',)
    empty_value_display = '-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title',
        'title_id', 'text',
        'author', 'score',
        'pub_date',
    )
    empty_value_display = '-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'review_id', 'text', 'author', 'pub_date',
    )
    empty_value_display = '-'


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
