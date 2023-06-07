from ArtBay import db_cursor, conn
from ArtBay.models import User, Artist, Customer, Produce, Sell, ProduceOrder


# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_Artist(Artist: Artist):
    sql = """
    INSERT INTO Artists(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (Artist.user_name, Artist.full_name, Artist.password))
    conn.commit()


def insert_customer(customer: Customer):
    sql = """
    INSERT INTO Customers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
    conn.commit()


def insert_produce(produce: Produce):
    sql = """
    INSERT INTO Produce(category, item, unit, variety, price)
    VALUES (%s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        produce.category,
        produce.item,
        produce.unit,
        produce.variety,
        produce.price
    ))
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(Artist_pk, produce_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.Artist_pk, sell.produce_pk,))
    conn.commit()


def insert_produce_order(order: ProduceOrder):
    sql = """
    INSERT INTO ProduceOrder(produce_pk, Artist_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.produce_pk,
        order.Artist_pk,
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


def get_Artist_by_pk(pk):
    sql = """
    SELECT * FROM Artists
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    Artist = Artist(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return Artist


def get_produce_by_filters(category=None, item=None, variety=None,
                           Artist_pk=None, Artist_name=None, price=None):
    sql = """
    SELECT * FROM vw_produce
    WHERE
    """
    conditionals = []
    if category:
        conditionals.append(f"category='{category}'")
    if item:
        conditionals.append(f"item='{item}'")
    if variety:
        conditionals.append(f"variety = '{variety}'")
    if Artist_pk:
        conditionals.append(f"Artist_pk = '{Artist_pk}'")
    if Artist_name:
        conditionals.append(f"Artist_name LIKE '%{Artist_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_customer_by_pk(pk):
    sql = """
    SELECT * FROM Customers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return customer


def get_produce_by_pk(pk):
    sql = """
    SELECT produce_pk as pk, * FROM vw_produce
    WHERE produce_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    produce = Produce(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return produce


def get_all_produce_by_Artist(pk):
    sql = """
    SELECT * FROM vw_produce
    WHERE Artist_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_all_produce():
    sql = """
    SELECT produce_pk as pk, category, item, variety, unit, price, Artist_name, available, Artist_pk
    FROM vw_produce
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_available_produce():
    sql = """
    SELECT * FROM vw_produce
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    produce = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return produce


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM ProduceOrder po
    JOIN Produce p ON p.pk = po.produce_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [ProduceOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, produce_pk, Artist_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE produce_pk = %s
    AND Artist_pk = %s
    """
    db_cursor.execute(sql, (available, produce_pk, Artist_pk))
    conn.commit()
