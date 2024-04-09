from django.urls import path, include
from .views import CompanyRegisterView, EmployeeRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/company/', CompanyRegisterView.as_view(), name='register_company'),
    path('register/employee/', EmployeeRegisterView.as_view(), name='register_employee'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]