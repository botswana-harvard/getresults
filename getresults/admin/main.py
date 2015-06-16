from django.contrib import admin

from ..models import Result, ResultItem, Panel, PanelItem, Utestid, Order, Sender, UtestidMapping


class ResultItemInline(admin.TabularInline):
    model = ResultItem
    extra = 0


class ResultItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'result_datetime'
    list_display = ('result', 'utestid', 'value', 'quantifier', 'result_datetime')
    search_fields = ('result__result_identifier', 'result__order__panel__name',
                     'result_datetime')
admin.site.register(ResultItem, ResultItemAdmin)


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class ResultAdmin(admin.ModelAdmin):
    date_hierarchy = 'collection_datetime'
    list_display = ('result_identifier', 'collection_datetime', 'order',
                    'operator', 'analyzer_name')
    search_fields = ('result_identifier', 'analyzer_name', 'order__order_identifier')
    inlines = [ResultItemInline]
admin.site.register(Result, ResultAdmin)


class PanelItemInline(admin.TabularInline):
    model = PanelItem
    extra = 0


class PanelItemAdmin(admin.ModelAdmin):
    list_display = ('panel', 'utestid')
    search_fields = ('panel__name', 'utestid__name')
admin.site.register(PanelItem, PanelItemAdmin)


class PanelAdmin(admin.ModelAdmin):
    inlines = [PanelItemInline]
admin.site.register(Panel, PanelAdmin)


class UtestidAdmin(admin.ModelAdmin):
    pass
admin.site.register(Utestid, UtestidAdmin)


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'order_datetime'
    list_display = ('order_identifier', 'order_datetime', 'panel', 'aliquot')
    search_fields = ('order_identifier', 'aliquot__aliquot_identifier', 'panel__name')

    inlines = [ResultInline, ]
admin.site.register(Order, OrderAdmin)


class SenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
admin.site.register(Sender, SenderAdmin)


class UtestidMappingAdmin(admin.ModelAdmin):
    list_display = ('sender', 'utestid', 'sender_utestid_name')
    search_fields = ('sender_name', 'utestid', 'sender_utestid_name')
admin.site.register(UtestidMapping, UtestidMappingAdmin)
