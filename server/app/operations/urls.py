from django.urls import path

from .apis import ListCreateCategoryView


category_patterns = [
    path("", ListCreateCategoryView.as_view(), name="category")
]
