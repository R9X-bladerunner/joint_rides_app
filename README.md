# joint_rides_app
Тестовое задание состоит из двух частей:
1. Проектирование архитектуры
2. Немного кода

1. Нужно подготовить архитектуру небольшого сервиса, пусть это будет сервис по поиску поездок по типу blablacar.ru 
Достаточно лишь схематично описать архитектуру данного сервиса, не вдаваясь глубоко в детали и описать основные принципы взаимодействия
Что нужно описать детально: 
Таблицы с пользователями
Создание поездок, взаимодействие с ними, таблицу по поездкам

По итогу желательно выдать какую-то общую схему сервиса, описание его принципов работы, возможные сценарии и две таблицы что указаны выше.

2. Немного кода.
Написать на fastAPI часть по взаимодействию с поездками из вышеописанного сервиса. Создание поездки, бронирование поездки, подтверждение поездки, отмена поездки

Quick start:

Local development:
### Setup two databases
docker-compose up -d

### Alembic migrations upgrade and initial_data.py script
bash init.sh

### Run app
uvicorn app.main:app --reload

Run on Docker:
### 
docker compose -f docker-compose.dev.yml up   
