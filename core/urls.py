from django.contrib import admin
from django.urls import path

from .swagger_schema import schema_view


urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger API documentation
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "swagger/api.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
