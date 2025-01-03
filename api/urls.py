from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlideViewSet, DeckViewSet

router = DefaultRouter()
router.register(r'slides', SlideViewSet, basename='slide')
router.register(r'decks', DeckViewSet, basename='deck')

urlpatterns = [
    path('', include(router.urls)),
] 