# api/urls.py
from django.urls import path
from .views import (
    DocumentListView, DocumentHistoryView, DocumentProcessView, DocumentChatView,
    RiskAnalysisView, FraudDetectionView, ComplianceCheckView, SimplifyView,
    ClauseGeneratorView, DocumentCompareView, LawyerRecommendView,
    TranslatorView, SaveSignatureView, DownloadSignedView,
    DownloadSummaryPDFView, DownloadTranslatedPDFView,
)

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='documents-list'),
    path('process-document/', DocumentProcessView.as_view(), name='process-document'),
    path('chat/', DocumentChatView.as_view(), name='document-chat'),
    path('risk/<int:pk>/', RiskAnalysisView.as_view(), name='risk-analysis'),
    path('fraud/<int:pk>/', FraudDetectionView.as_view(), name='fraud-detection'),
    path('compliance/<int:pk>/', ComplianceCheckView.as_view(), name='compliance-check'),
    path('simplify/', SimplifyView.as_view(), name='simplify'),
    path('generate-clause/', ClauseGeneratorView.as_view(), name='generate-clause'),
    path('compare/', DocumentCompareView.as_view(), name='compare-documents'),
    path('lawyers/', LawyerRecommendView.as_view(), name='lawyer-recommend'),
    path('translate/', TranslatorView.as_view(), name='translate'),
    path('save-signature/', SaveSignatureView.as_view(), name='save-signature'),
    path('download-signed/<int:pk>/', DownloadSignedView.as_view(), name='download-signed'),
    path('download-summary/<int:pk>/', DownloadSummaryPDFView.as_view(), name='download-summary'),
    path('download-translated-pdf/', DownloadTranslatedPDFView.as_view(), name='download-translated-pdf'),
    path('history/<int:pk>/', DocumentHistoryView.as_view(), name='document-history'),
]