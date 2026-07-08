from django.urls import path
from . import views

# Namespace for all banking app URLs (e.g. {% url 'banking:document_list' %})
app_name = 'banking'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<pk>/', views.document_detail, name='document_detail'),
    path('search/', views.semantic_search_view, name='semantic_search'),
    path('assistant/', views.rag_query_view, name='rag_query'),
    path('tasks/', views.workflow_tasks, name='workflow_tasks'),
    path('tasks/<pk>/complete/', views.complete_task, name='complete_task'),
]
