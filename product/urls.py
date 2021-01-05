from django.urls import path
from . import views
from .views import search

urlpatterns = [
    path('detail/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('', views.ItemDetailView.as_view(), name='item-detail'),
    path('add-to-cart', views.AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-wish', views.AddToWishView.as_view(), name='add-to-wish'),
    path('checkout', views.Checkout.as_view(), name='checkout'),
    path('add-comment/<int:id>', views.addcomment, name='add-comment'),
    path('cat-list/<cat>', views.cat_filter, name='cat-list'),
    path('command-review/<cat>', views.comment_filter, name='command-list'),
    path('newsletter/',views.newsletter, name = 'newsletter'),
    path('paginator/<int:id>', views.comment_show, name='paginator'),


]
