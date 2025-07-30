@echo off
chcp 65001
echo "|===================================|"
echo "| PyInstaller Binary Builder        |"
echo "|===================================|"





:: Создание и Активация окружения для PyInstaller
echo "---> Создание окружения TEMP/.pyinstaller и установка зависимостей проекта."
IF EXIST "TEMP\.pyinstaller\bin\activate" (
  echo "---> Окружение уже установленно, пропускаем создание"
) ELSE (
  python3 -m venv TEMP\.pyinstaller
)
call TEMP\.pyinstaller\Scripts\activate
python3 -m pip install --upgrade pip
pip install --upgrade pyinstaller
IF EXIST "source\requirements.txt" (
  pip install -r source\requirements.txt
) ELSE (
  echo "---> Файл requirements.txt не найден, пропускаем установку зависимостей..."
)

:: Определение файла для сборки
echo "---> Поиск файла для сборки..."
IF EXIST "source\main.py" (
  set "TARGET_FILE=source\main.py"
  set "OUTPUT_NAME=main"
) ELSE (
  echo "---> Поиск файлов *engine.py..."
  set "TARGET_FILE="
  set "OUTPUT_NAME="
  FOR %%f IN ("source\*engine.py") DO (
    set "TARGET_FILE=%%f"
    set "OUTPUT_NAME=%%~nf"
  ) 
)
IF DEFINED TARGET_FILE (
    echo "---> Найден файл: %TARGET_FILE%"
) ELSE (
  echo "---> ОШИБКА: Не найдены файлы main.py или *engine.py для сборки!"
  call .\TEMP\.pyinstaler\Scripts\deactivate.bat
  pause
  exit /b 1
)

:: Определение переменной для корневого пути
set "SCRIPT_DIR=%~dp0"

echo "==============================================="
echo "Сборка приложения с помощью PyInstaller..."
echo "---> Входной файл: %TARGET_FILE%"
echo "---> Выходной файл: %OUTPUT_NAME%"
echo "---> Корневая папка : %SCRIPT_DIR%"
echo "==============================================="

:: Запуск PyInstaller для сборки
:: --target-architecture=x86_64 ^
::
echo "---> Запуск PyInstaller..."
pyinstaller.exe --clean --onefile --console --noconfirm ^
--distpath="%SCRIPT_DIR%dist" --name="%OUTPUT_NAME%" ^
--workpath="%SCRIPT_DIR%TEMP\.build" ^
--specpath="%SCRIPT_DIR%TEMP\.spec" ^
--icon="%SCRIPT_DIR%source\Images\app.ico" ^
%TARGET_FILE%

set "PYINST=%ERRORLEVEL%"
echo "---> Деактивация окружения PyInstaller..."
call .pyinstaller\Scripts\deactivate.bat
IF %PYINST% NEQ 0 (
  echo ОШИБКА: Сборка не удалась!
  pause
  exit /b 1
)

echo "==============================================="
echo "---> Сборка завершена успешно!"
:: Удаление временных директорий
echo "---> Удаление временных директорий..."
RMDIR /S /Q "%SCRIPT_DIR%TEMP\.spec"

:: Открытие папки с результатами сборки
IF EXIST "%SCRIPT_DIR%dist" (
  dir "%SCRIPT_DIR%dist\"
  explorer "%SCRIPT_DIR%dist\"
)




echo "==============================================="
pause
exit /b
