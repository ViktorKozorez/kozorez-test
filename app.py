from flask import Flask, render_template, request, redirect, url_for, session
import requests

import config
import utils
from forms import IndexForm, TipForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'V6G4J7EECPFZJ9DDD'


@app.route('/', methods=['GET'])
def index():
    form = IndexForm()
    return render_template('index.html', form=form)


@app.route('/switch', methods=['POST'])
def switch():
    form = IndexForm(request.form)
    if form.currency.data == 'USD':
        return redirect(url_for('tip'), code=307)
    elif form.currency.data == 'EUR':
        return redirect(url_for('invoice'), code=307)


@app.route('/tip', methods=['GET', 'POST'])
def tip():
    if request.method == 'POST':
        form = IndexForm(request.form)
        if form.validate_on_submit():
            session['amount'] = form.amount.data
            session['currency'] = form.currency.data
            session['description'] = form.description.data
            return redirect(url_for('tip'))
        else:
            return render_template('index.html', form=form)
    
    amount = session.get('amount')
    currency = config.currencies[session.get('currency')]
    shop_id = config.shop_id
    shop_invoice_id = utils.random_generator()
    description = session.get('description')

    sign = utils.MD5_generator([amount, currency, shop_id, shop_invoice_id],
                               config.secret)

    form = TipForm(amount=amount,
                   currency=currency,
                   shop_id=shop_id,
                   sign=sign,
                   shop_invoice_id=shop_invoice_id,
                   description=description)

    return render_template('tip.html', form=form)


@app.route('/invoice', methods=['POST'])
def invoice():
    if request.method == 'POST':
        form = IndexForm(request.form)
        if form.validate_on_submit():
            amount = form.amount.data
            currency = config.currencies[form.currency.data]
            payway = 'payeer_eur'
            shop_id = config.shop_id
            shop_invoice_id = utils.random_generator()
            description = form.description.data

            sign = utils.MD5_generator([amount, currency, payway, shop_id, shop_invoice_id],
                                       config.secret)

            postData = {'amount': amount,
                          'currency': currency,
                          'payway': payway,
                          'shop_id': shop_id,
                          'shop_invoice_id': shop_invoice_id,
                          'sign': sign}

            res = requests.post('https://central.pay-trio.com/invoice',
                                json=postData)
 
            return redirect(res.json()['data']['data']['referer'])
        else:
            return render_template('index.html', form=form)
