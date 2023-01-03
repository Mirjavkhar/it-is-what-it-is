from wtforms import Form, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length

# ===== Forms  ===== #

class ReportForm(Form):
    title = StringField('title', validators=[InputRequired()])
    content = TextAreaField('content')
    file = FileField('file')