UPDATE activist
SET valid_to_dt = '2023-04-02'
WHERE tg_username = '@hassliebe_i';

INSERT INTO activist (
        activist_id,
        first_name,
        surname,
        tg_username,
        valid_from_dt
    )
SELECT activist_id,
    first_name,
    surname,
    '@nikitin_i_n',
    '2023-04-03'
FROM activist
WHERE tg_username = '@hassliebe_i';

UPDATE activist
SET valid_to_dt = '2020-10-07'
WHERE tg_username = '@elonmusk';

INSERT INTO type_of_waste (
        name,
        category,
        description,
        collection_rules
    )
VALUES (
        'Блистеры',
        'Мелкое / редкое',
        'Блистеры от таблеток или драже',
        'Принимаются только сами блистеры, без таблеток в них'
    );

INSERT INTO container (
        container_id,
        map_location_id,
        place,
        type_of_waste,
        responsible_activist_id,
        description,
        capacity_litres
    )
VALUES (
        DEFAULT,
        (
            SELECT map_location_id
            FROM map_location
            WHERE location_name = '6ка'
        ),
        'Громкая боталка',
        'Блистеры',
        (
            SELECT activist_id
            FROM activist
            WHERE tg_username = '@deizzzy'
        ),
        'Пластиковый контейнер сбоку',
        2.0
    );

DELETE FROM container
WHERE map_location_id = (
        SELECT map_location_id
        FROM map_location
        WHERE location_name = 'АК'
    );

SELECT count(*)
FROM container
WHERE is_maintained;

SELECT tg_username
FROM activist
WHERE valid_to_dt >= now()::date;
