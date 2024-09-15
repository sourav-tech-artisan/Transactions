from app.apps.transactions.views import TransactionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls