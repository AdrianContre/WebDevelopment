
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost",views.newPost,name="newPost"),
    path("profile/<int:userId>",views.profile,name="profile"),
    path("follow",views.follow,name="follow"),
    path("unfollow",views.unfollow,name="unfollow"),
    path("following",views.following,name="following"),
    path("editPost/<int:postId>",views.editPost,name="editPost"),
    path("increaseLike/<int:postId>",views.increaseLike,name="increaseLike"),
    path("decreaseLike/<int:postId>",views.decreaseLike,name="decreaseLike")
]
