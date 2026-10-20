from django.urls import path

from modules.seo.api.views import PageSeoView

urlpatterns = [path("", PageSeoView.as_view())]
