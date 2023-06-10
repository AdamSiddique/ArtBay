import base64

from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user

from ArtBay.forms import FilterArtForm, AddArtForm, BuyArtForm
from ArtBay.models import Art as ArtModel, ArtOrder
from ArtBay.queries import insert_art, get_art_by_pk, Sell, \
    insert_sell, get_all_art_by_artist, get_art_by_filters, insert_art_order, update_sell, \
    get_orders_by_customer_pk, get_all_art, update_stall

Art = Blueprint('Art', __name__)


@Art.route("/art", methods=['GET', 'POST'])
def art():
    form = FilterArtForm()
    title = 'Our art!'
    art = []
    if request.method == 'POST':
        art = get_art_by_filters(medium=request.form.get('medium'),
                                         item=request.form.get('item'),
                                         artist_name=request.form.get('sold_by'),
                                         price=request.form.get('price'))
        title = f'Our {request.form.get("medium")}!'
    return render_template('pages/art.html', art=get_all_art(), form=form, title=title, current_user=current_user)

@Art.route("/add-art", methods=['GET', 'POST'])
@login_required
def add_art():
    if not current_user.has_stall:
        pk = current_user.pk
        update_stall(has_stall=True,
                     user_pk=pk)
    form = AddArtForm(data=dict(artist_pk=current_user.pk))
    if request.method == 'POST':
        if form.validate_on_submit():
            art_data = dict(
                title=form.title.data,
                medium=form.medium.data,
                price=form.price.data,
                descrip=form.descrip.data,
                image=form.image.data
            )
            art = ArtModel(art_data)
            new_art_pk = insert_art(art)
            sell = Sell(dict(artist_pk=current_user.pk, art_pk=new_art_pk, available=True))
            insert_sell(sell)
            # Redirect to your_art after successful form submission
            return redirect(url_for('Art.your_art'))
    return render_template('pages/add-art.html', form=form)


@Art.route("/your-art", methods=['GET', 'POST'])
@login_required
def your_art():
    form = FilterArtForm()
    art = []
    if request.method == 'GET':
        art = get_all_art_by_artist(current_user.pk)
    if request.method == 'POST':
        art = get_art_by_filters(medium=request.form.get('medium'),
                                         artist_pk=current_user.pk)
    return render_template('pages/your-art.html', form=form, art=art)


@Art.route('/art/buy/<pk>', methods=['GET', 'POST'])
@login_required
def buy_art(pk):
    form = BuyArtForm()
    art = get_art_by_pk(pk)
    if request.method == 'POST':
        if form.validate_on_submit():
            order = ArtOrder(dict(art_pk=art.pk,
                                      artist_pk=art.artist_pk,
                                      customer_pk=current_user.pk))
            insert_art_order(order)
            update_sell(available=False,
                        art_pk=art.pk,
                        artist_pk=art.artist_pk)
            return redirect(url_for('Art.your_orders'))
    return render_template('pages/buy-art.html', form=form, art=art)


@Art.route('/art/your-orders')
def your_orders():
    orders = get_orders_by_customer_pk(current_user.pk)
    return render_template('pages/your-orders.html', orders=orders)

@Art.route("/create-stall", methods=['GET', 'POST'])
def create_stall():
    return render_template('pages/create-stall.html')