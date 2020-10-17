"""NeVerimAbime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import api
from api.ingredient.views import nutrient_view
from api.views import CustomAuthToken, MeViewSet, UserViewSet
from api.views import UserViewSet as userview
from .views import loginPage as loginPage, view_login, home
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view

#
# schema_view = get_swagger_view(title='NeVerimAbime API')

schema_view = get_schema_view(
    openapi.Info(
        title="NeVerimAbime API",
        default_version='v1',
        description="BOUN SWE 573 Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="keremocakoglu@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('home/', home, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # for login page
    path('', loginPage, name='loginPage'),
    path('login/', view_login, name="login"),
    # todo after succesfully inserting new datas redirect other url
    url(r'^registration/', include('rest_auth.registration.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    path('api/v1/me/', MeViewSet.as_view({'get': 'retrieve'}), name='me'),
    path('api/v1/auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    # override sjwt stock token
    path('api/v1/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/", include('api.urls')),
    path("api/ingredientsearch/", nutrient_view, name='nutrient_view'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/users/getusers/', userview.getusers, name='profile-list'),
    url('documentation/', schema_view),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
