from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    body = TextAreaField(
        'Message', 
        validators=[DataRequired(), Length(1,200)], 
        render_kw={'class':"form-control", 'placeholder':'Enter Content Here'}
    )
    category = SelectField(
        'Category',
        coerce=int,
        render_kw={'class':"form-control", 'placeholder':'Message Category'}
    )
    submit = SubmitField(
        render_kw={'class':'btn btn-primary', 'type':'submit'}
    )

class DeleteMessageForm(FlaskForm):
    delete = SubmitField('Delete')

class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired(), Length(1,20)])
    submit = SubmitField('Add')

class DeleteCategoryForm(FlaskForm):
    delete = SubmitField('Delete')

class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')