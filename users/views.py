from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Company, Employee
from .permissions import IsCompanyUser
from .serializers import CompanySerializer, EmployeeSerializer


# Create your views here.
class CompanyRegisterView(generics.CreateAPIView):
    """This view allows the registration of a new company."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This method retrieves all companies,
        accessible by all authenticated users.
        """

        return Company.objects.all()

    def get_object(self):
        """
        This method retrieves a company by its RUT
        without any user-specific restrictions.
        """

        rut = self.kwargs.get("rut")
        return get_object_or_404(Company, rut=rut)

    @action(
        detail=False, methods=["get"], url_path="current", url_name="current_company"
    )
    def current_company(self, request):
        """
        This method returns the information of
        the company associated with the current user.
        """

        user = request.user
        if hasattr(user, "company"):
            company = user.company
            serializer = self.get_serializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Compañía no encontrada."}, status=status.HTTP_404_NOT_FOUND
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="employees",
        url_name="company_employees",
    )
    def employees(self, request):
        """This method returns all employees of the current user's company."""

        user = request.user
        if hasattr(user, "company"):
            company = user.company
            employees = Employee.objects.filter(company=company)
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Compañía no encontrada."}, status=status.HTTP_404_NOT_FOUND
        )

    def partial_update(self, request, rut=None):
        """
        This method allows the current user to partially
        update the company information by RUT.

        Body: {
            "updated_field": updated_value,
            ...
        }
        """

        instance = get_object_or_404(Company, rut=rut)
        if instance.user != request.user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, rut=None):
        """This method allows the current user to delete the company by RUT."""

        instance = get_object_or_404(Company, rut=rut)
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
    """This view allows the registration of a new employee by a user company."""

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
        """This method retrieves all employees."""

        return Employee.objects.all()

    def get_object(self):
        """
        This method retrieves an employee by its
        RUT without any user-specific restrictions.
        """

        rut = self.kwargs.get("rut")
        return get_object_or_404(Employee, rut=rut)

    @action(
        detail=False, methods=["get"], url_path="current", url_name="current_employee"
    )
    def current_employee(self, request):
        """
        This method returns the information of
        the employee associated with the current user.
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

    @action(
        detail=False, methods=["get"], url_path="company", url_name="employee_company"
    )
    def company(self, request):
        """This method returns the company of the current user employee."""

        user = request.user
        try:
            employee = Employee.objects.get(user=user)
            company = employee.company
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Empleado no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, rut=None):
        """
        This method allows the current user or their company
        to update the employee information by RUT.

        Body: {
            "updated_field": new_value,
            ...
        }
        """

        instance = get_object_or_404(Employee, rut=rut)
        user = request.user

        if instance.user != user and instance.company.user != user:
            return Response(
                {"detail": "No autorizado."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, rut=None):
        """
        This method allows the current user or their
        company to delete the employee information by RUT.
        """

        instance = get_object_or_404(Employee, rut=rut)
        user = request.user

        if instance.user != user and instance.company.user != user:
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
        """This method adds the user type to the token response."""

        token = super().get_token(user)
        # Add custom claims
        token["user_type"] = "company" if hasattr(user, "company") else "employee"
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        This method returns the token response with the user type.

        Body: {
            "username": "user's username",
            "password": "user's password"
        }
        """

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
