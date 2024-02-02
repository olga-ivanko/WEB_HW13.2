from django.urls import path
from . import views

app_name = "quotesapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("tag/", views.tag, name="tag"),
    path("author/", views.author, name="author"),
    path("quote/", views.quote, name="quote"),
    path("author/<str:author_name>/", views.about_author, name="about_author"),
    path("quote/<int:quote_id>/", views.quote_detail, name="quote_detail"),
]
