from django.db import models
import base64
from django.contrib.auth.hashers import make_password, check_password


# Multiple bank accounts supported (Indian + international — IFSC for India, SWIFT/IBAN for international).
class InvoiceBankDetails(models.Model):
    objects = None
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100, blank=True)
    swift_code = models.CharField(max_length=100, blank=True, null=True)
    iban_number = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, unique=True)
    bank_address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tbl_invoice_bank_details"

    def __str__(self):
        return "{}-{}".format(self.bank_name, self.nick_name)

#  Billing address with Indian tax numbers
class InvoiceCompanyAddress(models.Model):
    objects = None
    company_name = models.CharField(max_length=200)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=30, blank=True, null=True)
    gst_number = models.CharField(max_length=80, blank=True, null=True)
    cin_number = models.CharField(max_length=80, blank=True, null=True)
    tan_number = models.CharField(max_length=80, blank=True, null=True)
    trn_number = models.CharField(max_length=80, blank=True, null=True)
    license_number = models.CharField(max_length=80, blank=True, null=True)
    sac_number = models.CharField(max_length=80, blank=True, null=True)
    ct_number = models.CharField(max_length=80, blank=True, null=True)
    is_active = models.BooleanField(default=True, )

    class Meta:
        db_table = "tbl_invoice_company_details"

    def __str__(self):
        return self.company_name


class InvoiceAuthorizedPerson(models.Model):
    objects = None
    name = models.CharField(max_length=255, unique=True)
    person_sign = models.ImageField(upload_to="media/authorized_person", verbose_name="Person Sign")   # signature image
    company_logo_sign = models.ImageField(upload_to="media/authorized_person_logo", verbose_name="Company Seal") # company seal image

    class Meta:
        db_table = "tbl_invoice_authorized_person"
        
    def __str__(self):
        return self.name

    def person_sign_data(self):
        with open(self.person_sign.path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
             # converts image to base64 string
            return "data:image/png;base64," + encoded_string.decode('utf-8')

    def company_logo_sign_data(self):
        with open(self.company_logo_sign.path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return "data:image/png;base64," + encoded_string.decode('utf-8')


# e.g. Banner, Video, Native Simple lookup table for ad format types used in insertion orders.
class AdsFormats(models.Model):
    objects = None
    title = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_ads_formats"
        verbose_name = "Ad Format"
        verbose_name_plural = "Ad Format"

    def __str__(self):
        return self.title

#  e.g. CPM, CPC, CPL KPI metrics used in campaigns.
class Metrics(models.Model):
    objects = None
    title = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_metrics"
        verbose_name = "Metrics"
        verbose_name_plural = "Metrics"

    def __str__(self):
        return self.title


# e.g. Bank Transfer, Cheque, UPI
class ModeOfPayment(models.Model):
    objects = None
    title = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "tbl_mode_of_payment"
        verbose_name = "Mode of Payment"
        verbose_name_plural = "Mode of Payment"

    def __str__(self):
        return self.title


# Used in invoices to define when payment is due.
class PaymentTerms(models.Model):
    objects = None
    title = models.CharField(max_length=50, unique=True)
    days = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_payment_terms"
        verbose_name = "Payment Term"
        verbose_name_plural = 'Payment Terms'

    def __str__(self):
        return self.title

class Ethnicity(models.Model):
    objects = None
    title = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_country_ethnicity"
        verbose_name = "Ethnicity"
        verbose_name_plural = "Ethnicity"

    def __str__(self):
        return self.title

# Departments (e.g. Creative, Campaign, Finance) with roles nested under each one.
class Department(models.Model):
    objects = None
    title = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_department"
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["title"]

    def __str__(self):
        return self.title


# Roles under a department (e.g. Account Director, Manager, Executive under Creative).
class Role(models.Model):
    objects = None
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles")
    title = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["department__title", "title"]
        # same role title can repeat across departments, but not twice within one
        unique_together = ("department", "title")

    def __str__(self):
        return f"{self.title} ({self.department.title})"
    

class UserCredential(models.Model):
    objects = None
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)  # stores the HASHED password, never plaintext

    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="user_credentials")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="user_credentials")

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_user_credential"
        verbose_name = "User Credential"
        verbose_name_plural = "User Credentials"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} — {self.role.title} ({self.department.title})"

    def set_password(self, raw_password):
        """Hash and store the password. Always call this instead of assigning .password directly."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify a login attempt against the stored hash."""
        return check_password(raw_password, self.password)