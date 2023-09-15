from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("listCategory",views.listCategory,name="listCategory"),
    path("clickCategory/<str:type>",views.clickCategory,name="clickCategory"),
    path("removeWatchList/<int:id>",views.removeWatchList,name="remove"),
    path("addwatchList/<int:id>",views.addWatchList,name="add"),
    path("close/<int:id>",views.closeList,name="closeList"),
    path("placeBid/<int:id>",views.placeBid,name="placeBid"),
    path("watchlist",views.displayWatchList,name="watchlist"),
    path("comments/<int:id>",views.postComments,name="comments"),
    path("notifications",views.notifications,name="notifications")
]
