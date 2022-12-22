from django.urls import path

from . import apis


goal_accumulation_patterns = [
    path("", apis.GoalGeneralView.as_view(), name="goal-accumulation"),
]
