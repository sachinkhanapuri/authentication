from django.urls import path
from gpsapp import views

# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title='vehicle objects')



urlpatterns = [

    path('vehicle/',views.vehicle_view.as_view(),name='allvehicle'),



]


