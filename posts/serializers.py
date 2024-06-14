from rest_framework import serializers

from users.serializers import EmployeeSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    possible_sellers = EmployeeSerializer(many=True, read_only=True)
    chosen_seller = EmployeeSerializer(read_only=True)
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "possible_sellers",
            "is_sold",
            "chosen_seller",
        ]
        read_only_fields = ["creator"]

    def get_creator(self, obj):
        if obj.creator and obj.creator.user:
            return obj.creator.user.employee.name
        else:
            return None
