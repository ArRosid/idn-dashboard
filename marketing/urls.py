from django.urls import path
from marketing.views import (
    InteraksiListView,
    createInteraksi,
    editInteraksi,
    delete_interaksi,
    interaksi_bulanan,
)

app_name = "marketing"

urlpatterns = [
    path("list_interaksi/", InteraksiListView.as_view(), name="list_interaksi"),
    path("add_interaksi/", createInteraksi, name="add_interaksi"),
    path("edit_interaksi/<int:pk>/", editInteraksi, name="edit_interaksi"),
    path("delete_interaksi/<int:pk>/", delete_interaksi, name="delete_interaksi"),
    path("interaksi_bulanan/", interaksi_bulanan, name="interaksi_bulanan"),
]
