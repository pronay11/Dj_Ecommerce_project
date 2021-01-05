from django.urls import path
from . import views


urlpatterns = [
    path('remove-cart-item/<int:cart_item_id>', views.RemoveFromCartView.as_view(), name='remove-cart-item'),
    path('remove-wish-item/<int:wish_item_id>', views.RemoveFromWishView.as_view(), name='remove-wish-item'),
    path('search-item/', views.SearchProductView.as_view()),
    path('create-item/', views.CreateProductView.as_view()),
    path('create-category/', views.CreateCategoryAPI.as_view()),
    path('update-category/<int:cid>/', views.UpdateCategoryApi.as_view()),
    path('test', views.TestAuth.as_view()),
    path('get-stripe-session/', views.CreateStripeSession.as_view()),
]