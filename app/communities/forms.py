from wtforms import Form, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired

# ===== Forms  ===== #

class CommunityCreateForm(Form):
    name = StringField('title', validators=[InputRequired()])
    about = TextAreaField('about')
    img = FileField('img')
    bgimg = FileField('bgimg')

class CommunityCustomizeForm(Form):
    about = TextAreaField('about')
    img = FileField('img')
    bgimg = FileField('bgimg')
