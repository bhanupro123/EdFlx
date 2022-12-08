from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired
    

class registerform(FlaskForm):
    name = StringField(label="UserName",validators=[DataRequired()])
    email = EmailField(label="Email",validators=[Email(),DataRequired()])
    password = PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
    repeat_password = PasswordField(label="Repeat Password",validators=[DataRequired(),Length(min=6),EqualTo('password')])
    submit=  SubmitField(label="Register")

class loginform(FlaskForm): 
    email = EmailField(label="Email",validators=[Email(),DataRequired(),Length(min=6)])
    password = PasswordField(label="Password",validators=[Length(min=6),DataRequired()]) 
    submit=  SubmitField(label="Login")

