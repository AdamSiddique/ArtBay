from ArtBay import db_cursor, conn
from ArtBay.models import User, Art, Sell, ArtOrder


# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_art(art: Art):
    sql = """
    INSERT INTO Art(title, medium, price, descrip, picture)
    VALUES (%s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        art.title,
        art.medium,
        art.price,
        art.descrip,
        art.image,
    ))
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None



def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(artist_pk, art_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.artist_pk, sell.art_pk,))
    conn.commit()


def insert_art_order(order: ArtOrder):
    sql = """
    INSERT INTO ArtOrder(art_pk, artist_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.art_pk,
        order.artist_pk,
        order.customer_pk,
    ))
    conn.commit()


# SELECT QUERIES
def get_user_by_pk(pk):
    sql = """
    SELECT * FROM Users
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_art_by_filters(medium=None, item=None, variety=None,
                           artist_pk=None, artist_name=None, price=None):
    sql = """
    SELECT * FROM vw_art
    WHERE
    """
    conditionals = []
    if medium:
        conditionals.append(f"medium='{medium}'")
    if item:
        conditionals.append(f"item='{item}'")
    if variety:
        conditionals.append(f"variety = '{variety}'")
    if artist_pk:
        conditionals.append(f"artist_pk = '{artist_pk}'")
    if artist_name:
        conditionals.append(f"artist_name LIKE '%{artist_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    art = [Art(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return art


def get_art_by_pk(pk):
    sql = """
    SELECT art_pk as pk, * FROM vw_art
    WHERE art_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    art = Art(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return art


def get_all_art_by_artist(pk):
    sql = """
    SELECT * FROM vw_art
    WHERE artist_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    art = [Art(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return art


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_all_art():
    sql = """
    SELECT art_pk as art_pk, title, medium, price, descrip, artist_name, available, picture, artist_pk
    FROM vw_art
    """
    order = " ORDER BY price "
    db_cursor.execute(sql + order)
    art = [Art(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return art


def get_available_art():
    sql = """
    SELECT * FROM vw_art
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    art = [Art(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return art


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM ArtOrder ao
    JOIN Art a ON a.pk = ao.art_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [ArtOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, art_pk, artist_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE art_pk = %s
    AND artist_pk = %s
    """
    db_cursor.execute(sql, (available, art_pk, artist_pk))
    conn.commit()

def update_stall(has_stall, user_pk):
    sql = """
    UPDATE Users
    SET has_stall = %s
    WHERE pk = %s
    """
    db_cursor.execute(sql, (has_stall, user_pk))
    conn.commit()