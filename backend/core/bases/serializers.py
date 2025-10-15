from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Base, BaseMembership, Field, FieldTypes, Record

User = get_user_model()


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ["id", "name", "field_type", "is_required", "options", "order"]

    def validate(self, attrs):
        field_type = attrs.get('field_type', getattr(self.instance, 'field_type', None))
        options = attrs.get('options', getattr(self.instance, 'options', {})) or {}
        if field_type in {FieldTypes.SINGLE_SELECT, FieldTypes.MULTI_SELECT} and 'choices' not in options:
            raise serializers.ValidationError({"options": "Select fields must define a 'choices' list."})
        return attrs


class BaseMembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BaseMembership
        fields = ["id", "user", "role"]


class BaseSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=False)
    memberships = BaseMembershipSerializer(many=True, required=False)

    class Meta:
        model = Base
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "created_at",
            "updated_at",
            "fields",
            "memberships",
        ]
        read_only_fields = ["base", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        fields_data = validated_data.pop("fields", [])
        memberships_data = validated_data.pop("memberships", [])
        base = Base.objects.create(**validated_data)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            BaseMembership.objects.get_or_create(
                base=base,
                user=request.user,
                defaults={"role": BaseMembership.MembershipRole.ADMIN},
            )
        self._sync_fields(base, fields_data)
        self._sync_memberships(base, memberships_data)
        return base

    def update(self, instance, validated_data):
        fields_data = validated_data.pop("fields", None)
        memberships_data = validated_data.pop("memberships", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if fields_data is not None:
            self._sync_fields(instance, fields_data)
        if memberships_data is not None:
            self._sync_memberships(instance, memberships_data)
        return instance

    def _sync_fields(self, base, fields_data):
        existing_ids = []
        for field_data in fields_data:
            field_id = field_data.get("id")
            defaults = field_data.copy()
            defaults.pop("id", None)
            if field_id:
                Field.objects.update_or_create(id=field_id, defaults={**defaults, "base": base})
                existing_ids.append(field_id)
            else:
                Field.objects.create(base=base, **defaults)
        if fields_data == []:
            Field.objects.filter(base=base).delete()
        elif existing_ids:
            Field.objects.filter(base=base).exclude(id__in=existing_ids).delete()

    def _sync_memberships(self, base, memberships_data):
        existing_ids = []
        for membership in memberships_data:
            membership_id = membership.get("id")
            defaults = membership.copy()
            defaults.pop("id", None)
            if membership_id:
                BaseMembership.objects.update_or_create(
                    id=membership_id,
                    defaults={**defaults, "base": base},
                )
                existing_ids.append(membership_id)
            else:
                BaseMembership.objects.create(base=base, **defaults)
        creator = base.created_by
        if creator:
            BaseMembership.objects.get_or_create(
                base=base,
                user=creator,
                defaults={"role": BaseMembership.MembershipRole.ADMIN},
            )
        if memberships_data == []:
            BaseMembership.objects.filter(base=base).exclude(user=creator).delete()
        elif existing_ids:
            BaseMembership.objects.filter(base=base).exclude(id__in=existing_ids).exclude(user=creator).delete()


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ["id", "base", "data", "created_by", "created_at", "updated_at"]
        read_only_fields = ["base", "created_by", "created_at", "updated_at"]

    def validate(self, attrs):
        base = attrs.get("base") or self.context.get("base")
        if self.instance and not base:
            base = self.instance.base
        if not base:
            raise serializers.ValidationError({"base": "Base context is required."})
        data = attrs.get("data", getattr(self.instance, "data", {}))
        record = Record(base=base, data=data)
        record.clean_data()
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        base = validated_data.get("base") or self.context.get("base")
        record = Record(base=base, data=validated_data.get("data", {}), created_by=user)
        record.clean_data()
        validated_data["data"] = record.data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        data = validated_data.get("data", instance.data)
        record = Record(base=instance.base, data=data, created_by=instance.created_by)
        record.clean_data()
        instance.data = record.data
        instance.save()
        return instance


class AnalyticsSerializer(serializers.Serializer):
    base_id = serializers.IntegerField()
    record_count = serializers.IntegerField()
    aggregations = serializers.DictField(child=serializers.DictField(), default=dict)
