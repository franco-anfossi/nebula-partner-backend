from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CompanyRegisterView,
    CompanyViewSet,
    EmployeeRegisterView,
    EmployeeViewSet,
    MyTokenObtainPairView,
)

router = DefaultRouter()
router.register(r"company", CompanyViewSet, basename="company")
router.register(r"employee", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
    path("register/company/", CompanyRegisterView.as_view(), name="register_company"),
    path(
        "register/employee/", EmployeeRegisterView.as_view(), name="register_employee"
    ),
    path(
        "company/<str:rut>/",
        CompanyViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="company-detail",
    ),
    path(
        "employee/<str:rut>/",
        EmployeeViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="employee-detail",
    ),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
