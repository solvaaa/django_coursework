from django.contrib import admin
import mailing.models as model
# Register your models here.


@admin.register(model.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name', 'comment')


@admin.register(model.Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'frequency', 'status')
    list_filter = ('frequency', 'status')


@admin.register(model.MailingMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', )
    search_fields = ('subject', 'body')


@admin.register(model.MailingLogs)
class LogsAdmin(admin.ModelAdmin):
    readonly_fields = ('attempt_time', 'attempt_status', 'server_response')
    list_display = ('attempt_time', 'attempt_status', 'server_response')
    list_filter = ('attempt_status', 'server_response')
    search_fields = ('attempt_time', )
