DROP TABLE IF EXISTS Produce CASCADE;

CREATE TABLE IF NOT EXISTS Pieces(
    pk serial unique not null PRIMARY KEY,
    category varchar(30),
    item varchar(30),
    variety varchar(30),
    unit varchar(10),
    price float
);

DELETE FROM Pieces;

CREATE INDEX IF NOT EXISTS pieces_index
ON Pieces (category, item, variety);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    artist_pk int not null REFERENCES Artists(pk) ON DELETE CASCADE,
    piece_pk int not null REFERENCES Pieces(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (artist_pk, piece_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (artist_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS PieceOrder;

CREATE TABLE IF NOT EXISTS PieceOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    artist_pk int not null REFERENCES Artists(pk) ON DELETE CASCADE,
    piece_pk int not null REFERENCES Pieces(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM PieceOrder;

CREATE OR REPLACE VIEW vw_piece
AS
SELECT p.category, p.item, p.variety,
       p.unit, p.price, s.available,
       p.pk as produce_pk,
       a.full_name as artist_name,
       a.pk as artist_pk
FROM Pieces p
JOIN Sell s ON s.piece_pk = p.pk
JOIN Artists a ON s.artist_pk = a.pk
ORDER BY available, p.pk;