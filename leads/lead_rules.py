from email.utils import parseaddr
from .models import ExcludedEmail, LeadCategory, generate_ticket_id
from company_details.models import CompanyDetails
from company_details.models import CompanyContacts   # matches contacts too, optional

def extract_email_address(raw_from):
    """'John Doe <john@example.com>' -> 'john@example.com'"""
    _, addr = parseaddr(raw_from or "")
    return addr.lower().strip()


def is_excluded_sender(raw_from):
    sender_email = extract_email_address(raw_from)
    if not sender_email:
        return False
    return ExcludedEmail.objects.filter(email__iexact=sender_email).exists()


def classify_email(subject, body):
    """
    Returns (category_status, category_name).
    Checks categories in priority order; first keyword match wins.
    """
    text = f"{subject or ''} {body or ''}".lower()

    categories = LeadCategory.objects.filter(is_active=True).prefetch_related('keywords')
    for category in categories:
        for kw in category.keywords.all():
            if kw.keyword.lower() in text:
                return 'category', category.name

    return 'uncategory', None

# ── NEW: find a matching CompanyDetails record by sender email ──────────────
def find_matching_client(sender_email):
    """
    Returns a CompanyDetails instance if the sender's email matches either
    the company's own email or one of its registered contacts' emails.
    Returns None if no match is found.
    """
    if not sender_email:
        return None

    client = CompanyDetails.objects.filter(email__iexact=sender_email).first()
    if client:
        return client
    
    contact = CompanyContacts.objects.filter(email__iexact=sender_email).select_related('company').first()
    if contact:
        return contact.company

    return None