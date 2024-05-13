from django.urls import path, include
from .views import CompanyRegisterView, EmployeeRegisterView, CompanyViewSet, EmployeeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'employee', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('register/company/', CompanyRegisterView.as_view(), name='register_company'),
    path('register/employee/', EmployeeRegisterView.as_view(), name='register_employee'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]