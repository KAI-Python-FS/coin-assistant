from typing import Any

from django.http.request import QueryDict


def query_parameters_to_dict(
    query_dict: QueryDict, list_params: list[str] | tuple[str] | None = None
) -> dict[str, Any | None]:
    """
    Возвращает словарь параметров, переданных в запросе.

    При проектировании приложения было допущено,
    что возможна фильтрация по nullable-полю.

    Напрямую null нельзя передать в query-параметрах, поэтому для фильтрации значений по null
    нужно передавать пустую строку.
    """
    if not list_params:
        list_params = []

    params_as_dict = {}
    for each_key, each_value in query_dict.items():
        if each_key in list_params:
            query_parameter_value = (
                query_dict.getlist(each_key) if each_value else None
            )
        else:
            query_parameter_value = each_value  # type: ignore

        params_as_dict[each_key] = query_parameter_value

    return params_as_dict
