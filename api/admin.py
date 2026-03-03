from django.contrib import admin

from .models import Project, SiteSetting, Stat, Statistic, Truck, Vehicle


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


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title',)
    ordering = ('-updated_at',)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'suffix', 'order', 'updated_at')
    list_editable = ('value', 'suffix', 'order')
    search_fields = ('key', 'label_en', 'label_ar')
    ordering = ('order', 'key')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name_en', 'contact_phone', 'updated_at')
    search_fields = ('site_name_en', 'site_name_ar')
    ordering = ('-updated_at',)
