import json
from rest_framework import serializers
from .models import CompanyDetails, CompanyContacts, CompanyAddress, generate_client_id

class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        exclude = ['company']


class CompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContacts
        exclude = ['company', 'user']


class CompanyDetailsSerializer(serializers.ModelSerializer):

    addresses = CompanyAddressSerializer(many=True, required=False)
    contacts = CompanyContactSerializer(many=True, required=False)

    class Meta:
        model = CompanyDetails
        exclude = ['user', 'client_id']   # user + client_id are set in the view/create(), not client-supplied

  
    def to_internal_value(self, data):
        data = data.copy()

        # unwrap JSON-string fields (only relevant if sent as multipart form fields)
        for key in ("addresses", "contacts", "billing"):
            if isinstance(data.get(key), str):
                try:
                    data[key] = json.loads(data[key])
                except Exception:
                    raise serializers.ValidationError(f"Invalid JSON for '{key}'")

        # flatten "billing" onto the top level — CompanyDetails stores these
        # fields directly, there's no separate ClientBilling model
        billing = data.pop("billing", {}) or {}
        for k, v in billing.items():
            data[k] = v

        return super().to_internal_value(data)
    
     # ── NEW: domain cross-check against the contacts submitted in this same request ──
    @staticmethod
    def _extract_domain(email):
        email = (email or "").strip().lower()
        if "@" not in email:
            return None
        return email.split("@")[-1]

    def validate(self, data):
        contacts = data.get("contacts", [])

        allowed_domains = set()
        for c in contacts:
            domain = self._extract_domain(c.get("email", ""))
            if domain:
                allowed_domains.add(domain)

        # no contacts submitted at all -> nothing to validate against
        if not allowed_domains:
            return data

        for field_name in ("default_email_send_to", "default_email_send_cc"):
            value = data.get(field_name)
            if not value:
                continue
            
            emails = [e.strip() for e in value.split(",") if e.strip()]
            invalid_emails = [
                e for e in emails if self._extract_domain(e) not in allowed_domains
            ]
            if invalid_emails:
                raise serializers.ValidationError({
                    field_name: (
                        "These email(s) don't match any Company Contact's domain "
                        f"({', '.join(sorted(allowed_domains))}): {', '.join(invalid_emails)}"
                    )
                })

        return data

    def create(self, validated_data):
        addresses_data = validated_data.pop("addresses", [])
        contacts_data = validated_data.pop("contacts", [])
        signatures = self.context.get("signatures", {})
        user = self.context["user"]

        company = CompanyDetails.objects.create(
            user=user,
            client_id=generate_client_id(),
            **validated_data,
        )
        
        first_contact = None
        for index, contact in enumerate(contacts_data):
            sig = signatures.get(f"contact_signature_{index}")
            contact_obj = CompanyContacts.objects.create(company=company, **contact)
            if sig:
                contact_obj.digital_signature = sig
                contact_obj.save()
            if index == 0:
                first_contact = contact_obj

        if first_contact:
            company.default_contact_person = first_contact
            company.save(update_fields=["default_contact_person"])

        for addr in addresses_data:
            CompanyAddress.objects.create(company=company, **addr)

        return company