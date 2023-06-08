DROP TABLE IF EXISTS Art CASCADE;

CREATE TABLE IF NOT EXISTS Art(
    pk serial unique not null PRIMARY KEY,
    title varchar(30),
    medium varchar(30),
    price float,
    descrip varchar(30),
    picture bytea
);

DELETE FROM Art;

CREATE INDEX IF NOT EXISTS art_index
ON Art (medium);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    artist_pk int not null REFERENCES Artists(pk) ON DELETE CASCADE,
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
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    artist_pk int not null REFERENCES Artists(pk) ON DELETE CASCADE,
    art_pk int not null REFERENCES Art(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM ArtOrder;

CREATE OR REPLACE VIEW vw_art
AS
SELECT p.medium, p.price, s.available,
       p.pk as art_pk,
       f.full_name as artist_name,
       f.pk as artist_pk
FROM Art p
JOIN Sell s ON s.art_pk = p.pk
JOIN Artists f ON s.artist_pk = f.pk
ORDER BY available, p.pk;