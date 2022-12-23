import pytest

from server.app.goals.models import Goal
from tests.factories.goals import BudgetFactory, GoalRefillFactory


class TestGoalManager:
    """Проверка работы менеджера"""

    @pytest.mark.django_db()
    def test_goal_queryset(self):
        """Тест проверки получения целей накопления"""
        budgets, goal_refills = (
            BudgetFactory.create_batch(size=3),
            GoalRefillFactory.create_batch(size=4),
        )

        actual_goals = Goal.objects.goals().count()

        assert actual_goals == len(goal_refills)
