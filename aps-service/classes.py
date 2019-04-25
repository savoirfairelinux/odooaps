from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField


class CreateProduct(FlaskForm):
    title = TextField('Product Title')
    shortdesc = TextField('Short Description')
    priority = IntegerField('Priority')
    create = SubmitField('Create')


class DeleteProduct(FlaskForm):
    key = TextField('Product ID')
    title = TextField('Product Title')
    delete = SubmitField('Delete')


class UpdateProduct(FlaskForm):
    key = TextField('Product Key')
    shortdesc = TextField('Short Description')
    update = SubmitField('Update')


class ResetProduct(FlaskForm):
    reset = SubmitField('Reset')
