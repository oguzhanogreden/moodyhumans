from django.urls import path

from . import views

app_name = "measurements"
urlpatterns = [
    path(
        "finished/", views.MeasurementFinishedView.as_view(), name="finished"
    ),  # should remain above StartMeasurement
    path("<str:name>/history", views.MeasurementHistoryView.as_view(), name="history"),
    path("<str:name>/start", views.StartMeasurementView.as_view(), name="start"),
    path(
        "m<int:session_id>/<str:name>/<int:item>/",
        views.MeasurementItemView.as_view(),
        name="item",
    ),
]
