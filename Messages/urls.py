from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Messages.api.views import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
