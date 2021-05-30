from rest_framework.routers import (
    Route,
    DynamicRoute,
    SimpleRouter,
    DefaultRouter,
    escape_curly_brackets,
)


custom_method_routes = [
    # List route
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
    # Detail route
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
    """
    Custom Method 라우터에 필요한 믹스인.
    utils.decorators 내의 slash_editable_action 함수에 종속적이다.
    """

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
    """
    Custom Method 기능이 추가된 SimpleRouter.
    utils.decorators 내의 slash_editable_action에 종속적이다.
    """

    routes = custom_method_routes


class CustomMethodDefaultRouter(CustomMethodMixin, DefaultRouter):
    """
    Custom Method 기능이 추가된 DefaultRouter.
    utils.decorators 내의 slash_editable_action에 종속적이다.
    """

    routes = custom_method_routes
