## Новая структура БД

Таблица `user`:
```
chat_id - chat (not person) id & primary key
username - tg username
first_name
surname
state
info_subscribed
info_count - how many info messages they have received
info_rights - can they send info messages
last_usage
temporary_data (json)
```

Таблица `map_location`:
```
name
category (общежития, корпуса или внешние точки)
latitude
longitude
text
```

Таблица `type_of_waste`: `name is_core`

Таблица `container`:
```
id
map_location  -> name
exact_place
type_of_waste -> name
responsible_activist_id -> chat_id
description (для карты)
is_maintained (на случай, если придётся контейнер временно убрать/закрыть)
```

Таблица `bot_usage`: `date actions_count users_count`

Таблица `report`: `datetime container chat_id`

Таблица `taking_out`: `datetime container chat_id`

Таблица `other_data`: столбцы `key`, `value` (например, хранить дату ближайшей акции, дату последнего обновления карты)
