from django.contrib import admin
from django.contrib.admin import AdminSite  # custom admin panel 
from categories import models
from django import forms

@admin.register(models.InvoiceBankDetails)
class InvoiceBankDetailsAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "ifsc_code", "swift_code", "account_number", "is_active")
    list_display_links = ("bank_name", "ifsc_code", "swift_code", "account_number", "is_active")

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(models.InvoiceCompanyAddress)
class InvoiceCompanyAddressAdmin(admin.ModelAdmin):
    list_display = ("company_name", "address_line_1", "address_line_2", "city", "state_name", "is_active")
    list_display_links = ("company_name", "address_line_1", "address_line_2", "city", "state_name", "is_active")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.InvoiceAuthorizedPerson)
class InvoiceAuthorizedPersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(models.AdsFormats, models.Metrics)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_on")
    search_fields = ("title",)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.ModeOfPayment)
class ModeOfPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.PaymentTerms)
class PaymentTermsAdmin(admin.ModelAdmin):
    list_display = ("title", "days", "is_active", "created_on")
    search_fields = ("title",)

    def has_delete_permission(self, request, obj=None):
        return False


class RoleInline(admin.TabularInline):
    model = models.Role
    extra = 1


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_on")
    search_fields = ("title",)
    inlines = [RoleInline]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "is_active")
    list_filter = ("department",)
    search_fields = ("title",)

    def has_delete_permission(self, request, obj=None):
        return False

class UserCredentialAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Leave blank when editing to keep the current password unchanged.",
    )

    class Meta:
        model = models.UserCredential
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:   # creating a new user → password is mandatory
            self.fields["password"].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            instance.set_password(raw_password)  # hashes it — never stored as plain text
        if commit:
            instance.save()
        return instance
    
@admin.register(models.UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    form = UserCredentialAdminForm  
    list_display = ("username", "email", "department", "role", "is_active")
    list_filter = ("department", "role", "is_active")
    search_fields = ("username", "email")

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.Ethnicity)
class EthnicityAdmin(admin.ModelAdmin):
    list_display = ("title", "created_on", "updated_on")
    search_fields = ("title",)

    def has_delete_permission(self, request, obj=None):
        return False