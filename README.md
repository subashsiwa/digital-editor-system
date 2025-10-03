# Digital Editor System

Система управления редакцией с системой ролей и workflow статей.

## 🚀 Быстрый старт

```bash
# Клонирование и установка
git clone https://github.com/YaEvgeshka/digital-editor-system.git
cd digital-editor-system

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# Зависимости и база данных
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Перейдите на http://localhost:8000
📋 Функциональность
👥 Система ролей

    Владелец - полный доступ ко всем функциям

    Редактор - управление контентом и workflow

    Автор - создание и редактирование статей

    Дизайнер - работа с визуальной частью

📊 Workflow статей
text

Черновик → На проверке → Одобрено → Опубликовано

🔧 Технические особенности

    Кастомная модель пользователя

    Разграничение прав доступа

    Система комментариев к статьям

    RESTful архитектура

🛠 Установка для разработки
1. Клонирование репозитория
bash

git clone https://github.com/YaEvgeshka/digital-editor-system.git
cd digital-editor-system

2. Виртуальное окружение
bash

python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Зависимости
bash

pip install -r requirements.txt

4. База данных
bash

python manage.py migrate
python manage.py createsuperuser

5. Запуск
bash

python manage.py runserver

📁 Структура проекта
text

digital-editor-system/
├── config/                 # Настройки Django
│   ├── settings.py        # Основные настройки
│   └── urls.py            # URL маршруты
├── journal/               # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # Логика представлений
│   ├── admin.py           # Админ-панель
│   └── templates/         # HTML шаблоны
├── requirements.txt       # Зависимости Python
└── manage.py             # Утилита управления

🧪 Тестирование
bash

# Запуск всех тестов
python manage.py test

# Тесты конкретного приложения
python manage.py test journal

🌐 Деплой
Настройки для продакшена
python

# В settings.py
DEBUG = False
ALLOWED_HOSTS = ['ваш-домен.com']

# Для PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'digital_editor',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

🔌 API Endpoints

    GET /dashboard/ - Личный кабинет

    POST /articles/create/ - Создание статьи

    POST /articles/1/edit/ - Редактирование статьи

    POST /login/ - Авторизация

    GET /logout/ - Выход


📞 Контакты

Автор: YaEvgeshka
GitHub: https://github.com/YaEvgeshka
Проект: https://github.com/YaEvgeshka/digital-editor-system
