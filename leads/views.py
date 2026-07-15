from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lead, LeadCategory, generate_ticket_id
from .lead_rules import extract_email_address, find_matching_client
from .serializers import LeadSerializer, LeadCategorySerializer


class LeadListAPIView(generics.ListAPIView):
    queryset = Lead.objects.all().order_by("-received_at")
    serializer_class = LeadSerializer


class LeadCategoryListAPIView(generics.ListAPIView):
    """Returns active categories for the edit-category dropdown."""
    queryset = LeadCategory.objects.filter(is_active=True).order_by('priority', 'name')
    serializer_class = LeadCategorySerializer


class LeadCategorizeAPIView(APIView):
    """
    PATCH /leads/categorize_lead/<pk>/  { "category_name": "Creative Team" }
    Assigns a category to an uncategorized lead, generates a ticket_id,
    and tries to link a matching client if one isn't already set.
    """
    def patch(self, request, pk):
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=404)

        category_name = request.data.get("category_name")
        if not category_name:
            return Response({"error": "category_name is required"}, status=400)

        if not LeadCategory.objects.filter(name=category_name, is_active=True).exists():
            return Response({"error": "Invalid category"}, status=400)

        lead.category_name = category_name
        lead.category_status = "category"

        if not lead.ticket_id:
            lead.ticket_id = generate_ticket_id()

        if not lead.client:
            sender_email = extract_email_address(lead.sender)
            client = find_matching_client(sender_email)
            if client:
                lead.client = client

        lead.save()

        serializer = LeadSerializer(lead, context={"request": request})
        return Response(serializer.data, status=200)