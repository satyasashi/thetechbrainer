from django.contrib import admin
from django.urls import path, include
from thetechbrainer.settings import dev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('siteuser.urls')),
    path('blog/', include('blog.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if dev.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
