from typing import Iterable, Any, Dict, List, Callable


def filter_an(subjects: Iterable[Any], filter_func: Callable) -> list:
    """Фильтрует итерируемый объект subjects при помощи функции фильтрации filter_func"""
    return list(filter(lambda subject: not filter_func(subject), subjects))


def replace_in(subjects: Iterable[str], replace_dict: Dict[str, str]) -> List[str]:
    """Заменяет значения в итерируемом объекте subjects на значение replace_dict[key],
    если key встречается в subjects. Совпадение с key фиксируется, если key является 
    началом элемента subjects.
    Если для одного ключа встречается несколько совпадений, то в результируещем 
    списке останется только одно замененое вхождение.
    """
    for i in range(0, len(subjects) - 1):
        for key, value in replace_dict.items():
            if subjects[i].startswith(key):
                subjects[i] = value
    
    return list(set(subjects))


def split_by(n: int, text: str) -> list:
    """Разбивает строку text по n символов"""
    return [text[i:i+n] for i in range(0, len(text), n)]