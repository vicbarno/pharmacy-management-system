from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, PatientViewSet, SaleViewSet, SaleItemViewSet

router = DefaultRouter()
router.register('medicines', MedicineViewSet)
router.register('patients', PatientViewSet)
router.register('sales', SaleViewSet)
router.register('sale-items', SaleItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]