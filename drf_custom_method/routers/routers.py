from rest_framework.routers import (
    Route,
    DynamicRoute,
    SimpleRouter,
    DefaultRouter,
    escape_curly_brackets,
)
from rest_framework_nested.routers import NestedSimpleRouter, NestedDefaultRouter


# Custom Method Routers
# =============================================================================
custom_method_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    DynamicRoute(
        url=r"^{prefix}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    Route(
        url=r"^{prefix}/{lookup}{trailing_slash}$",
        mapping={
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        },
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    DynamicRoute(
        url=r"^{prefix}/{lookup}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


class CustomMethodMixin:
    def _get_dynamic_route(self, route, action):
        initkwargs = route.initkwargs.copy()
        initkwargs.update(action.kwargs)

        url_path = escape_curly_brackets(action.url_path)
        slash = action.slash  # here

        return Route(
            url=route.url.replace("{url_path}", url_path).replace(
                "{slash}", slash
            ),  # here
            mapping=action.mapping,
            name=route.name.replace("{url_name}", action.url_name),
            detail=route.detail,
            initkwargs=initkwargs,
        )


class CustomMethodSimpleRouter(CustomMethodMixin, SimpleRouter):

    routes = custom_method_routes


class CustomMethodDefaultRouter(CustomMethodMixin, DefaultRouter):

    routes = custom_method_routes


# Nested Singleton Resource Custom Method Routers
# =============================================================================
sub_resource_singleton_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update",},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    DynamicRoute(
        url=r"^{prefix}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


class NestedSingletonResourceCustomMethodSimpleRouter(
    CustomMethodMixin, NestedSimpleRouter
):

    routes = sub_resource_singleton_routes


class NestedSingletonResourceCustomMethodDefaultRouter(
    CustomMethodMixin, NestedDefaultRouter
):

    routes = sub_resource_singleton_routes
