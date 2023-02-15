from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ["id", "title", "memo", "created", "completed"]


class TodoToggleCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        """
        "Creating a ModelSerializer without either 
        the 'fields' attribute or the 'exclude' attribute has been deprecated 
        since 3.3.0, and is now disallowed. 
        Add an explicit fields = '__all__' to the TodoToggleCompleteSerializer serializer."
        """
        fields = ["id", "completed"]  # why need to show id?
        read_only_fields = ["title", "memo", "created", "completed"]
