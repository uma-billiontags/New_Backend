from django.db import models
from categories.models import Department, Role, UserCredential


class TaskAssignment(models.Model):
    TASK_TYPE_CHOICES = (
        ("lead_handling", "Lead Handling"),
        # more task_types (creative_upload, campaign_setup, etc.) added later
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    ticket_id = models.CharField(max_length=20, db_index=True)
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES, default="lead_handling")

    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="task_assignments")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_assignments")
    assigned_to = models.ForeignKey(UserCredential, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="tasks_assigned_to_me")
    assigned_by = models.ForeignKey(UserCredential, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="tasks_assigned_by_me")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)

    # ── for later: turnaround time ──
    deadline_hours = models.PositiveIntegerField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)

    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tbl_task_assignment"
        # one active row per ticket + purpose — reassigning updates this row, not a new one
        unique_together = ("ticket_id", "task_type")
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.ticket_id} → {self.task_type} → {self.assigned_to}"