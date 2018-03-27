from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class IndexForm(FlaskForm):
    amount = IntegerField('Amount', validators=[InputRequired("Enter Amount")])
    currency = SelectField('Currency', choices=[('USD', 'USD'),
                                                ('EUR', 'EUR')])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class TipForm(FlaskForm):
    amount = HiddenField('amount')
    currency = HiddenField('currency')
    shop_id = HiddenField('shop_id')
    sign = HiddenField('sign')
    shop_invoice_id = HiddenField('shop_invoice_id')
    description = HiddenField('description')
    submit = SubmitField('Submit')
