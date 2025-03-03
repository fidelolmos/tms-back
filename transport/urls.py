from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectionViewSet, OrderViewSet, RouteViewSet, TMSViewSet

router = DefaultRouter()
router.register(r'directions', DirectionViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'tms', TMSViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
