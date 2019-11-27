from django.urls import path, include
from rest_framework import routers

from .views import PaymentViewSet, AccountViewSet


router = routers.DefaultRouter()
router.register(r'payment', PaymentViewSet)
router.register(r'accounts', AccountViewSet, basename='accounts')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls))
]