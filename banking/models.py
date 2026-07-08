from django.db import models


class BankingDocument(models.Model):
    DOCUMENT_TYPES = [
        ('loan_application', 'Loan Application'),
        ('kyc', 'KYC Document'),
        ('compliance', 'Compliance Report'),
        ('account_statement', 'Account Statement'),
        ('risk_assessment', 'Risk Assessment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    customer_name = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=100)
    embedding = models.JSONField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_document_type_display()}: {self.title}"


class WorkflowTask(models.Model):
    TASK_TYPES = [
        ('document_review', 'Document Review'),
        ('compliance_check', 'Compliance Check'),
        ('approval_request', 'Approval Request'),
        ('risk_assessment', 'Risk Assessment'),
    ]

    document = models.ForeignKey(
        BankingDocument, on_delete=models.CASCADE, related_name='tasks'
    )
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    description = models.TextField()
    assigned_to = models.CharField(max_length=255, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_task_type_display()} for {self.document.title}"
