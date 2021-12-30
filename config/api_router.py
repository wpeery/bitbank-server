from django.conf import settings
from rest_framework import routers

from bitbank.users.api import views as user_views
from bitbank.transfer.api import views as transfer_views

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register("users", user_views.UserViewSet)
router.register("transfer", transfer_views.TransferViewSet, basename="transfer")


app_name = "api"
urlpatterns = router.urls
