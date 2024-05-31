from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Company, Employee
from .permissions import IsCompanyUser
from .serializers import CompanySerializer, EmployeeSerializer


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
        Este método permite que solo el usuario
        asociado a una compañía pueda ver sus propios datos.
        """
        user = self.request.user
        if hasattr(user, "company"):
            return Company.objects.filter(user=user)
        return Company.objects.none()

    def get_object(self):
        """
        Este método asegura que solo se pueda acceder a una compañía específica
        si pertenece al usuario actual.
        """
        obj = super().get_object()
        user = self.request.user
        if obj.user != user:
            raise PermissionDenied("No tienes permiso para acceder a esta compañía.")
        return obj

    @action(
        detail=False, methods=["get"], url_path="current", url_name="current_company"
    )
    def current_company(self, request):
        """
        Devuelve la información de la compañía asociada al usuario actual.
        """
        user = request.user
        if hasattr(user, "company"):
            company = user.company
            serializer = self.get_serializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Compañía no encontrada."}, status=status.HTTP_404_NOT_FOUND
        )

    def partial_update(self, request, pk=None):
        """
        Permite actualizar parcialmente los datos de la compañía.
        """
        instance = get_object_or_404(Company, pk=pk)
        if instance.user != request.user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Company, pk=pk)
        if instance.user != request.user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(
            {"detail": "Compañía eliminada correctamente."},
            status=status.HTTP_204_NO_CONTENT,
        )


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
        Este método restringe la vista para que solo muestre empleados
        de la compañía del usuario actual.
        """
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            company = employee.company
            employees = Employee.objects.filter(company=company)
            return employees
        except Employee.DoesNotExist:
            return Employee.objects.none()

    def get_object(self):
        """
        Este método asegura que solo se pueda acceder a un empleado específico
        si pertenece a la misma compañía que el usuario actual.
        """
        obj = super().get_object()
        user = self.request.user

        try:
            employee = Employee.objects.get(user=user)
            if obj.company != employee.company:
                raise PermissionDenied(
                    "No tienes permiso para acceder a este empleado."
                )
        except Employee.DoesNotExist:
            raise PermissionDenied("No tienes permiso para acceder a este empleado.")

        return obj

    @action(
        detail=False, methods=["get"], url_path="current", url_name="current_employee"
    )
    def current_employee(self, request):
        """
        Devuelve la información del empleado asociado al usuario actual.
        """
        user = request.user
        try:
            employee = Employee.objects.get(user=user)
            serializer = self.get_serializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Empleado no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

    def perform_create(self, serializer):
        """
        Sobreescribe la creación para asegurar que los
        empleados se crean bajo la compañía del usuario.
        """
        if not hasattr(self.request.user, "company"):
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(company=self.request.user.company)

    def partial_update(self, request, pk=None):
        """
        Actualiza parcialmente la información de un empleado.
        """
        instance = get_object_or_404(Employee, pk=pk)
        if instance.company.user != request.user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Employee, pk=pk)
        if instance.company.user != request.user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(
            {"detail": "Empleado eliminado correctamente."},
            status=status.HTTP_204_NO_CONTENT,
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["user_type"] = "company" if hasattr(user, "company") else "employee"
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.user
        token = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]
        return Response(
            {
                "refresh": str(refresh),
                "access": str(token),
                "user_type": "company" if hasattr(user, "company") else "employee",
            }
        )
