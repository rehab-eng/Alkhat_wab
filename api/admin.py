from django.contrib import admin

from .models import Project, Stat, Truck


admin.site.site_header = 'KHUTUT ALRIMAL Command Center'
admin.site.site_title = 'KHUTUT ALRIMAL Admin'
admin.site.index_title = 'Golden Sands Administration'


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    ordering = ('-date',)
    list_filter = ('date',)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'suffix', 'order', 'updated_at')
    list_editable = ('value', 'suffix', 'order')
    ordering = ('order', 'key')
