from rest_framework.decorators import MethodMapper, pretty_name
from rest_framework.decorators import action


def slash_editable_action(
    methods=None,
    detail: bool = None,
    slash: str = "/",  # here
    url_path: str = None,
    url_name: str = None,
    **kwargs
):
    """
    Custom Method 기능을 활용하기 위해 기존 action을 확장한 개념의 action 함수.
    slash 파라미터가 추가되었다.
    """
    methods = ["get"] if (methods is None) else methods
    methods = [method.lower() for method in methods]

    assert detail is not None, "@action() missing required argument: 'detail'"

    if "name" in kwargs and "suffix" in kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def decorator(func):
        func.mapping = MethodMapper(func, methods)

        func.detail = detail
        func.url_path = url_path if url_path else func.__name__
        func.url_name = url_name if url_name else func.__name__.replace("_", "-")
        func.slash = slash  # here
        func.kwargs = kwargs

        if "name" not in kwargs and "suffix" not in kwargs:
            func.kwargs["name"] = pretty_name(func.__name__)
        func.kwargs["description"] = func.__doc__ or None

        return func

    return decorator
