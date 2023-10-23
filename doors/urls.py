from rest_framework import routers

from doors.views import DoorViewSet

app_name = 'doors'

router = routers.SimpleRouter()
router.register(r'doors', DoorViewSet)
urlpatterns = router.urls