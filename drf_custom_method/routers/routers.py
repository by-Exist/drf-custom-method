from rest_framework.routers import SimpleRouter, DefaultRouter
from .mixins import CustomMethodMixin, NestedMixin
from .routes import custom_method_default_routes, sub_resource_singleton_routes


# TODO: Add doc string


# Custom Method
class CustomMethodSimpleRouter(CustomMethodMixin, SimpleRouter):
    routes = custom_method_default_routes


class CustomMethodDefaultRouter(CustomMethodMixin, DefaultRouter):
    routes = custom_method_default_routes


# Nested + Custom Method
class NestedCustomMethodSimpleRouter(NestedMixin, SimpleRouter):
    routes = custom_method_default_routes


class NestedCustomMethodDefaultRouter(NestedMixin, DefaultRouter):
    routes = custom_method_default_routes


# Nested + Custom Method + Singleton Resource
class NestedSingletonResourceCustomMethodSimpleRouter(NestedCustomMethodSimpleRouter):
    routes = sub_resource_singleton_routes


class NestedSingletonResourceCustomMethodDefaultRouter(NestedCustomMethodDefaultRouter):
    routes = sub_resource_singleton_routes
