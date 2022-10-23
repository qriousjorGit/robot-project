from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///robotbase2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.String(100), unique=False, nullable=True)
    robot_name = db.Column(db.String(100), unique=False, nullable=True)
    robot_deactivated = db.Column(db.String(100), unique=False, nullable=True)
    robot_photo = db.Column(db.String(100), unique=False, nullable=True)
    robot_title = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Botlist %r>' % self.robot_name

all_bots = db.session.query(Robot).all()

# bot_to_update = Robot.query.filter_by(robot_deactivated = '01-14-2022').all()
# print(bot_to_update)

print(len(all_bots))
# print(type(all_bots))
# print(all_bots[0].robot_photo)

janbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('01'):
        # print(bot.robot_name, bot.robot_deactivated, bot.robot_photo)
        janbots.append(bot)

print(f"January - {len(janbots)}")

febbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('02'):
        # print(bot.robot_name, bot.robot_deactivated, bot.robot_photo)
        febbots.append(bot)

print(f"February - {len(febbots)}")

marchbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('03'):
        # print(bot.robot_name, bot.robot_deactivated, bot.robot_photo)
        marchbots.append(bot)

print(f"March - {len(marchbots)}")

aprilbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('04'):
        # print(bot.robot_name, bot.robot_deactivated, bot.robot_photo)
        aprilbots.append(bot)

print(f"April - {len(aprilbots)}")

maybots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('05'):
        # print(bot.robot_name, bot.robot_deactivated, bot.robot_photo)
        maybots.append(bot)

print(f"May - {len(maybots)}")

junebots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('06'):
        junebots.append(bot)

print(f"June list {len(junebots)}")

julybots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('07'):
        julybots.append(bot)

print(f"July list {len(julybots)}")

augustbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('08'):
        augustbots.append(bot)

print(f"August list {len(augustbots)}")

septemberbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('09'):
        septemberbots.append(bot)
        
octoberbots = []
for bot in all_bots:
    if bot.robot_deactivated.startswith('10'):
        octoberbots.append(bot)

print(f"October list {len(octoberbots)}")


@app.route('/')
def home():
    return render_template('index.html', jan_list=janbots, feb_list=febbots, march_list=marchbots, april_list=aprilbots, may_list=maybots, june_list=junebots, july_list=julybots, august_list=augustbots, sept_list=septemberbots,  oct_list=octoberbots)
    #TODO: There's probably a better way to render the template with "length" than passing a list for every month

@app.route('/all')
def show_all():
    return render_template('all.html', jan_list=janbots, feb_list=febbots, march_list=marchbots, april_list=aprilbots, may_list=maybots, june_list=junebots, july_list=julybots, august_list=augustbots, sept_list=septemberbots,  oct_list=octoberbots)


@app.route('/<month>')
def show_month(month):
    if month == '1':
        return render_template('month.html', bot_list=janbots)
    elif month == '2':
        return render_template('month.html', bot_list=febbots)
    # elif request.args.get('month') == '3':
    elif month == '3':
        return render_template('month.html', bot_list=marchbots)
    elif month == '4':
        return render_template('month.html', bot_list=aprilbots)
    elif month == '5':
        return render_template('month.html', bot_list=maybots)
    elif month == '6':
        return render_template('month.html', bot_list=junebots)
    elif month == '7':
        return render_template('month.html', bot_list=julybots)
    elif month == '8':
        return render_template('month.html', bot_list=augustbots)
    elif month == '9':
        return render_template('month.html', bot_list=septemberbots)
    elif month == '10':
        return render_template('month.html', bot_list=octoberbots)
   


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        a1 = request.form.get('answer1')
        a2 = request.form.get('answer2')

        if check_answer(a1, a2):
            return f"<a href='mailto:qriousjor@yahoo.com'> Email me! </a>"
        else:
            return f"Answers submitted {a1} and {a2} are not correct." \
                   f"<br> " \
                   f"<img src='static/images/shallnotpass.png')' alt='Gandalf' style='width: 50%'>"

    return render_template('contact.html')

def check_answer(a, b):
    if a.lower() == "taras shevchenko":
        if b.lower() == "vareniki" or b.lower() == "varenyky":
            return True
        else:
            return False

if __name__ == "__main__":
    app.run(debug=True)

