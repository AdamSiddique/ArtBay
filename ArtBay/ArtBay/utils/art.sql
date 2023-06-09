DROP TABLE IF EXISTS Art CASCADE;

CREATE TABLE IF NOT EXISTS Art(
    pk serial unique not null PRIMARY KEY,
    title varchar(30),
    medium varchar(30),
    price int,
    descrip varchar(200),
    picture varchar(2083)
);

DELETE FROM Art;

CREATE INDEX IF NOT EXISTS art_index
ON Art (medium);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    artist_pk int not null REFERENCES Users(pk) ON DELETE CASCADE,
    art_pk int not null REFERENCES Art(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (artist_pk, art_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (artist_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS ArtOrder;

CREATE TABLE IF NOT EXISTS ArtOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Users(pk) ON DELETE CASCADE,
    artist_pk int not null REFERENCES Users(pk) ON DELETE CASCADE,
    art_pk int not null REFERENCES Art(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM ArtOrder;

CREATE OR REPLACE VIEW vw_art
AS
SELECT a.title, a.medium, a.price, a.descrip, a.picture, s.available,
       a.pk as art_pk,
       u.full_name as artist_name,
       u.pk as artist_pk
FROM Art a
JOIN Sell s ON s.art_pk = a.pk
JOIN Users u ON s.artist_pk = u.pk
ORDER BY available, a.pk;