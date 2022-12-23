from dataclasses import dataclass


@dataclass
class BalanceDetailedByCategoriesCategoryItem:
    """Дата-класс детализированных данных об одной категории баланса пользователя"""

    category_id: str
    category_name: str
    total: float


@dataclass
class BalanceDetailedByCategories:
    """Дата-класс сводных детализированных данных баланса пользователя"""

    spending: list[BalanceDetailedByCategoriesCategoryItem]
    refill: list[BalanceDetailedByCategoriesCategoryItem]
    balance: float
