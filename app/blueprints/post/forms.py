from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    img_url = StringField('Image URL: ', validators=[DataRequired()])
    caption = StringField('Caption : ', validators=[DataRequired()])
    location = StringField('Location :')
    submit_btn = SubmitField('Create Post')