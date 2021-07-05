import csv
import winreg

import collect_util as cutil

from uuid import getnode


class SysInfo:
    """
    Используется для храниния собранной информации о системе.
    """

    def __init__(
            self,
            unit="",
            cabinet="",
            department="",
            mac="",
            inv_num="",
            arm_type="",
            software="",
            periphery="",
            conn_type="",
        ):
            self.unit = unit
            self.cabinet = cabinet
            self.department = department
            self.mac = mac
            self.inv_num = inv_num
            self.arm_type = arm_type
            self.software = software
            self.periphery = periphery
            self.conn_type = conn_type

    def write_to_csv(self, file):
        """Принимает на вход file-like объект и пишет в него
        состояние объекта SysInfo в формате csv."""
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow((
            self.unit,
            self.cabinet,
            self.department,
            self.mac,
            self.inv_num,
            self.arm_type,
            self.software,
            self.periphery,
            self.conn_type,
        ))


class AppCollector:
    
    """
    Статический класс для инкапсуляции кода получения списка приложений
    установленных на компьютере при помощи поиска в регистре Windows
    """

    REGISTRY_SUB_KEYS = (
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
    )

    def __init__(self, blacklist, replace_dict):
        self._blacklist = blacklist
        self._replace_dict = replace_dict

    def _get_apps_from_reg(self):
        app_names = set()
        
        for sub_key in self.REGISTRY_SUB_KEYS:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, access=winreg.KEY_READ)
            subkeys_count = winreg.QueryInfoKey(key)[0]
            for i in range(0, subkeys_count - 1):
                try:
                    key_name = winreg.EnumKey(key, i)
                    key_path = sub_key + "\\" + key_name
                    each_key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        key_path,
                        access=winreg.KEY_READ
                    )
                    app_name, _ = winreg.QueryValueEx(each_key, "DisplayName")
                    app_names.add(app_name)
                except WindowsError:
                    pass

        return list(app_names)

    def _is_in_blacklist(self, app):
        for unnecessary in self._blacklist:
            if app.startswith(unnecessary):
                return True

    def get_apps(self) -> list:
        """ ищет приложения установленные на компьютере и возвращает список строк
        с именами приложений"""
        apps = self._get_apps_from_reg()
        apps = cutil.filter_an(apps, self._is_in_blacklist)
        apps = cutil.replace_in(apps, self._replace_dict)
        apps = sorted(apps)
        return apps


"""возвращает MAC адрес eth0 в формате 00-00-00-00-00-00"""
def get_mac() -> str:
    mac = getnode()
    mac = f"0x{mac:X}"
    mac = mac[2:]
    mac = cutil.split_by(2, mac)
    mac = "-".join(mac)
    return mac


"""пишет собранные данные в указаный файл"""
def write_to_csv(filename, info: SysInfo):
    with open(filename, "a") as f:
        info.write_to_csv(f)


# if __name__ == "__main__":
#     mac = get_mac()
#     apps = get_apps()
#     # os.system("wmic printer list brief")
#     print(subprocess.getoutput("wmic printer list brief"))
#     print("MAC: ", mac)
