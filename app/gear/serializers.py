from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for item objects"""

    class Meta:
        model = Item
        fields = ('id', 'name', 'notes', 'weight')
        read_only_fields = ('id',)
