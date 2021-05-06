from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
class SearchForm(FlaskForm):
    search = StringField("", render_kw={"placeholder": "Введите город",
                                        "style": "width:10%;\
                                                position:absolute;\
                                                top:0;\
                                                left:100px"})
    submit = SubmitField("Поиск", render_kw={"placeholder": "Введите город",
                                             "style": "position:absolute;\
                                                    top:0;\
                                                    left:300px"})