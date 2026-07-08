from django import forms
from .models import BankingDocument


# Form for uploading a new banking document.
class DocumentUploadForm(forms.ModelForm):
    pdf_file = forms.FileField(
        required=False,
        label='PDF Document',
        help_text='Upload a text-based PDF — its text is extracted automatically.',
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
    )

    class Meta:
        model = BankingDocument
        fields = ['title', 'document_type', 'pdf_file', 'content', 'customer_name', 'customer_id', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Paste content here, or leave blank if uploading a PDF above.'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Loan Application – John Smith'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'e.g. John Smith'}),
            'customer_id': forms.TextInput(attrs={'placeholder': 'e.g. CUST-001'}),
        }
        help_texts = {
            'content': 'Optional if you upload a PDF above.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Content is required on the model, but here it may be filled from a PDF.
        self.fields['content'].required = False

    def clean_pdf_file(self):
        pdf = self.cleaned_data.get('pdf_file')
        if pdf and not pdf.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Please upload a file with a .pdf extension.')
        return pdf

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('pdf_file') and not (cleaned.get('content') or '').strip():
            raise forms.ValidationError(
                'Provide document text: either upload a PDF or paste content.'
            )
        return cleaned



# Form for the semantic search page.
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=500,
        label='Search Query',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. mortgage loan requirements for first-time buyers'}),
    )
    document_type = forms.ChoiceField(
        choices=[('', 'All Types')] + BankingDocument.DOCUMENT_TYPES,
        required=False,
        label='Filter by Type',
    )
    limit = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=5,
        required=False,
        label='Results',
    )



# Form for the RAG retrieval assistant.
class RAGQueryForm(forms.Form):
    question = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'e.g. What are the outstanding compliance issues for customer CUST-007?',
        }),
        label='Your Question',
    )
    document_type = forms.ChoiceField(
        choices=[('', 'All Types')] + BankingDocument.DOCUMENT_TYPES,
        required=False,
        label='Limit to Document Type',
    )
