
import glob, os, subprocess, sys, zipfile


def find_engine_files():
  """Находит все файлы *_engine.py в папках с префиксом '_'"""
  engine_files = []
  current_dir = os.path.dirname(os.path.abspath(__file__))
  # Поиск папок с префиксом '_'
  pattern = os.path.join(current_dir, '_*')
  for folder in glob.glob(pattern):
    if os.path.isdir(folder):
      # Поиск файлов *_engine.py в каждой папке
      engine_pattern = os.path.join(folder, '*_engine.py')
      for engine_file in glob.glob(engine_pattern):
        engine_files.append(engine_file)
  return engine_files


def extract_zip_archives():
  """Ищет и извлекает ZIP архивы по маске _*.zip, затем удаляет архивы"""
  current_dir = os.path.dirname(os.path.abspath(__file__))
  zip_pattern = os.path.join(current_dir, '_*.zip')
  zip_files = glob.glob(zip_pattern)
  if not zip_files:
    print("ZIP архивы не найдены")
    return
  print(f"Найдено {len(zip_files)} ZIP архивов:")
  for zip_file in zip_files:
    print(f"  - {os.path.basename(zip_file)}")
  for zip_file in zip_files:
    try:
      print(f"Извлечение архива: {os.path.basename(zip_file)}")
      with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(current_dir)
      print(f"  ✅ Архив извлечен успешно")
      # Удаляем архив после успешного извлечения
      os.remove(zip_file)
      print(f"  ✅ Архив удален")
    except zipfile.BadZipFile:
      print(f"  ❌ Ошибка: {os.path.basename(zip_file)} не является корректным ZIP архивом")
    except PermissionError:
      print(f"  ❌ Ошибка: Нет прав для работы с {os.path.basename(zip_file)}")
    except Exception as e:
      print(f"  ❌ Ошибка при обработке {os.path.basename(zip_file)}: {e}")


def run_engines_sequentially():
  """Запускает все engine файлы последовательно с поддержкой интерактивного ввода"""
  engine_files = find_engine_files()
  print(f"Найдено {len(engine_files)} engine файлов:")  
  if not engine_files:
    return
  
  for engine_file in engine_files:
    print(f"  - {engine_file}")
  
  print("\n=== Последовательный запуск engines ===")
  print("Каждый engine будет запущен отдельно для авторизации")
  print("Время для выполнения авторизации engine 10 мин.")
  print("После авторизации всех engines они будут запущены в фоновом режиме")
  print("Нажмите Enter для продолжения или Ctrl+C для выхода...")
  
  try:
    input()
  except KeyboardInterrupt:
    print("\nОтмена запуска")
    return
  
  # Последовательная авторизация каждого engine
  for i, engine_file in enumerate(engine_files, 1):
    print(f"\n--- Запуск {i}/{len(engine_files)}: {os.path.basename(engine_file)} ---")
    print("После успешной авторизации нажмите Ctrl+C чтобы перейти к следующему боту")
    
    # Устанавливаем переменную окружения для режима авторизации
    auth_env = os.environ.copy()
    auth_env['AUTH_ONLY_MODE'] = 'true'
    
    try:
      # Запускаем engine в интерактивном режиме для авторизации
      process = subprocess.Popen(
        [sys.executable, engine_file], 
        cwd=os.path.dirname(engine_file),
        env=auth_env
      )
      
      # Ждем завершения процесса или прерывания пользователем
      try:
        print("Ожидание авторизации... (Нажмите Ctrl+C после авторизации)")
        process.wait()
        print(f"  ✅ {os.path.basename(engine_file)} процесс завершен")
      except KeyboardInterrupt:
        print(f"\n⏹️  Прерывание процесса авторизации для {os.path.basename(engine_file)}")
        process.terminate()
        
        # Проверяем успешность авторизации
        print("Была ли авторизация успешной?")
        while True:
          try:
            confirm = input("Введите 'y' если да, 'n' если нет, 's' чтобы пропустить: ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
              print(f"  ✅ {os.path.basename(engine_file)} отмечен как успешно авторизованный")
              break
            elif confirm in ['n', 'no', 'н', 'нет']:
              print(f"  ❌ {os.path.basename(engine_file)} отмечен как неуспешно авторизованный")
              break
            elif confirm in ['s', 'skip', 'п', 'пропустить']:
              print(f"  ⏭️  {os.path.basename(engine_file)} пропущен")
              break
            else:
              print("Введите 'y' (да), 'n' (нет) или 's' (пропустить)")
          except (KeyboardInterrupt, EOFError):
            print(f"\n⏹️  Пропуск {os.path.basename(engine_file)}")
            break
        
        # Ждем завершения процесса с таймаутом
        try:
          process.wait(timeout=5)
        except subprocess.TimeoutExpired:
          process.kill()
          process.wait()
      
    except Exception as e:
      print(f"  ❌ Ошибка при запуске {os.path.basename(engine_file)}: {e}")
  
  print("\n=== Запуск всех engines в фоновом режиме ===")
  run_all_engines_subprocess()


def run_all_engines_subprocess():
  """Запускает все engine файлы одновременно в отдельных процессах"""
  engine_files = find_engine_files()
  print(f"Найдено {len(engine_files)} engine файлов:")  
  if not engine_files:
    return
  for engine_file in engine_files:
    print(f"  - {engine_file}")
  processes = []
  for engine_file in engine_files:
    try:
      print(f"Запуск процесса для: {os.path.basename(engine_file)}")
      # Запускаем каждый engine в отдельном процессе Python
      process = subprocess.Popen([sys.executable, engine_file], cwd=os.path.dirname(engine_file))
      processes.append(process)
    except Exception as e:
      print(f"Ошибка при запуске {engine_file}: {e}")
  print(f"\nЗапущено {len(processes)} процессов. Нажмите Ctrl+C для остановки всех.")
  if not processes:
    return
  try:
    # Ждем завершения всех процессов
    for process in processes:
      process.wait()
  except KeyboardInterrupt:
    print("\nОстановка всех процессов...")
    for process in processes:
      try:
        process.terminate()
      except:
        pass
    # Ждем завершения процессов пробуем их убивать 
    for process in processes:
      try:
        process.wait(timeout=5)
      except subprocess.TimeoutExpired:
        process.kill()
    print("Все процессы остановлены.")


def main():
  """Главная функция с выбором режима запуска"""
  print("=== Telegram Userbot Manager ===")
  
  # Сначала проверяем и извлекаем архивы
  extract_zip_archives()
  
  print("\nВыберите режим запуска:")
  print("1. Фоновый запуск (требует готовых сессий)")
  print("2. Последовательный запуск (с авторизацией)")
  print("0. Выход")
  
  while True:
    try:
      choice = input("\nВведите номер (1-2, 0): по умолчанию [1] ").strip()
      if not choice or choice == '1':
        run_all_engines_subprocess()
        break
      elif choice == '2':
        run_engines_sequentially()
        break
      elif choice == '0':
        break
      else:
        print("Неверный выбор. Введите 1 или 2")
    except KeyboardInterrupt:
      print("\nВыход из программы")
      break
    except EOFError:
      print("\nВыход из программы (EOF)")
      break
    except Exception as e:
      print(f"Ошибка: {e}")
      break

if __name__ == "__main__":
  main()
