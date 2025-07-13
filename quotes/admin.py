from django.contrib import admin
from .models import Source, Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'source', 'weight', 'views', 'likes', 'dislikes')
    list_editable = ('weight',)
    search_fields = ('text', 'source__name')

    @staticmethod
    def short_text(obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')
