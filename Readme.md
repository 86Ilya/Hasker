# Hasker: Poor Man's Stackoverflow

Данный проект представляет собой простой аналог сайта *stackoverflow*

### Перед установкой 

Для установки проекта у вас должен быть предустановлен *Docker* в системе.

## Локальные настройки
Все локальные настройки вынесены в `local_settings.py`
Данный модуль необходимо настроить согласно вашему окружению на основе примера `local_settings.template`
Для докер образа данный модуль идёт в комплекте.

### Установка 
Для установки проекта вам достаточно склонировать репозиторий и запустить скрипт `/deploy.sh`
После завершения сборки и успешного прохождения тестов сервер запустится на локальном хосте по адресу:
http://localhost:8000/
<br/>
Для завершения работы достаточно ввести **Ctrl+C**

## Запуск тестов

Тесты запускаются автоматически после сборки докер-контейнеров.
Для "ручного" запуска необходимо в контейнере с проектом ввести команду:
```bash
python3 /opt/hasker/manage.py test
``` 

## API
У проекта имеется API, более подробное описание находится по следующему адресу:
```
http://hostname/api/v1/docs/
```
Где `hostname` - это имя машины с запущенным сервером Hasker

## Проект собран с использованием следующих библиотек 

* [Django v2.1.7](https://www.djangoproject.com/) - Web framework
* [Bootstrap v4.3.1](https://getbootstrap.com/) - Used in front-end
* [Fontawesome v5.8.1](http://fontawesome.ru/) - Used in front-end
