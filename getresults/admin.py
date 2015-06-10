from django.contrib import admin

from .models import Result, ResultItem, Panel, PanelItem, Utestid


class ResultAdmin(admin.ModelAdmin):
    list_display = ('result_identifier', 'collection_datetime', 'panel',
                    'operator', 'analyzer_name')
    search_fields = ('result_identifier', 'source')
admin.site.register(Result, ResultAdmin)


class ResultItemAdmin(admin.ModelAdmin):
    list_display = ('result', 'utestid', 'value', 'quantifier', 'result_datetime')
    search_fields = ('result__result_identifier', 'result__panel__name',
                     'result_datetime')
admin.site.register(ResultItem, ResultItemAdmin)


class PanelAdmin(admin.ModelAdmin):
    pass
admin.site.register(Panel, PanelAdmin)


class PanelItemAdmin(admin.ModelAdmin):
    list_display = ('panel', 'utestid')
    search_fields = ('panel__name', 'utestid__name')
admin.site.register(PanelItem, PanelItemAdmin)


class UtestidAdmin(admin.ModelAdmin):
    pass
admin.site.register(Utestid, UtestidAdmin)
