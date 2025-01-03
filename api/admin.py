from django.contrib import admin
from .models import Slide, Deck

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('deck_id', 'title', 'relevant_product', 'date_created', 'date_modified')
    search_fields = ('title', 'description', 'relevant_product')
    readonly_fields = ('deck_id', 'date_created', 'date_modified')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('slide_id', 'file_name', 'slide_num', 'date_uploaded')
    list_filter = ('deck',)
    search_fields = ('file_name', 'slide_num')
    readonly_fields = ('slide_id', 'date_uploaded') 