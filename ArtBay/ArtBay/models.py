from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from ArtBay import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')


class Customer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class Artist(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = Artist(user_data)
    print(user)


class Art(ModelMixin):
    def __init__(self, art_data: Dict):
        super(Art, self).__init__(art_data)
        self.pk = art_data.get('pk')
        self.title = art_data.get('title')
        self.medium = art_data.get('medium')
        self.price = art_data.get('price')
        self.descrip = art_data.get('descrip')
        self.image = art_data.get('image')
        # From JOIN w/ Sell relation
        self.available = art_data.get('available')
        self.artist_name = art_data.get('artist_name')
        self.artist_pk = art_data.get('artist_pk')


class Sell(ModelMixin):
    def __init__(self, sell_data: Dict):
        super(Sell, self).__init__(sell_data)
        self.available = sell_data.get('available')
        self.artist_pk = sell_data.get('artist_pk')
        self.art_pk = sell_data.get('art_pk')


class ArtOrder(ModelMixin):
    def __init__(self, art_order_data: Dict):
        super(ArtOrder, self).__init__(art_order_data)
        self.pk = art_order_data.get('pk')
        self.customer_pk = art_order_data.get('customer_pk')
        self.artist_pk = art_order_data.get('artist_pk')
        self.art_pk = art_order_data.get('art_pk')
