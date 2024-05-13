from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework import viewsets, generics
from .models import Company, Employee
from .permissions import IsCompanyUser

# Create your views here.
class CompanyRegisterView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este método permite que solo el usuario asociado a una compañía pueda ver sus propios datos.
        """
        user = self.request.user
        if hasattr(user, 'company'):
            return Company.objects.filter(user=user)
        return Company.objects.none()

    def partial_update(self, request, pk=None):
        """
        Permite actualizar parcialmente los datos de la compañía.
        """
        instance = get_object_or_404(Company, pk=pk)
        if instance.user != request.user:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Company, pk=pk)
        if instance.user != request.user:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response({"detail": "Compañía eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

class EmployeeRegisterView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyUser]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este método restringe la vista para que solo muestre empleados de la compañía del usuario actual.
        """
        user = self.request.user
        if hasattr(user, 'company'):
            return Employee.objects.filter(company=user.company)
        return Employee.objects.none()

    def perform_create(self, serializer):
        """
        Sobreescribe la creación para asegurar que los empleados se crean bajo la compañía del usuario.
        """
        if not hasattr(self.request.user, 'company'):
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(company=self.request.user.company)

    def partial_update(self, request, pk=None):
        """
        Actualiza parcialmente la información de un empleado.
        """
        instance = get_object_or_404(Employee, pk=pk)
        if instance.company.user != request.user:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Employee, pk=pk)
        if instance.company.user != request.user:
            return Response({"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()
        return Response({"detail": "Empleado eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)