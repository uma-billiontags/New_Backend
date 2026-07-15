from rest_framework import serializers
from . import models


class InvoiceBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceBankDetails
        fields = "__all__"


class InvoiceCompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceCompanyAddress
        fields = "__all__"


class InvoiceAuthorizedPersonSerializer(serializers.ModelSerializer):
    # Explicit URL fields so the frontend gets a usable <img src> straight away
    person_sign = serializers.ImageField(required=False)
    company_logo_sign = serializers.ImageField(required=False)

    class Meta:
        model = models.InvoiceAuthorizedPerson
        fields = ("id", "name", "person_sign", "company_logo_sign")


class AdsFormatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdsFormats
        fields = "__all__"


class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metrics
        fields = "__all__"


class ModeOfPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModeOfPayment
        fields = "__all__"


class PaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentTerms
        fields = "__all__"


class EthnicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ethnicity
        fields = "__all__"
        
class RoleSerializer(serializers.ModelSerializer):
    department_title = serializers.CharField(source="department.title", read_only=True)

    class Meta:
        model = models.Role
        fields = ("id", "department", "department_title", "title", "is_active")


class DepartmentSerializer(serializers.ModelSerializer):
    # nested read-only roles list — shows on GET, ignored on POST/PUT (roles created via their own endpoint)
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = models.Department
        fields = ("id", "title", "is_active", "roles")
        
class UserCredentialSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # write_only: never sent back in responses
    department_title = serializers.CharField(source="department.title", read_only=True)
    role_title = serializers.CharField(source="role.title", read_only=True)

    class Meta:
        model = models.UserCredential
        fields = (
            "id", "username", "email", "password",
            "department", "department_title",
            "role", "role_title",
            "is_active",
        )

    def validate(self, data):
        # cross-check: role must actually belong to the submitted department
        department = data.get("department") or getattr(self.instance, "department", None)
        role = data.get("role") or getattr(self.instance, "role", None)

        if department and role and role.department_id != department.id:
            raise serializers.ValidationError({
                "role": f"'{role.title}' does not belong to the '{department.title}' department."
            })
        return data

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        user = models.UserCredential(**validated_data)
        user.set_password(raw_password)
        user.save()
        return user

    def update(self, instance, validated_data):
        raw_password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if raw_password:
            instance.set_password(raw_password)
        instance.save()
        return instance