from rest_framework import serializers

from users.serializers import EmployeeSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    possible_sellers = EmployeeSerializer(many=True, read_only=True)
    chosen_seller = EmployeeSerializer(read_only=True)

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
