from django.urls import path

from menu.views import IndexPageView


urlpatterns = [
    path("", IndexPageView.as_view(), name="index")
]
