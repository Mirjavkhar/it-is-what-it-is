from wtforms import Form, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length

# ===== Forms  ===== #

class PostForm(Form):
    title = StringField('title', validators=[InputRequired()])
    content = TextAreaField('content')
    file = FileField('file')
    
class CommentForm(Form):
    comment = TextAreaField('comment')
