from django.urls import path

from .apis import (
    BalanceCurrentView,
    CategoryGeneralView,
    CategoryConcreteView,
    OperationGeneralView,
    OperationConcreteView,
)


category_patterns = [
    path("", CategoryGeneralView.as_view(), name="category"),
    path("<int:category_id>", CategoryConcreteView.as_view(), name="concrete_category"),
]

operation_patterns = [
    path("", OperationGeneralView.as_view(), name="operation"),
    path("<int:operation_id>", OperationConcreteView.as_view(), name="concrete_operation"),
]

balance_patterns = [
    path("", BalanceCurrentView.as_view(), name="balance-current"),
]
