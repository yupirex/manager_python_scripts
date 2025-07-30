# 0. Для установки обработчиков binfmt
docker run --privileged --rm tonistiigi/binfmt --install arm64,arm

# 1. Соберите Docker-образ для arm64
# Используем --platform=linux/arm64, чтобы Docker знал, что собирать образ для этой архитектуры.
# -t arm64-builder - это имя вашего образа.
docker build --platform=linux/arm64 -f wsl_Dockerfile -t arm64-builder .

# 2. Запустите контейнер и выполните скрипт сборки
# -v "$(pwd):/app" монтирует вашу текущую директорию Windows в /app внутри контейнера.
# Это позволяет контейнеру видеть ваш код и сохранять результат сборки обратно на хост.
# --rm автоматически удалит контейнер после завершения.
# Также пробросить папку дист откуда заберем приложуху
mkdir "dist"

docker run -it --platform=linux/arm64 --rm \
  -v "$(pwd)/mixer.bash:/app/mixer.bash" \
  -v "$(pwd)/source:/app/source" \
  -v "$(pwd)/dist:/app/dist" \
  arm64-builder \
  bash
  #/app/mixer.bash

# docker run -it --platform=linux/arm64 --rm \
#   --mount type=bind,src="$(pwd)/mixer.bash",target=/app/mixer.bash \
#   --mount type=bind,src="$(pwd)/source",target=/app/source \
#   --mount type=bind,src="$(pwd)/dist",target=/app/dist \
#   arm64-builder mixer.bash