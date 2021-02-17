from django.contrib import admin
from .models import Proposition, Tag
# Register your models here.


class PropositionAdmin(admin.ModelAdmin):
    list_filter = ['date_added',
                   'tags',
                   ]
    list_display_links = [
        'title'
    ]
    list_filter = ['date_added',
                   ]
    search_fields = [   
        'tags',
        'title'
    ]
    list_display = [
                    'prop_preview_photo',
                    'title',
                    'date_added',
                    ]
admin.site.register(Proposition, PropositionAdmin)
admin.site.register(Tag)