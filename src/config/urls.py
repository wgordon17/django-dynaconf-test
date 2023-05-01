from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path  # , re_path
from django.views.generic import TemplateView

from src.shared import views as error_views
from src.tailwind_theme.views import design_testing_view

handler400 = "src.shared.views.bad_request"
handler403 = "src.shared.views.permission_denied"
handler404 = "src.shared.views.page_not_found"
handler500 = "src.shared.views.server_error"


# TODO: Make projects view _without_ the /projects/, so just /<org>/<project>/
# TODO: Ensure ALL top level URLs are included in the "not allowed" list for usernames
# TODO: Ensure that organization creation _also_ follows the same restrictions as usernames
# TODO: Add a safety startup check to prevent Django
#  from starting if any _existing_ organization names conflict with top level URLs


urlpatterns = [
    path("", include("src.apps.marketing.urls", namespace="marketing")),
    # TODO: validate that two_factor login supersedes allauth login URLs
    path("", include("src.apps.authentication.urls", namespace="authentication")),
    # TODO: remove after https://github.com/pennersr/django-allauth/issues/3306 is resolved
    # This is only here to account for hard-coded `reverse` values in allauth
    path("", include("src.apps.authentication.allauth_urls")),
    # path("", include("allauth.urls")),
    # Search
    path("search/", include("src.apps.search.urls", namespace="search")),
    # Projects
    # path("projects/", view=project_views.project_redirect_view, name="projects-home"),
    # re_path(r"(?:(?P<organization>[-a-z0-9]+)/)?projects/", include("src.apps.projects.urls", namespace="projects")),
    # path("<str:organization>/projects/", include("src.apps.projects.urls", namespace="projects")),
    # # Organizations
    # path("organizations/", include("src.apps.organizations.urls", namespace="organizations")),
    # # # Billing
    # path("<str:organization>/billing/", include("src.apps.billing.urls", namespace="billing")),
    # # # Preferences
    # path("<str:organization>/preferences/", include("src.apps.preferences.urls", namespace="preferences")),
    # # Payment
    # path("<str:organization>/payment/", include("djstripe.urls", namespace="djstripe")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path("form-test/", design_testing_view),
        path("400/", error_views.bad_request),
        path("403/", error_views.permission_denied),
        path("404/", error_views.page_not_found),
        path("429/", TemplateView.as_view(template_name="429.html")),
        path("500/", error_views.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns = [path("__debug__/", include("debug_toolbar.urls")), *urlpatterns]
