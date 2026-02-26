from rest_framework import generics, permissions
from django.db.models import Q
from .models import Document
from .serializers import DocumentSerializer
from security.permissions import ArgusAbacPermission

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, ArgusAbacPermission]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile
        
        queryset = Document.objects.filter(
            Q(owner=user) | Q(department=profile.department)
        )
        
        return queryset.filter(sensitivity_level__lte=profile.clearance_level)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)