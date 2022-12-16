from django.urls import path

from .apis import CategoryGeneralView, CategoryConcreteView


category_patterns = [
    path("", CategoryGeneralView.as_view(), name="category"),
    path("<int:category_id>", CategoryConcreteView.as_view(), name="concrete_category"),
]
