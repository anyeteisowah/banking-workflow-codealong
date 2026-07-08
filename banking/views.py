from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import BankingDocument, WorkflowTask
from .forms import DocumentUploadForm, SearchForm, RAGQueryForm
from .services.embedding_service import generate_embedding
from .services.vector_search_service import semantic_search
from .services.rag_service import answer_query
from .services.pdf_service import extract_text_from_pdf, PDFExtractionError


def document_list(request):
    documents = BankingDocument.objects.all()
    doc_type = request.GET.get('type')
    status = request.GET.get('status')

    if doc_type:
        documents = documents.filter(document_type=doc_type)
    if status:
        documents = documents.filter(status=status)

    context = {
        'documents': documents,
        'document_types': BankingDocument.DOCUMENT_TYPES,
        'status_choices': BankingDocument.STATUS_CHOICES,
        'current_type': doc_type,
        'current_status': status,
    }
    return render(request, 'banking/document_list.html', context)


def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)

            # A PDF upload takes precedence: extract its text into content.
            pdf = form.cleaned_data.get('pdf_file')
            if pdf:
                try:
                    document.content = extract_text_from_pdf(pdf)
                except PDFExtractionError as e:
                    messages.error(request, str(e))
                    return render(request, 'banking/document_upload.html', {'form': form})

            text_to_embed = f"{document.title}\n{document.content}"
            indexed = True
            try:
                document.embedding = generate_embedding(text_to_embed)
            except Exception as e:
                indexed = False
                messages.warning(request, f'Document saved but embedding generation failed: {e}')
            document.save()
            _create_workflow_tasks(document)
            if indexed:
                messages.success(request, f'Document "{document.title}" uploaded and indexed successfully.')
            else:
                messages.info(request, f'Document "{document.title}" uploaded. Add a valid Voyage AI key to generate embeddings for semantic search.')
            return redirect('banking:document_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'banking/document_upload.html', {'form': form})


def document_detail(request, pk):
    document = get_object_or_404(BankingDocument, pk=pk)
    tasks = document.tasks.all()
    return render(request, 'banking/document_detail.html', {
        'document': document,
        'tasks': tasks,
    })


def semantic_search_view(request):
    results = []
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            doc_type = form.cleaned_data.get('document_type') or None
            limit = form.cleaned_data.get('limit') or 5
            try:
                query_embedding = generate_embedding(query)
                results = semantic_search(query_embedding, limit=limit, document_type=doc_type)
            except Exception as e:
                messages.error(request, f'Search failed: {e}')

    return render(request, 'banking/search.html', {'form': form, 'results': results})


def rag_query_view(request):
    answer = None
    sources = []
    form = RAGQueryForm()

    if request.method == 'POST':
        form = RAGQueryForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            doc_type = form.cleaned_data.get('document_type') or None
            try:
                result = answer_query(question, document_type=doc_type)
                answer = result['answer']
                sources = result['sources']
            except Exception as e:
                messages.error(request, f'Query failed: {e}')

    return render(request, 'banking/rag_query.html', {
        'form': form,
        'answer': answer,
        'sources': sources,
    })


def workflow_tasks(request):
    tasks = WorkflowTask.objects.filter(is_completed=False)
    return render(request, 'banking/workflow_tasks.html', {'tasks': tasks})


def complete_task(request, pk):
    task = get_object_or_404(WorkflowTask, pk=pk)
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, f'Task "{task.get_task_type_display()}" marked as completed.')
    return redirect('banking:workflow_tasks')


def _create_workflow_tasks(document):
    task_map = {
        'loan_application': [
            ('document_review', 'Review loan application documents for completeness'),
            ('risk_assessment', 'Conduct risk assessment for loan applicant'),
            ('approval_request', 'Submit for final approval'),
        ],
        'kyc': [
            ('document_review', 'Verify identity documents'),
            ('compliance_check', 'Run compliance and AML checks'),
        ],
        'compliance': [
            ('compliance_check', 'Review compliance report and flag issues'),
        ],
        'account_statement': [
            ('document_review', 'Review account statement for anomalies'),
        ],
        'risk_assessment': [
            ('risk_assessment', 'Validate risk assessment methodology'),
            ('approval_request', 'Route to risk committee for approval'),
        ],
    }
    for task_type, description in task_map.get(document.document_type, []):
        WorkflowTask.objects.create(
            document=document,
            task_type=task_type,
            description=description,
        )
