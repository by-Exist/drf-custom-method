from rest_framework.routers import Route, escape_curly_brackets
from rest_framework_nested.routers import NestedMixin


# TODO: add work - check action is "slash_editable_action"


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
