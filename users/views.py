from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Company, Employee
from .permissions import IsCompanyUser

# Create your views here.
class CompanyRegisterView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class EmployeeRegisterView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
