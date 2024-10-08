# Проект "Флип карточки"

## Описание проекта

Учебный проект: Проект для изучения иностранных слов посредством флип-карточек и игры - определи слово.
Тестовый вариант можно посмотреть на flip-cards.ru

## Установка и запуск проекта

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Demek07/flip-cards.git
   cd flip-cards
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Скопируйте файл `.env.example` и переименуйте его в `.env`:

   ```bash
   cp .env.example .env
   ```

5. Откройте файл `.env` и заполните следующие переменные окружения:

   - SECRET_KEY=ВВЕДИТЕ_ВАШ_ДЖАНГО_СЕКРЕТНЫЙ_КЛЮЧ
   - EMAIL_HOST_PASSWORD=ВВЕДИТЕ_ВАШ_ПАРОЛЬ_ОТ_ПОЧТЫ
   - EMAIL_HOST=ВВЕДИТЕ_ВАШ_ХОСТ_ПОЧТЫ
   - EMAIL_PORT=ВВЕДИТЕ_ВАШ_ПОРТ_ПОЧТЫ
   - EMAIL_HOST_USER=ВВЕДИТЕ_ВАШ_ЕМЕЙЛ
   - DEBUG=True - если хотите видеть отладочную инфу при ошибках, False - если не хотите
   - API_DICTIONARYAPI=ВВЕДИТЕ_ВАШ_API_КЛЮЧ_DICTIONARYAPI

6. Примените миграции:

   ```bash
   python manage.py migrate
   ```

7. Создайте суперпользователя для доступа к админ-панели Django:

   ```bash
   python manage.py createsuperuser
   ```

8. Загрузите DUMP базы:

   ```bash
   python manage.py loaddata dump.json
   ```

9. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```
10. Можно использовать🙂
