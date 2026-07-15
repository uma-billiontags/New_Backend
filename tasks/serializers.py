from rest_framework import serializers
from .models import TaskAssignment


class TaskAssignmentSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source="assigned_to.username", read_only=True, default=None)
    assigned_by_name = serializers.CharField(source="assigned_by.username", read_only=True, default=None)
    role_title = serializers.CharField(source="role.title", read_only=True, default=None)
    department_title = serializers.CharField(source="department.title", read_only=True, default=None)

    class Meta:
        model = TaskAssignment
        fields = (
            "id", "ticket_id", "task_type",
            "department", "department_title",
            "role", "role_title",
            "assigned_to", "assigned_to_name",
            "assigned_by", "assigned_by_name",
            "status", "notes",
            "assigned_at", "updated_at",
        )