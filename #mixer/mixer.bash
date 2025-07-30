#!/bin/bash

echo "|===================================|"
echo "| PyInstaller Binary Builder        |"
echo "| sudo apt update                   |"
echo "| sudo apt install python3-pip      |"
echo "| sudo apt install python3.11-venv  |"
echo "| sudo apt install python3-dev      |"
echo "|===================================|"

# Создание и Активация окружения для PyInstaller
echo "---> Создание окружения TEMP/.pyinstaller и установка зависимостей проекта."
if [ -r ./TEMP/.pyinstaller/bin/activate ]; then
  echo "---> Окружение уже установленно, пропускаем создание"
else
  python3 -m venv TEMP/.pyinstaller
fi
source TEMP/.pyinstaller/bin/activate 
python3 -m pip install --upgrade pip 
pip install --upgrade pyinstaller
if [ -r ./source/requirements.txt ]; then
  pip install -r ./source/requirements.txt
else
  echo "---> Файл requirements.txt не найден, пропускаем установку зависимостей..."
fi

# Определение файла для сборки
echo "---> Поиск файла для сборки..."
if [ -f "./source/main.py" ]; then
    target_file=source/main.py
    output_name=main
else
    echo "---> Поиск файлов *engine.py..."
    target_file=$(find source/ -name "*engine.py" -type f | head -1)
    output_name=$(basename "$target_file" .py)
fi




if [ -n "$target_file" ]; then
    echo "---> Найден файл: $target_file"
else
    echo "---> ОШИБКА: Не найдены файлы main.py или *engine.py для сборки!"
    deactivate
    read -p "---> Нажмите Enter для выхода..."
    exit 1
fi

# Определение переменной для корневого пути
script_dir=$(dirname "$(realpath "$0")")

echo "==============================================="
echo "Сборка приложения с помощью PyInstaller..."
echo "---> Входной файл: $target_file"
echo "---> Выходной файл: $output_name"
echo "---> Корневая папка : $script_dir"
echo "==============================================="
echo 
# Запуск PyInstaller для сборки
# --target-architecture=universal2 \ # macOS only; valid values: x86_64, arm64, universal2
# --path=".\TEMP\.source\Lib\site-packages" # не допускает пробелы в именах папки, в 7 версии будет ошибкой
echo "---> Запуск PyInstaller..."
pyinstaller --clean --onefile --console --noconfirm \
--distpath="$script_dir/dist" --name="${output_name}" \
--workpath="$script_dir/TEMP/.build" \
--specpath="$script_dir/TEMP/.spec" \
--icon="$script_dir/source/Images/app.ico" \
"${target_file}"

pyinst=$?
echo "---> Деактивация окружения PyInstaller..."
deactivate
if [ $pyinst -ne 0 ]; then
  echo "---> ОШИБКА: Сборка не удалась!"
  read -p "---> Нажмите Enter для выхода..."
  exit 1
fi

echo "==============================================="
echo "---> Сборка завершена успешно!"
# Удаление временных директорий
echo "---> Удаление временных директорий..."
rm -rf "$script_dir/TEMP/.spec"

# Открыть директорию с результатами (Linux аналог explorer)
if command -v xdg-open &> /dev/null; then
    xdg-open "$script_dir/dist"
elif command -v nautilus &> /dev/null; then
    nautilus "$script_dir/dist"
else
    echo "---> Результаты в директории: $script_dir/dist"
    ls -l "$script_dir/dist"
fi
echo "==============================================="
read -p "---> Нажмите Enter для выхода..."

