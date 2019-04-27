from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gear import views


router = DefaultRouter()
router.register('items', views.ItemViewSet)

app_name = 'gear'

urlpatterns = [
    path('', include(router.urls))
]
