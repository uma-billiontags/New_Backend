from django.contrib import admin
from .models import Lead, ExcludedEmail, LeadCategory, CategoryKeyword


class CategoryKeywordInline(admin.TabularInline):
    model = CategoryKeyword
    extra = 1


@admin.register(LeadCategory)
class LeadCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'is_active')
    inlines = [CategoryKeywordInline]


@admin.register(ExcludedEmail)
class ExcludedEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'reason', 'created_at')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'subject', 'sender', 'category_status', 'category_name', 'received_at')
    list_filter = ('category_status', 'category_name')
    search_fields = ('ticket_id' , 'subject', 'sender', 'body')