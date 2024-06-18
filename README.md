# test_task_17_06
Здравствуйте!  
Данный проект содержит 1 публичное API для CRUD операций по созданию/добавлению и тд мемов,  
БД postgresql для хранений названий и ссылок на мемы,  
1 приватное API для взаимодействия с s3 хранилищем и само s3 хранилище.  
Запуск  
git clone https://github.com/MalyshM/test_task_17_06.git  
docker compose up --build -d

http://localhost:8090/docs/  
http://localhost:8091/docs/  

Нужно в обязательном порядке создать .env файлы с полями  
ACCESS_KEY
SECRET_KEY
ENDPOINT_URL
BUCKET_NAME  
в приватном API и  
PRIVATE_API_URL
S3_SERVER_URL  
в публичном API  
без этих действий не будет соединения с s3 хранилищем и, соответственно, проект будет нерабочий
