from typing import Any

from django.http.request import QueryDict


def query_parameters_to_dict(query_dict: QueryDict, list_params: list[str] | tuple[str] = None) -> dict[str, Any]:
    """Возвращает словарь параметров, переданных в запросе"""
    if not list_params:
        list_params = []

    return {
        each_key: (
            query_dict.getlist(each_key) if each_key in list_params
            else each_value
        )
        for each_key, each_value in query_dict.items()
    }
