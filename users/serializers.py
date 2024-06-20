from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Company, Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class CompanySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Company
        fields = ["id", "rut", "name", "phone_number", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data["rut"],
            email=validated_data["email"],
            password=password,
        )

        company = Company.objects.create(user=user, **validated_data)
        return company


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    employee_type = serializers.ChoiceField(
        choices=(("buyer", "Buyer"), ("seller", "Seller")), required=False
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "rut",
            "name",
            "phone_number",
            "email",
            "password",
            "employee_type",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=validated_data["rut"],
            email=validated_data["email"],
            password=password,
        )
        company_user = self.context["request"].user.company
        validated_data.pop("company", None)
        employee = Employee.objects.create(
            user=user, company=company_user, **validated_data
        )
        return employee
