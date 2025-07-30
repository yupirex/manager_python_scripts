# config_utils.py

import os
import configparser

def print_section_header(title):
    """Вспомогательная функция для печати заголовка секции."""
    print(f"\n{'='*60}")
    print(f"{title.center(60)}")
    print(f"{'='*60}")

def get_or_create_config(config_filename="config.ini"):
    """
    Проверяет наличие конфигурационного файла.
    Если файл существует, считывает его.
    Если файла нет, создает новый с дефолтными значениями.
    Возвращает объект ConfigParser или None в случае ошибки.
    """
    print_section_header("Тест ConfigParser")
    
    config = configparser.ConfigParser()
    # Получаем абсолютный путь к файлу конфигурации
    # Это важно, чтобы скрипт всегда искал config.ini рядом с собой,
    # независимо от того, из какой директории он запущен.
    #script_dir = os.path.dirname(os.path.abspath(__file__))
    #config_path = os.path.join(script_dir, config_filename)

    if os.path.exists(config_filename):
      print(f"  ✅ Конфигурационный файл '{config_filename}'")
      try:
        config.read(config_filename)
        print("  Содержимое файла:")
        for section in config.sections():
          print(f"    [{section}]")
          for key, value in config.items(section):
            print(f"      {key} = {value}")
        print("  Конфигурация успешно считана.")
        return config
      except configparser.Error as e:
        print(f"  ❌ Ошибка при чтении конфигурационного файла: {e}")
        return None
      except Exception as e:
        print(f"  ❌ Неизвестная ошибка при чтении файла: {e}")
        return None
    else:
      # Задаем дефолтные значения
      config['General'] = {
        'app_name': 'MyUniversalApp',
        'version': '1.0.0',
        'debug_mode': 'True'
      }
      config['Network'] = {
        'server_ip': '127.0.0.1',
        'port': '8080',
        'timeout_seconds': '30'
      }

      try:
        with open(config_filename, 'w') as configfile:
          config.write(configfile)
        print(f"  ✅ Конфигурационный файл '{config_filename}' успешно создан с дефолтными значениями.")
        print("  Пожалуйста, перезапустите скрипт, чтобы увидеть его содержимое.")
        return config # Возвращаем созданный конфиг, хотя он пока пуст для текущего запуска
      except IOError as e:
        print(f"  ❌ Ошибка при создании конфигурационного файла: {e}")
        return None
      except Exception as e:
        print(f"  ❌ Неизвестная ошибка при создании файла: {e}")
        return None
      finally:
        print("  Тест ConfigParser завершен.")

# Пример использования (для самостоятельной проверки config_utils.py)
if __name__ == "__main__":
  print("Запуск config_utils.py напрямую для проверки.")
  my_config = get_or_create_config("test_config.ini")
  if my_config:
    print("\nОбъект конфигурации успешно получен.")
    if my_config.has_section('General'):
      print(f"Имя приложения из конфига: {my_config['General'].get('app_name')}")
  else:
    print("\nНе удалось получить объект конфигурации.")