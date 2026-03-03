from rest_framework import generics, permissions
from django.db.models import Q
from .models import Document
from .serializers import DocumentSerializer
from security.permissions import ArgusAbacPermission
from rest_framework.pagination import PageNumberPagination 

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, ArgusAbacPermission]
    pagination_class = StandardResultsSetPagination 

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        
        queryset = Document.objects.filter(
            Q(owner=user) | Q(department=profile.department)
        )
        
        return queryset.filter(sensitivity_level__lte=profile.clearance_level)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, ArgusAbacPermission]