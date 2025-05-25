from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('content/', include('content.urls')),
    path('content/', include('content.additional_urls')),
    path('payments/', include('payments.urls')),
    path('admin-panel/', include('accounts.additional_urls')),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/content/', include('content.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'
