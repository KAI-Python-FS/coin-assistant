from django.urls import path

from .apis import CreateCategoryView


category_patterns = [
    path("", CreateCategoryView.as_view(), name="category")
]
