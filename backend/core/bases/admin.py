from django.contrib import admin

from .models import Base, BaseMembership, Field, Record


class FieldInline(admin.TabularInline):
    model = Field
    extra = 0


class BaseMembershipInline(admin.TabularInline):
    model = BaseMembership
    extra = 0


@admin.register(Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name", "description")
    inlines = [FieldInline, BaseMembershipInline]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ("name", "base", "field_type", "is_required", "order")
    list_filter = ("field_type", "is_required")
    search_fields = ("name",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "base", "created_by", "updated_at")
    search_fields = ("base__name",)
    list_filter = ("base",)


@admin.register(BaseMembership)
class BaseMembershipAdmin(admin.ModelAdmin):
    list_display = ("base", "user", "role")
    list_filter = ("role",)
    search_fields = ("base__name", "user__username")
