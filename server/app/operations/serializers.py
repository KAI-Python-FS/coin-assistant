import datetime

from pydantic import BaseModel, validator

from .enums import OperationTypeEnum


class BaseCategorySerializer(BaseModel):
    """Сериализатор всех данных одной категории"""

    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryRetrieveOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных получения одной категории"""


class CategoryListItemOutputSerializer(BaseCategorySerializer):
    """Сериализатор получения списка Категорий"""


class CategoryCreateInputSerializer(BaseModel):
    """Сериализатор входящих данных создания Категории"""

    name: str


class CategoryCreateOutputSerializer(BaseCategorySerializer):
    """Сериализатор исходящих данных создания Категории"""


class CategoryUpdateInputSerializer(BaseModel):
    """Сериализатор входящих данных обновления Категории"""

    name: str


class CategoryUpdateOutputSerializer(BaseCategorySerializer):
    """Сериалиазатор исходящих данных обновления Категории"""


class BaseOperationSerializer(BaseModel):
    """Сериализатор всех данных одной операции"""

    id: int
    name: str
    description: str | None
    operation_at: datetime.datetime | None
    operation_type: OperationTypeEnum
    cost: float
    category: BaseCategorySerializer | None

    class Config:
        orm_mode = True


class OperationCreateInputSerializer(BaseModel):
    """Сериализатор входящих данных создания Операции пользователя"""

    name: str
    description: str | None
    operation_at: datetime.datetime | None
    operation_type: OperationTypeEnum
    cost: float
    category: int | None


class OperationCreateOutputSerializer(BaseOperationSerializer):
    """Сериализатор исходящих данных создания Операции пользователя"""


class OperationListFilterSerializer(BaseModel):
    """Сериализатор фильтров списка Операций пользователя"""

    by_operation_type: OperationTypeEnum | None
    by_categories: list[int] | None
    by_operation_start_date: datetime.datetime | None
    by_operation_finish_date: datetime.datetime | None


class OperationListItemOutputSerializer(BaseOperationSerializer):
    """Сериалиазатор исходящих данных получения списка Операций пользователя"""


class OperationRetrieveOutputSerializer(BaseOperationSerializer):
    """Сериализатор исходящих данных получения одной Операции"""


class OperationUpdateInputSerializer(BaseModel):
    """Сериализатор входящих данных обновления одной Операции"""

    name: str | None
    description: str | None
    cost: float | None
    date: datetime.datetime | None
    category: int | None


class BalanceDetailedCategoryOutputSerializer(BaseModel):
    """Сериализатор исходящих детализированных данных по одной Категории"""

    category_id: int | None
    category_name: str | None
    total: float

    @validator("total")
    def round_total(cls, v):
        """Округляет баланс"""
        return round(v, 2)


class BalanceDetailedOutputSerializer(BaseModel):
    """Сериализатор исходящих детализированных данных о текущем балансе пользователя"""

    spending: list[BalanceDetailedCategoryOutputSerializer]
    refill: list[BalanceDetailedCategoryOutputSerializer]
    balance: float

    @validator("balance")
    def round_balance(cls, v):
        """Округляет баланс"""
        return round(v, 2)
