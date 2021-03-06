# ai_tech_testcase
Для запуска выполнить команду `docker-compose up -d`


Сервис запустится на порте 8000


___________________________________________________________________

Необходимо написать очень простой поисковик по текстам документов. Данные хранятся в БД по желанию, поисковый индекс в эластике. 

Ссылка на тестовый массива данных: [[csv](https://drive.google.com/uc?export=download&confirm=s5vl&id=1O5rOunfzkkF4vIZXk3WCbb6A2XpRPDt1)]

### Структура БД:

- `id` - уникальный для каждого документа;
- `rubrics` - массив рубрик;
- `text` - текст документа;
- `created_date` - дата создания документа.

### Структура Индекса:

- `iD` - id из базы;
- `text` - текст из структуры БД.

## Необходимые методы

- сервис должен принимать на вход произвольный текстовый запрос, искать по тексту документа в индексе и возвращать первые 20 документов со всем полями БД, упорядоченные по дате создания;
- удалять документ из БД и индекса по полю  `id`.

## Технические требования:

- любой python фреймворк кроме Django и DRF;
- `README` с гайдом по поднятию;
- `docs.json` - документация к сервису в формате openapi.

## Программа максимум:

- функциональные тесты;
- сервис работает в Docker;
- асинхронные вызовы.
