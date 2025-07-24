from django.urls import path

from . import views

app_name = "songs"

urlpatterns = [
    path("create/", views.song_create, name="create"),
    path(
        "detail/<int:id>/<slug:slug>/",
        views.song_detail,
        name="detail",
    ),
    path("like/", views.song_like, name="like"),
    path("", views.song_list, name="list"),
    path(
        "<int:pk>/edit/",
        views.song_edit,
        name="edit",
    ),
    path("<int:pk>/delete/", views.song_delete, name="delete"),
    path("<int:pk>/add-to-spotify/", views.song_add_to_spotify, name="add_to_spotify"),
    path("ranking/", views.song_ranking, name="ranking"),
]
