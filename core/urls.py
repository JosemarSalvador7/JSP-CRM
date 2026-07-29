from django.contrib import admin
from django.urls import path, include

# media archive
from django.conf.urls.static import static
from django.conf import settings

# internacionalization
from django.conf.urls.i18n import i18n_patterns

import dashboard
import dashboard.views

urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("contacts/", include("contacts.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("interactions/", include("interations.urls")),
    path("task/", include("task.urls")),
    path("opportunities/", include("opportunities.urls")),
    path("", dashboard.views.home_view),
)
