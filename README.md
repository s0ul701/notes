# NOTES

## Локальный запуск

1. Склонировать проект:

   ```bash
   git clone https://github.com/s0ul701/notes.git
   ```

2. Зайти в папку проекта:

    ```bash
    cd notes
    ```

3. Собрать Docker-образы:

    ```bash
    docker-compose build
    ```

4. Запустить Docker-образы (+ скачать образы используемых сервисов):

    ```bash
    docker-compose up
    ```

[API-документация](http://0.0.0.0:1337/docs/)
