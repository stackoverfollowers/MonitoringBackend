Хакатон ЕВРАЗа 2.0

Для запуска приложения:
- `git clone https://github.com/stackoverfollowers/MonitoringBackend`
- Создаем файл `.env` в директории бэка (MonitoringBackend), заполняем его данными
```
MONGO_USER=user
MONGO_PASS=passroot
MONGO_DB=main_db
```
- Запускаем бэк с помощью `docker-compose up` в директории бэка
- Берем ссылку на бэк (порт 8000)
- `git clone https://github.com/stackoverfollowers/evraz-client`
- Создаем `.env` в директории фронта (evraz-client), вписываем в него 
`SERVER_URL = "наш url"`
- В папке фронта `docker build -t client .`
- Запускаем фронт с помощью `docker run -p 3000:3000 client`

Наш бэк тут -> http://176.113.82.20/