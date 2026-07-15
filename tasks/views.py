import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from categories.models import Department, Role, UserCredential
from .models import TaskAssignment
from .serializers import TaskAssignmentSerializer


@require_GET
def get_department_users(request, department_title):
    """Returns roles -> nested active users for a given department (e.g. 'Account Manager')."""
    try:
        department = Department.objects.get(title__iexact=department_title, is_active=True)
    except Department.DoesNotExist:
        return JsonResponse({"error": f"Department '{department_title}' not found."}, status=404)

    roles = Role.objects.filter(department=department, is_active=True).order_by("title")

    data = []
    for role in roles:
        users = UserCredential.objects.filter(role=role, is_active=True).order_by("username")
        if users.exists():  # skip roles with no active users, keeps the picker clean
            data.append({
                "role_id": role.id,
                "role_title": role.title,
                "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users],
            })

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def assign_task(request):
    """
    Creates or updates the (ticket_id, task_type) assignment.
    Body: { ticket_id, task_type, role_id, user_id, assigned_by_id }
    """
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request body."}, status=400)

    ticket_id = payload.get("ticket_id")
    task_type = payload.get("task_type", "lead_handling")
    role_id = payload.get("role_id")
    user_id = payload.get("user_id")
    assigned_by_id = payload.get("assigned_by_id")

    if not ticket_id or not role_id or not user_id:
        return JsonResponse({"error": "ticket_id, role_id and user_id are required."}, status=400)

    try:
        role = Role.objects.select_related("department").get(pk=role_id)
    except Role.DoesNotExist:
        return JsonResponse({"error": "Invalid role."}, status=400)

    try:
        assigned_to = UserCredential.objects.get(pk=user_id, role=role)
    except UserCredential.DoesNotExist:
        return JsonResponse({"error": "Selected user does not belong to the selected role."}, status=400)

    assigned_by = UserCredential.objects.filter(pk=assigned_by_id).first() if assigned_by_id else None

    task, _created = TaskAssignment.objects.update_or_create(
        ticket_id=ticket_id, task_type=task_type,
        defaults={
            "department": role.department,
            "role": role,
            "assigned_to": assigned_to,
            "assigned_by": assigned_by,
            "status": "pending",
        },
    )

    return JsonResponse(TaskAssignmentSerializer(task).data, status=200)


@require_GET
def get_assignments_for_tickets(request):
    """Bulk-fetch current assignments for a list of ticket_ids (used by the Leads table)."""
    ticket_ids = [t.strip() for t in request.GET.get("ticket_ids", "").split(",") if t.strip()]
    task_type = request.GET.get("task_type", "lead_handling")

    if not ticket_ids:
        return JsonResponse([], safe=False)

    tasks = TaskAssignment.objects.filter(ticket_id__in=ticket_ids, task_type=task_type)
    return JsonResponse(TaskAssignmentSerializer(tasks, many=True).data, safe=False)

from leads.models import Lead
from leads.serializers import LeadSerializer
from campaigns.models import Campaign   # ← ADD THIS

@require_GET
def get_my_leads(request):
    """
    Returns leads currently assigned to a specific user (for their dashboard).
    GET /tasks/get_my_leads/?user_id=5&task_type=lead_handling
    """
    user_id = request.GET.get("user_id")
    task_type = request.GET.get("task_type", "lead_handling")

    if not user_id:
        return JsonResponse({"error": "user_id is required."}, status=400)

    assigned_tasks = TaskAssignment.objects.filter(
        assigned_to_id=user_id,
        task_type=task_type,
    ).exclude(status="cancelled")

    ticket_ids = list(assigned_tasks.values_list("ticket_id", flat=True))
    if not ticket_ids:
        return JsonResponse([], safe=False)

    leads = Lead.objects.filter(ticket_id__in=ticket_ids).order_by("-received_at")
    serializer = LeadSerializer(leads, many=True, context={"request": request})

    # ── which of these tickets already have a campaign ──
    campaigned_tickets = set(
        Campaign.objects.filter(ticket_id__in=ticket_ids)
        .values_list("ticket_id", flat=True)
    )   # ← ADD THIS

    # attach each lead's task status/assigned_at so the dashboard can show it
    status_map = {t.ticket_id: t for t in assigned_tasks}
    data = serializer.data
    for lead_data in data:
        task = status_map.get(lead_data.get("ticket_id"))
        lead_data["task_status"] = task.status if task else None
        lead_data["assigned_at"] = task.assigned_at.isoformat() if task else None
        lead_data["has_campaign"] = lead_data.get("ticket_id") in campaigned_tickets   # ← ADD THIS

    return JsonResponse(data, safe=False)