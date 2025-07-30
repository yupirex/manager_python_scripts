# PyInstaller Build System

Этот каталог содержит скрипты для автоматической сборки исполняемых файлов из Python-проектов с помощью PyInstaller на различных платформах.

## Структура файлов

```note
#mixer/
├── pyinstall.zip             # Архив со всеми скриптами сборки
└── pyinstall/                # Рабочая директория сборки
    ├── mixer.bash            # Скрипт сборки для Linux/macOS
    ├── mixer.cmd             # Скрипт сборки для Windows  
    ├── wsl_arm.bash          # Скрипт для сборки ARM64 через Docker
    ├── wsl_Dockerfile        # Docker образ для ARM64 сборки
    └── source/               # Исходные файлы для сборки
        ├── main.py           # Тестовое приложение (проверка среды)
        ├── requirements.txt  # Зависимости Python
        ├── commons/          # Утилиты
        │   └── conf_util.py
        └── Images/
            └── app.ico       # Иконка приложения
```

## Быстрый старт

### Windows

```cmd
cd #mixer/pyinstall
mixer.cmd
```

### Linux/macOS  

```bash
cd #mixer/pyinstall
./mixer.bash
```

### ARM64 через Docker (WSL/Linux)

```bash
cd #mixer/pyinstall
./wsl_arm.bash
```

## Подготовка к сборке

1. **Скопируйте ваш проект** в папку `source/`, заменив содержимое
2. **Убедитесь что есть один из файлов:**
   - `main.py` (приоритет)
   - Или любой файл с паттерном `*engine.py`
3. **Создайте `requirements.txt`** со всеми зависимостями
4. **Опционально:** замените `Images/app.ico` на вашу иконку

## Детальное описание скриптов

### mixer.bash (Linux/macOS)

- Создает виртуальное окружение в `TEMP/.pyinstaller/`
- Устанавливает PyInstaller и зависимости из `requirements.txt`
- Автоматически находит файл для сборки (`main.py` или `*engine.py`)
- Собирает single-file исполняемый файл с консолью
- Результат сохраняется в `dist/`
- Очищает временные файлы
- Автоматически открывает папку с результатом

**Системные требования:**

```bash
sudo apt update
sudo apt install python3-pip python3.11-venv python3-dev
```

### mixer.cmd (Windows)

- Аналогичная функциональность для Windows
- Использует Windows-специфичные команды (`call`, `set`, `pause`)
- Открывает результат через `explorer`
- Поддерживает кодировку UTF-8 (`chcp 65001`)

### wsl_arm.bash + wsl_Dockerfile (ARM64)

**Docker-based сборка для ARM64 архитектуры**:

1. **Установка эмуляции ARM64:**

   ```bash
   docker run --privileged --rm tonistiigi/binfmt --install arm64,arm
   ```

2. **Сборка Docker образа:**

   ```bash
   docker build --platform=linux/arm64 -f wsl_Dockerfile -t arm64-builder .
   ```

3. **Запуск контейнера:**

   ```bash
   mkdir dist
   docker run -it --platform=linux/arm64 --rm \
     -v "$(pwd)/mixer.bash:/app/mixer.bash" \
     -v "$(pwd)/source:/app/source" \
     -v "$(pwd)/dist:/app/dist" \
     arm64-builder bash
   ```

**Dockerfile включает:**

- Debian Bookworm ARM64
- Python 3 + pip + dev tools
- Виртуальное окружение с PyInstaller
- Все необходимые библиотеки разработки

## Тестовое приложение

В `source/main.py` находится утилита проверки среды, которая тестирует:

- ✅ Информацию о системе (ОС, архитектура, Python)
- ✅ Импорт стандартных и сторонних модулей
- ✅ Функциональность Tkinter GUI  
- ✅ Сетевые возможности (requests)
- ✅ Работу с конфигурационными файлами

Это полезно для проверки совместимости вашей среды перед сборкой реальных проектов.

## Настройки PyInstaller

Все скрипты используют следующие параметры:

- `--clean` - очистка кэша перед сборкой
- `--onefile` - создание единого исполняемого файла
- `--console` - включение консольного окна
- `--noconfirm` - автоматическое подтверждение
- `--icon` - использование пользовательской иконки
- Настраиваемые пути для dist, build, spec

## Устранение неполадок

### Общие проблемы

1. **Отсутствуют зависимости Python:**
   - Проверьте `requirements.txt`
   - Убедитесь что все модули устанавливаются без ошибок

2. **Не найден файл для сборки:**
   - Убедитесь что в `source/` есть `main.py` или `*engine.py`
   - Проверьте права доступа к файлам

3. **Ошибки компиляции PyInstaller:**
   - Проверьте совместимость версий зависимостей
   - Попробуйте обновить PyInstaller: `pip install --upgrade pyinstaller`

### Docker ARM64 специфичные

1. **Ошибка "no matching manifest":**
   - Убедитесь что установлены обработчики binfmt
   - Проверьте поддержку multi-arch в Docker

2. **Проблемы монтирования томов:**
   - Используйте абсолютные пути
   - Проверьте права доступа к директориям

## Для сборки конкретного бинарника

1. **Скопируйте проект:**

   ```bash
   cp -r _your_project/* #mixer/pyinstall/source/
   ```

2. **Переименуйте main файл** (если необходимо):

   ```bash
   mv source/your_engine.py source/main.py
   ```

3. **Запустите сборку** соответствующим скриптом

4. **Найдите результат** в `dist/your_project_name.exe` или `dist/main`

## Поддерживаемые платформы

- ✅ Windows (x86_64)
- ✅ Linux (x86_64)
- ✅ macOS (x86_64, Apple Silicon)
- ✅ Linux ARM64 (через Docker)

Результирующие исполняемые файлы не требуют установки Python на целевой машине и содержат все необходимые зависимости. Собранные файлы можно запускать в нескольких экземплярах, для Linux `nohup bin_file &`
