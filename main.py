from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Map", validators=[DataRequired(),URL()])
    open = StringField("Opening Time e.g.8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g.5:30PM", validators=[DataRequired()])
    rating = SelectField("Coffe Rating", validators=[DataRequired()], choices=[('✘', '✘'),('☕️', '☕️'),('☕️☕️', '☕️☕️'),('☕️☕️☕️', '☕️☕️☕️'),('☕️☕️☕️☕️', '☕️☕️☕️☕️'),('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')])
    wifi = SelectField("Wifi Strenght Rating", validators=[DataRequired()],choices=[('✘', '✘'),('💪', '💪'),('💪💪', '💪💪'),('💪💪💪', '💪💪💪'),('💪💪💪💪', '💪💪💪💪'),('💪💪💪💪💪', '💪💪💪💪💪')])
    socket = SelectField("Power Socket Availibility", validators=[DataRequired()],choices=[('✘', '✘'),('🔌', '🔌'),('🔌🔌', '🔌🔌'),('🔌🔌🔌', '🔌🔌🔌'),('🔌🔌🔌🔌', '🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        print(form.data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
        with open('day-62/523 Starting-Files-coffee-and-wifi/cafe-data.csv', mode='a') as file:
            file.write(f"\n{form.data['cafe']},{form.data['location']},{form.data['open']},{form.data['close']},{form.data['rating']},{form.data['wifi']},{form.data['socket']}")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('/Users/programing/Desktop/programing/day-62/523 Starting-Files-coffee-and-wifi/cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
            print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    data = []
    if form.validate_on_submit():
        with open('day-62/523 Starting-Files-coffee-and-wifi/login.csv') as file:
            text = csv.reader(file)
            for i in text:
               data.append(i)
            if data[1][0] == form.data['login']:
                if data[1][1] == form.data['password']:
                    return redirect(url_for('add_cafe'))
                else:
                    return render_template('password.html', form = form, err = True)
            else:
                return render_template('password.html', form = form, err = True)
    return render_template('password.html', form = form, err = False)

if __name__ == '__main__':
    app.run(debug=True)
