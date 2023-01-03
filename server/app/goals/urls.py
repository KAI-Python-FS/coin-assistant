from django.urls import path

from . import apis


goal_accumulation_patterns = [
    path("", apis.GoalRefillGeneralView.as_view(), name="goal-refill"),
    path(
        "<int:goal_id>",
        apis.GoalRefillConcreteView.as_view(),
        name="concrete-goal-refill",
    ),
]

budget_patterns = [
    path("", apis.BudgetGeneralView.as_view(), name="budget"),
    path("<int:budget_id>", apis.BudgetConcreteView.as_view(), name="concrete-budget"),
]
