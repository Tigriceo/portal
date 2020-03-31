from django.urls import path

from . import views

urlpatterns = [
    path("", views.OrderListView.as_view(), name="home"),
    path("search/", views.SearchOrderView.as_view(), name='search'),
    path("add/", views.CreateOrderView.as_view(), name='add_order'),
    path("myzapros/", views.MyOrderListView.as_view(), name="my_order"),
    path("order/<int:pk>/", views.MakeAnOfferView.as_view(), name="order"),
    path("my_offer/", views.MyOfferListView.as_view(), name="my_offer"),
    path("my_offer/<int:pk>", views.MyOfferInView.as_view(), name="my_offer_in"),
    path("myzapros/<int:pk>", views.ListOfferView.as_view(), name="offer_list"),
    path("inactive/<str:sort>", views.InactiveView.as_view(), name="inactive"),

    path("category/<str:slug>/", views.CategoryDetailView.as_view(), name="category"),

]