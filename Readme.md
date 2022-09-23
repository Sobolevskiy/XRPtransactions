# Cервис, который предоставляет данные об переводе XRP на адреса компании.

## Суть работы

Получает информацию о переводах XRP на адреса, указанные пользователем.
Данные выгружает из открытого API XRPL https://xrpl.org.
Данные выгружаются в момент старта сервиса для всех добавленных адресов, в момент добавления нового адреса пользователем,
а так же данные получаются в реалтайме для всех добавленных адресов по вебсокету.

## Quickstart

В дирректории проекта запустить команду
```shell
make start
```
Далее требуется создать суперюзера командой, создастся пользователь с логином admin, и паролем admin
```shell
make user
```

Далее перейти в браузере по адресу http://127.0.0.1:8080/admin/ и зайти в админку под своим суперпользователем
Перейти в раздел _XRPL аккаунты_ и добавить новый аккаунт, автоматически выгрузятся все платежи, а новые данные будут получаться по вебсокету.
Платежи можно найти в разделе Транзакции.
В разделе аккаунты в выпадающем меню есть ручная команда на запуск актуализации платежей аккаунта.

При переходе по адресу http://127.0.0.1:8080/api/ открывается список доступных эндпоинтов
- `/api/transactions/` - получение списка всех транзакций, доступна фильтрация транзакций по полям hash и ledger_index `/api/transactions/?ledger_index=7777`
- `/api/accounts/` - получение списка аккаунтов

## Архитектура

Сервис состоит из следующих частей:
- web - сервис на Django, реализует WEB интерфейс, API, а так же взаимодействие с БД;
- receiver - ресивер данных от биржи на asyncio, получает данные по вебсокету и отправляет их через MQ в web
- redis_consumer - слушает очередь сообщений от receiver и записывает в БД
- celery - реализует асинхронные таски на создание/получение всех транзакций
- db - база данных PostgreSQL
- queue - очередь сообщений Redis

## Принцип работы

1. Пользователь создает аккаунт в админке сервиса web
2. Запускается celery таск на выгрузку всех транзакций пользователя
3. В очередь _accounts_ отправляется сообщение {"add": <account_address>}
4. Ресивер данных получает это сообщение и подписывается по вебсокету на получение данных об этом аккаунте
5. Приходит новая транзакция, ресивер её получает, кладет в очередь _payments_ json с транзакцией
6. Консюмер читает это сообщение и создает celery таск на создание транзакции
7. Пользователь удаляет аккаунт, все транзакции удаляются, а в очередь _accounts_ отправляется сообщение {"delete": <account_address>}
8. Ресивер данных отписывается от получаения данных по вебсокету

## Возможности улучшения
- Проверять события вебсокета и переподписываться при потере коннекта
- Сделать репликацию сообщений в очереди redis, чтобы в случае ошибки не потерять данные
- Добавить дашборд для визуализации платежей