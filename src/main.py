import argparse
import csv
from os import PathLike
import pathlib

from typing import Iterable, Dict
from collect import SysInfo, AppCollector, get_mac
from options import UNNECESSARY_APPS, APPS_TO_REPLACE, CSV_HEADERS


# def in_args(args, *keys) -> bool:
#     for key in keys:
#         if key in args:
#             return True
#     return False

# def parse_console() -> Dict:
#     if in_args(args, "-u", "--unit"):
#         pass
#     elif in_args(args, "-c", "--cabinet"):
#         pass
#     elif in_args(args, "-d", "--department"):
#         pass
#     elif in_args(args, "-i", "--inventory_num"):
#         pass
#     elif in_args(args, "-a", "--arm_type"):
#         pass


def create_default_parser():
    parser = argparse.ArgumentParser(
        description="Собирает информацию о системе и записывает её в csv файл",
    )
    parser.add_argument("filepath", help="Путь к csv файлу для записи")
    parser.add_argument("-u", "--unit", nargs="?", default="", help="Подразделение")
    parser.add_argument("-c", "--cabinet", nargs="?", default="", help="Кабинет")
    parser.add_argument("-a", "--arm_type", nargs="?", default="", help="Тип АРМ")
    parser.add_argument("-d", "--department", nargs="?", default="", help="Отдел/кафедра")
    parser.add_argument("-i", "--inventory_num", nargs="?", default="", help="Инвентарный номер")
    return parser


def create_csv(filepath: pathlib.Path) -> bool:
    """Создаёт файл по пути filepath. Если файл был создает, то возвращает True, иначе False"""
    if not filepath.exists():
        with open(filepath, "w", encoding="utf-8") as f:
            return True
    return False


if __name__ == "__main__":
    parser = create_default_parser()
    args = vars(parser.parse_args())
    ac = AppCollector(UNNECESSARY_APPS, APPS_TO_REPLACE)
    apps = ac.get_apps()
    mac = get_mac()
    print(args)
    info = SysInfo(
        unit=args["unit"],
        cabinet=args["cabinet"],
        department=args["department"],
        mac=mac,
        inv_num=args["inventory_num"],
        arm_type=args["arm_type"],
        software=apps,
        periphery="",
        conn_type="",
    )

    path = pathlib.Path(args["filepath"])
    is_created = create_csv(path)
    with open(path, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_created:
            writer.writerow(CSV_HEADERS)
        info.write_to_csv(f)
