from django.contrib import admin
import mailing.models as model
from mailing.scheduler import remove_job


# Register your models here.


@admin.register(model.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'user')
    search_fields = ('email', 'name', 'comment')
    readonly_fields = ('user', )


@admin.register(model.Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'mailing_time', 'frequency', 'status', 'user')
    readonly_fields = ('user', )
    list_filter = ('frequency', 'status')

    def delete_model(self, request, obj):
        job_id = obj.pk
        remove_job(job_id)
        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            job_id = obj.pk
            remove_job(job_id)
        return super().delete_queryset(request, queryset)


@admin.register(model.MailingMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user')
    search_fields = ('subject', 'body')
    readonly_fields = ('user', )


@admin.register(model.MailingLogs)
class LogsAdmin(admin.ModelAdmin):
    readonly_fields = ('attempt_time', 'attempt_status', 'server_response')
    list_display = ('attempt_time', 'attempt_status', 'server_response')
    list_filter = ('attempt_status', 'server_response')
    search_fields = ('attempt_time', )
