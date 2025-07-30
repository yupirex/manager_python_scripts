# check_universal_env.py

import sys
import os
import platform
import subprocess
import time

from commons.conf_util import get_or_create_config, print_section_header 

try:
    import tkinter as tk
    from tkinter import messagebox
    tkinter_available = True
except ImportError:
    tkinter_available = False
    print("Внимание: Модуль 'tkinter' не найден. Тест GUI будет пропущен.")
except Exception as e:
    tkinter_available = False
    print(f"Внимание: Ошибка при импорте 'tkinter': {e}. Тест GUI будет пропущен.")

# Добавляем импорт requests
try:
    import requests
    requests_available = True
except ImportError:
    requests_available = False
    print("Внимание: Модуль 'requests' не найден. Сетевой тест будет пропущен.")
except Exception as e:
    requests_available = False
    print(f"Внимание: Ошибка при импорте 'requests': {e}. Сетевой тест будет пропущен.")


def run_system_info():
    """Выводит базовую информацию о системе."""
    print_section_header("Информация о системе")
    print(f"Операционная система: {platform.system()} ({platform.release()})")
    print(f"Архитектура: {platform.machine()}")
    print(f"Версия Python: {sys.version.splitlines()[0]}")
    print(f"Путь к исполняемому файлу Python: {sys.executable}")
    print(f"Рабочая директория: {os.getcwd()}")
    print(f"Переменная PATH: {os.environ.get('PATH', 'Не определена')}")
    print(f"Переменная DISPLAY (для GUI): {os.environ.get('DISPLAY', 'Не определена')}")

def run_import_test():
    """Проверяет импорт основных и некоторых сторонних модулей."""
    print_section_header("Тест импорта модулей")
    modules_to_test = [
        'math', 'json', 'os', 'sys', 'time', 'datetime', 'random',
        'collections', 're', 'logging', 'subprocess', 'threading',
        'http.client', 'urllib.request', 'hashlib', 'sqlite3', 'xml.etree.ElementTree',
        'configparser',
        'requests' # Добавляем requests в список для проверки
    ]
    
    success_count = 0
    fail_count = 0

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ Успешно импортирован: {module_name}")
            success_count += 1
        except ImportError:
            print(f"  ❌ НЕ удалось импортировать: {module_name}")
            fail_count += 1
        except Exception as e:
            print(f"  ⚠️ Ошибка при импорте {module_name}: {e}")
            fail_count += 1

    print(f"\nИмпорты завершены. Успешно: {success_count}, Неудачно: {fail_count}")

def run_gui_test():
    """Проверяет работу Tkinter GUI."""
    print_section_header("Тест GUI (Tkinter)")
    if not tkinter_available:
        print("  Тест GUI пропущен, так как модуль 'tkinter' недоступен.")
        print("  (Возможно, Python установлен без Tkinter или он не включен в дистрибутив).")
        return

    if platform.system() == "Linux" and "DISPLAY" not in os.environ:
        print("  ❌ GUI тест: Переменная окружения 'DISPLAY' не установлена.")
        print("  Для работы GUI в Linux (включая Docker-контейнеры) требуется запущенный X-сервер и настройка 'DISPLAY'.")
        print("  Это нормальное поведение для базовых Docker-контейнеров без GUI.")
        return

    try:
        root = tk.Tk()
        root.title("Тест GUI")
        root.geometry("400x150")
        
        root.withdraw()
        
        if platform.system() == "Windows" or platform.system() == "Darwin":
            root.attributes('-topmost', True)
            root.after(100, lambda: root.attributes('-topmost', False))
            root.deiconify()

        messagebox.showinfo(
            "Тест GUI",
            "Это тестовое окно Tkinter.\n"
            "Если вы видите это сообщение, значит, GUI работает!"
        )
        print("  ✅ Tkinter GUI тест: Окно сообщения должно было появиться.")
        
    except tk.TclError as e:
        print(f"  ❌ Tkinter GUI тест: Ошибка Tkinter/Tcl: {e}")
        if "no display name" in str(e).lower() or "can't connect to display" in str(e).lower():
            print("  Вероятно, X-сервер не запущен или 'DISPLAY' не настроен корректно.")
        print("  Убедитесь, что GUI-библиотеки установлены (например, 'python3-tk' в Debian/Ubuntu).")
    except Exception as e:
        print(f"  ❌ Tkinter GUI тест: Неизвестная ошибка - {e}")
    finally:
        if 'root' in locals() and root.winfo_exists():
            root.destroy()
        print("  Тест GUI завершен.")

def run_network_test():
    """Проверяет базовую сетевую функциональность с помощью requests."""
    print_section_header("Тест сети (Requests)")
    if not requests_available:
        print("  Тест сети пропущен, так как модуль 'requests' недоступен.")
        print("  Убедитесь, что он установлен (pip install requests).")
        return

    try:
        print("  Попытка выполнить GET-запрос к Google.com...")
        response = requests.get("https://www.google.com", timeout=10)
        print(f"  ✅ Успешно получен ответ от Google.com (статус: {response.status_code})")
        print(f"  Размер ответа: {len(response.content)} байт.")
    except requests.exceptions.ConnectionError:
        print("  ❌ Ошибка соединения: не удалось подключиться к удаленному хосту.")
        print("  Возможно, нет доступа к интернету из контейнера или проблема с DNS.")
    except requests.exceptions.Timeout:
        print("  ❌ Ошибка таймаута: запрос занял слишком много времени.")
        print("  Возможно, медленное соединение или удаленный хост недоступен.")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Общая ошибка запроса: {e}")
    except Exception as e:
        print(f"  ❌ Неизвестная ошибка при сетевом тесте: {e}")
    finally:
        print("  Тест сети завершен.")


if __name__ == "__main__":
    run_system_info()
    run_import_test()
    run_gui_test()
    
    my_app_config = get_or_create_config("app_config.ini") 
    
    run_network_test() # Вызываем новый сетевой тест

    print(f"\n{'='*60}")
    print(f"Все тесты завершены.".center(60))
    print(f"{'='*60}")

    if platform.system() == "Windows":
        input("Нажмите Enter для выхода...")
    else:
        pass