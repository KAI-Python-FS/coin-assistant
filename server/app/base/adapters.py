from typing import Any

from django.http.request import QueryDict


def query_parameters_to_dict(query_dict: QueryDict) -> dict[str, Any]:
    """Возвращает словарь параметров, переданных в запросе"""
    return {
        key: value
        for key, value in query_dict.items()
    }
