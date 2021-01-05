from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from product.views import HomeView
from product import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('product/', include('product.urls')),
    path('accounts/', include('account.urls')),
    path('count/', include('countdown.urls', namespace='countdown')),
    path('api/', include('api.urls')),
    path('search/', views.search, name="search"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)