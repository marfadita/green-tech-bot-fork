CREATE TABLE user (
    chat_id         bigint  PRIMARY KEY, -- chat id's can be greater than 32 bits but always smaller than 52 bits
    username        text,
    first_name      text,
    surname         text,
    state           text    NOT NULL,
    info_subscribed boolean NOT NULL DEFAULT TRUE,
    info_count      integer NOT NULL DEFAULT 0,
    info_rights     boolean NOT NULL DEFAULT FALSE,
    last_usage      date    NOT NULL DEFAULT '1975-01-01',
    temporary_data  text    -- DEFAULT NULL
);

CREATE TABLE map_location (
    name        text            PRIMARY KEY,
    category    text            NOT NULL,
    latitude    decimal(8,6)    NOT NULL,
    longitude   decimal(9,6)    NOT NULL,
    text        text,
    CONSTRAINT coords_must_be_unique UNIQUE (latitude, longitude)
);

CREATE TABLE type_of_waste (
    name        text        PRIMARY KEY,
    is_core     boolean     NOT NULL
);

CREATE TABLE container (
    id                      SERIAL  PRIMARY KEY, -- unique auto-incremented 'integer'
    map_location            text    NOT NULL REFERENCES map_location ON UPDATE CASCADE,
    exact_place             text,
    type_of_waste           text    NOT NULL REFERENCES type_of_waste ON UPDATE CASCADE,
    responsible_activist_id bigint  REFERENCES user ON DELETE RESTRICT,
    description             text,
    is_maintained           boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE report (
    datetime    timestamp   NOT NULL,
    container   integer     NOT NULL REFERENCES container,
    chat_id     bigint      REFERENCES user (chat_id)
);

CREATE TABLE taking_out (
    datetime    timestamp   NOT NULL,
    container   integer     NOT NULL REFERENCES container,
    chat_id     bigint      REFERENCES user (chat_id)
);

CREATE TABLE bot_usage (
    date            date    PRIMARY KEY,
    actions_count   integer NOT NULL,
    users_count     integer NOT NULL
);

CREATE TABLE other_data (
    key     text    PRIMARY KEY,
    value   text    NOT NULL
);
