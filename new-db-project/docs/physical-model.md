# Физическая модель

---

Таблица `container`:

| Название                  | Описание                              | Тип данных       | Ограничение       |
|---------------------------|---------------------------------------|------------------|-------------------|
| `container_id`            | Идентификатор                         | `INTEGER`        | `PRIMARY KEY`     |
| `map_location_id`         | Расположение (корпус/общежитие)       | `INTEGER`        | `FOREIGN KEY`     |
| `place`                   | Конкретное место, где стоит контейнер | `VARCHAR(200)`   | `NOT NULL`        |
| `type_of_waste`           | Тип отходов                           | `VARCHAR(200)`   | `FOREIGN KEY`     |
| `responsible_activist_id` | Ответственный                         | `INTEGER`        | (FK с учётом SCD) |
| `description`             | Краткое описание                      | `VARCHAR(500)`   | `NOT NULL`        |
| `capacity_litres`         | Вместимость в литрах                  | `NUMERIC(12, 2)` | `NOT NULL`        |
| `is_maintained`           | Обслуживается ли                      | `BOOLEAN`        | `NOT NULL`        |

Таблица `type_of_waste`:

| Название           | Описание      | Тип данных      | Ограничение   |
|--------------------|---------------|-----------------|---------------|
| `name`             | Назаание      | `VARCHAR(200)`  | `PRIMARY KEY` |
| `category`         | Категория     | `VARCHAR(200)`  | `NOT NULL`    |
| `description`      | Описание      | `VARCHAR(2000)` | `NOT NULL`    |
| `collection_rules` | Правила сбора | `VARCHAR(2000)` | `NOT NULL`    |

Таблица `map_location`:

| Название          | Описание               | Тип данных     | Ограничение       |
|-------------------|------------------------|----------------|-------------------|
| `map_location_id` | Идентификатор          | `INTEGER`      | `PRIMARY KEY`     |
| `latitude`        | Географическая широта  | `DECIMAL(8,6)` | `NOT NULL`        |
| `longitude`       | Географическая долгота | `DECIMAL(9,6)` | `NOT NULL`        |
| `location_name`   | Название               | `VARCHAR(200)` | `NOT NULL UNIQUE` |

Таблица `activist`:

| Название        | Описание                 | Тип данных     | Ограничение   |
|-----------------|--------------------------|----------------|---------------|
| `record_id`     | Идентификатор записи     | `INTEGER`      | `PRIMARY KEY` |
| `activist_id`   | Идентификатор активиста  | `INTEGER`      | `NOT NULL`    |
| `first_name`    | Имя                      | `VARCHAR(100)` | `NOT NULL`    |
| `surname`       | Фамилия                  | `VARCHAR(100)` | `NOT NULL`    |
| `tg_username`   | Никнейм в Telegram       | `VARCHAR(100)` | `NOT NULL`    |
| `valid_from_dt` | Актуальность записи - от | `DATE`         | `NOT NULL`    |
| `valid_to_dt`   | Актуальность записи - до | `DATE`         | `NOT NULL`    |

Таблица `taking_out`:

| Название        | Описание                            | Тип данных       | Ограничение   |
|-----------------|-------------------------------------|------------------|---------------|
| `taking_out_id` | Идентификатор записи                | `INTEGER`        | `PRIMARY KEY` |
| `datetime`      | Время выноса                        | `TIMESTAMP`      | `NOT NULL`    |
| `container_id`  | Из какого контейнера вынесли отходы | `INTEGER`        | `FOREIGN KEY` |
| `amount_litres` | Объём в литрах                      | `NUMERIC(12, 2)` | `NOT NULL`    |

Таблица `taking_out_participant`:

| Название        | Описание                     | Тип данных | Ограничение       |
|-----------------|------------------------------|------------|-------------------|
| `taking_out_id` | Идентификатор выноса отходов | `INTEGER`  | `FOREIGN KEY`     |
| `activist_id`   | Участвующий в этом активист  | `INTEGER`  | (FK с учётом SCD) |

Таблица `overflow_report`:

| Название       | Описание                     | Тип данных  | Ограничение   |
|----------------|------------------------------|-------------|---------------|
| `datetime`     | Время сообщения              | `TIMESTAMP` | `NOT NULL`    |
| `container_id` | Какой контейнер переполнился | `INTEGER`   | `FOREIGN KEY` |

---
Таблица `map_location`:
```postgresql
CREATE TABLE map_location (
    map_location_id INTEGER      PRIMARY KEY,
    latitude        DECIMAL(8,6) NOT NULL,
    longitude       DECIMAL(9,6) NOT NULL,
    location_name   VARCHAR(200) NOT NULL UNIQUE,
    CONSTRAINT coords_must_be_unique UNIQUE (latitude, longitude)
);
```
Таблица `type_of_waste`:
```postgresql
CREATE TABLE type_of_waste (
    name             VARCHAR(200)  PRIMARY KEY,
    category         VARCHAR(200)  NOT NULL,
    description      VARCHAR(2000) NOT NULL,
    collection_rules VARCHAR(2000) NOT NULL
);
```
Таблица `activist`:
```postgresql
CREATE TABLE activist (
    record_id     INTEGER      PRIMARY KEY, -- SCD type 2
    activist_id   INTEGER      NOT NULL,    -- natural key
    first_name    VARCHAR(100) NOT NULL,
    surname       VARCHAR(100) NOT NULL,
    tg_username   VARCHAR(100) NOT NULL,
    valid_from_dt DATE         NOT NULL,
    valid_to_dt   DATE         NOT NULL DEFAULT '5999-01-01 00:00:00'
);
```
Таблица `container`:
```postgresql
CREATE TABLE container (
    container_id            INTEGER        PRIMARY KEY,
    map_location_id         INTEGER        NOT NULL
        REFERENCES map_location (map_location_id) ON DELETE RESTRICT,
    place                   VARCHAR(200)   NOT NULL,
    type_of_waste           VARCHAR(200)   NOT NULL
        REFERENCES type_of_waste (name) ON DELETE RESTRICT ON UPDATE CASCADE,
    responsible_activist_id INTEGER,    -- REFERENCES activist (activist_id)
    description             VARCHAR(500)   NOT NULL,
    capacity_litres         NUMERIC(12, 2) NOT NULL,
    is_maintained           BOOLEAN        NOT NULL,
    CONSTRAINT maintained_must_have_activist
        CHECK (responsible_activist_id IS NOT NULL OR NOT is_maintained)
);
```
Таблица `taking_out`:
```postgresql
CREATE TABLE taking_out (
    taking_out_id INTEGER        PRIMARY KEY,
    datetime      TIMESTAMP      NOT NULL,
    container_id  INTEGER        NOT NULL
        REFERENCES container (container_id) ON DELETE RESTRICT,
    amount_litres NUMERIC(12, 2) NOT NULL
);
```
Таблица `taking_out_participant`:
```postgresql
CREATE TABLE taking_out_participant (
    taking_out_id INTEGER NOT NULL 
        REFERENCES taking_out (taking_out_id) ON DELETE CASCADE,
    activist_id   INTEGER NOT NULL -- REFERENCES activist (activist_id)
);
```
Таблица `overflow_report`:
```postgresql
CREATE TABLE overflow_report (
    datetime     TIMESTAMP NOT NULL,
    container_id INTEGER   NOT NULL
        REFERENCES container (container_id) ON DELETE RESTRICT
);
```
