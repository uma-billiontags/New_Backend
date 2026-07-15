import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import CompanyDetails
from .serializers import CompanyDetailsSerializer


@api_view(["POST"])
def create_client(request):
    try:
        # ── signature files (contact_signature_0, contact_signature_1, ...) ──
        signatures = {
            key: request.FILES[key]
            for key in request.FILES
            if key.startswith("contact_signature_")
        }

        # ── multipart sends the JSON as a 'data' string field; plain JSON body otherwise ──
        raw = request.data.get("data")
        data = json.loads(raw) if raw else request.data

        # ── duplicate checks ──
        email = data.get("email")
        name = data.get("name")

        if email and CompanyDetails.objects.filter(email=email).exists():
            return Response({"error": "This email is already registered"}, status=400)

        if name and CompanyDetails.objects.filter(name=name).exists():
            return Response({"error": "A client with this company name already exists"}, status=400)

        # ── login account for the client ──
        user, created = User.objects.get_or_create(username=email, defaults={"email": email})
        if created:
            user.set_unusable_password()
            user.save()

        # ── validate + save ──
        lead_id = data.pop("lead_id", None)  # pull it out before serializer validation
        serializer = CompanyDetailsSerializer(data=data, context={"signatures": signatures, "user": user})

        if serializer.is_valid():
            client = serializer.save()
            
            if lead_id:
                from leads.models import Lead
                Lead.objects.filter(pk=lead_id, client__isnull=True).update(client=client)

            return Response(
                {"message": "Client created successfully", "client_id": client.client_id},
                status=201,
            )

        return Response(serializer.errors, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)