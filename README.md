<h3>Хакатон ЕВРАЗа 2.0</h3>

> <h5>Для запуска приложения:</h5>
> 1. `git clone https://github.com/stackoverfollowers/MonitoringBackend`
> 2. Создаем файл `.env` в директории бэка (MonitoringBackend), заполняем его данными
> ```
>  MONGO_USER=user
>  MONGO_PASS=passroot
>  MONGO_DB=main_db
> ```
> 3. Запускаем бэк с помощью `docker-compose up` в директории бэка
> 4. Берем ссылку на бэк (порт 8000)
> 5. `git clone https://github.com/stackoverfollowers/evraz-client`
> 6. Создаем `.env` в директории фронта (evraz-client), вписываем в него 
> `SERVER_URL = "наш url"`
> 7. В папке фронта `docker build -t client .`
> 8. Запускаем фронт с помощью `docker run -p 3000:3000 client`

Наш бэк тут -> http://176.113.82.20/