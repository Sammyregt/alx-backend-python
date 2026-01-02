from django.urls import path, include
# from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path("", include(router.urls)),
]