### Запуск

`Перед запуском автоматически прогоняются тесты`

1. Создать файл с переменным окружения согласно шаблону .env.sample в корне проекта
2. Собрать контейнер `docker-compose build`
3. Запустить контейнер `docker-compose up`

### Схема БД
https://dbdiagram.io/d/635ee6cc5170fb6441c3a569

### Задание
Реализовать веб-сервис для организации учебного процесса в ВУЗе.  
Основные сущности:
- Куратор
- Направление подготовки
- Учебная дисциплина
- Учебная группа
- Студент

Администратором сервиса формируются направления подготовки, имеющие
свой перечень учебных дисциплин. За каждым направлением закреплен куратор.
Куратор зачисляет студентов и формирует учебные группы на основании
направлений. Каждая группа может состоять максимум из 20 студентов.
Функционал администратора:
- Управление направлениями подготовки
- Управление учебными дисциплинами
- Формирование отчета в виде эксель файла

Функционал куратора:

- Управление студентами
- Управление учебными группами

Требования:
- Набор полей моделей на личное усмотрение.
- Отчет администратора должен содержать в себе информацию о
направлениях(список направлений и их дисциплин и данные кураторов) и о
группах(отсортированный список студентов, данные о составе групп(кол-во
мужчин и женщин, количество свободных мест в группе)).
- Отчет должен генерироваться с помощью асинхронной задачи. Должен быть
отдельный метод, позволяющий узнать статус задачи и сгенерированный
отчет.  
Стек: DRF, СУБД PostgreSQL, Celery для асинхронных задач, брокер на свой
выбор.