from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Lead, LeadCategory, generate_ticket_id
from .lead_rules import extract_email_address, find_matching_client
from .serializers import LeadSerializer, LeadCategorySerializer
from django.db import IntegrityError


class LeadListAPIView(generics.ListAPIView):
    queryset = Lead.objects.all().order_by("-received_at")
    serializer_class = LeadSerializer


class LeadCategoryListAPIView(generics.ListAPIView):
    """Returns active categories for the edit-category dropdown."""
    queryset = LeadCategory.objects.filter(is_active=True).order_by('priority', 'name')
    serializer_class = LeadCategorySerializer


class LeadCategorizeAPIView(APIView):
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

        if not lead.client:
            sender_email = extract_email_address(lead.sender)
            client = find_matching_client(sender_email)
            if client:
                lead.client = client

        # retry a couple of times in case of a ticket_id collision
        for attempt in range(3):
            if not lead.ticket_id:
                lead.ticket_id = generate_ticket_id()
            try:
                lead.save()
                break
            except IntegrityError:
                if attempt == 2:
                    return Response({"error": "Could not generate a unique ticket ID, please retry."}, status=500)
                lead.ticket_id = None  # force a fresh generation and try again

        serializer = LeadSerializer(lead, context={"request": request})
        return Response(serializer.data, status=200)