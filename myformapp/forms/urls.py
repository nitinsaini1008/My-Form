from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
urlpatterns = [
	path("create/", CreateForm.as_view(), name="create-form"),
	path("get-form/<slug:uuid>/", GetFormData.as_view(), name="get-form"),
	path("response-form/<slug:uuid>/", SaveResponseForm.as_view(), name="save-response"),
	path("get-responses/<slug:uuid>/", ResponseListView.as_view(), name='get-responses'),
	path("get-response/<int:id>/", ResponseDetailView.as_view(), name='get-response-detail'),
]