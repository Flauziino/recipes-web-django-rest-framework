from . import models


from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_published', 'author',
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'author',
    list_filter = 'category', 'author', 'is_published',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
    autocomplete_fields = 'tags',


admin.site.register(
    models.Category, CategoryAdmin
)
