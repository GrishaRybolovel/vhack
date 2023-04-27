from django.contrib import admin

from .models import *

# Register your models here.

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'role', 'phone', 'user', 'post', 'status')
    list_display_links = ('id',)
    search_fields = ('id', 'name', 'role')


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')
    search_fields = ('id', 'message')


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'created', 'completion', 'done')
    list_display_links = ('id',)
    search_fields = ('id', 'author')


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contract', 'status', 'date_creation')
    search_fields = ('id',)

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'doc_type', 'duration', 'doc')
    search_fields = ('id', 'name')

class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_division')
    list_display_links = ('id',)
    search_fields = ('name',)

class CompanyDocumentsAdmin(admin.ModelAdmin):
    list_display = ('id',)

class MailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'naming', 'created', 'date_reg', 'number', 'author')
    list_display_links = ('id',)
    search_fields = ('id', 'name', 'date_reg')

admin.site.register(Employees, EmployeesAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Divisions, DivisionsAdmin)
admin.site.register(CompanyDocuments, CompanyDocumentsAdmin)
admin.site.register(Mails, MailsAdmin)