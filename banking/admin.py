from django.contrib import admin
from .models import BankingDocument, WorkflowTask


@admin.register(BankingDocument)
class BankingDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'status', 'customer_name', 'customer_id', 'created_at']
    list_filter = ['document_type', 'status']
    search_fields = ['title', 'customer_name', 'customer_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WorkflowTask)
class WorkflowTaskAdmin(admin.ModelAdmin):
    list_display = ['task_type', 'document', 'assigned_to', 'is_completed', 'created_at']
    list_filter = ['task_type', 'is_completed']
    readonly_fields = ['created_at', 'completed_at']
