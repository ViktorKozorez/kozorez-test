from flask import Flask, render_template, request, redirect, url_for
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class IndexForm(FlaskForm):
    summ = StringField('summ', validators=[InputRequired("Please enter your summ.")])
    currency = StringField('currency', validators=[InputRequired("Please enter your currency.")])
    description = StringField('description', validators=[InputRequired("Please enter your description.")])
    submit = SubmitField('Submit')

class TipForm(FlaskForm):
    amount = StringField('amount')
    currency = StringField('currency')
    shop_id = StringField('shop_id')
    sign = StringField('sign')
    shop_invoice_id = StringField('shop_invoice_id')
    description = StringField('description')
    submit = SubmitField('Submit')
 
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('tip'))
    return render_template('index.html', form=form)

@app.route('/tip', methods=['GET'])
def tip():
    form = TipForm(request.form)
    return render_template('tip.html', form=form)