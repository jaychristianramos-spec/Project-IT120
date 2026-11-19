
from django.urls import path

from . import views

app_name = "sms_app"

urlpatterns = [
    # Send SMS
    path("", views.send_sms_view, name="send"),

    # View message history
    path("history/", views.history_view, name="history"),

    # Refresh SMS delivery status
    path(
        "history/<int:pk>/refresh/",
        views.refresh_status_view,
        name="refresh"
    ),

    # Delete SMS record
    path(
        "history/<int:pk>/delete/",
        views.delete_sms_view,
        name="delete"
    ),
]
