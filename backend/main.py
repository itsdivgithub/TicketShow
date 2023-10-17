from lib import *

app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()

#Set the database URI
db_uri= 'sqlite:///'+ os.path.join(os.path.abspath(os.path.dirname(__file__)), 'castshow.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Flask CORS 
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

#celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TIMEZONE='Asia/Kolkata'
)
celery = make_celery(app)
app.app_context().push()


##______________________________________CELERY TASKS----ALL TASKS OF CELERY____________________________________________##

           ######_______________________EXPORT CSV TASK - USER TRIGGERED_______________________######

@celery.task
def generate_csv_file(venue_id):
    import csv
    import os
    import time

    #time.sleep(6)
    venue = Venue.query.get(venue_id)
    if not venue:
        return None

    shows_data = []
    for show in venue.shows:
        total_bookings = db.session.query(func.sum(Bookings.seats_booked)).filter(Bookings.show_id == show.id).scalar()
        total_booked_cost = db.session.query(func.sum(Bookings.booked_cost)).filter(Bookings.show_id == show.id).scalar()
        shows_data.append([
            show.name,
            show.rating,
            total_bookings or 0,
            total_booked_cost or 0
        ])

    with open("static/details.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Show Name', 'Rating', 'Number of Bookings', 'Total Booked Cost'])
        for show_data in shows_data:
            writer.writerow(show_data)

    return "Export Job Started.."



class Trigger(Resource):
    def get(self, venue_id):
        a=generate_csv_file.delay(venue_id)
        return {
            "Task_ID": a.id,
            "Task_State": a.state,
            "Task_Result": a.result  
        }
        
class Download(Resource):
    def get(self):
        return send_file('static/details.csv', as_attachment=True)
               



         ###__________________________CELERY TASK SCHEDULAR - DAILY REMINDER______________________________###

@celery.on_after_finalize.connect
def daily_periodic_tasks(sender, **kwargs):
	# UTC Time
	sender.add_periodic_task(crontab(hour=16, minute=39), SendDailyReminder.s(), name = "Daily Evening")
	sender.add_periodic_task(crontab(hour=16, minute=39, day_of_month=2), SendMonthlyReport.s(), name = "2nd of every month")	


WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAW_vDagA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=qPFhzCE_lERGsjhjqBhpeIW0HlHSB_rRxsawG4SFPiM"


@celery.task()
def SendDailyReminder():
    print("Starting SendDailyReminder Task")

    today = datetime.utcnow().date()

    users = db.session.query(User).filter_by(is_admin=False).all()

    for user in users:
        bookings_today = db.session.query(Bookings).filter_by(user_id=user.id, booked_time=today).first()

        if not bookings_today:
            url = WEBHOOK_URL
            data = {'text': f"Dear {user.username},\nWe have seen you haven't booked show today. Grab Your Tickets before shows get HOUSEFULL!!"}
            r = requests.post(url=url, json=data)




      ###_______________________CELERY TASK SCHEDULAR - MONTHLY ENTERTAINTMENT REPORT______________________###



SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@mycinema.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

def format_message(template_file, lastmonth, data={}, bookings=[]):

    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1]+ "-" + str(currentYear)

    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, lastmonth=lastmonth, bookings=bookings)

def get_user_bookings(user_id, lastmonth):

    today = datetime.utcnow()
    currentmonth= today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    bookings = Bookings.query \
        .join(Show) \
        .filter(Bookings.user_id == user_id, Bookings.booked_time >= lastmonth, Bookings.booked_time < currentmonth) \
        .all()


    user_bookings = []
    for booking in bookings:
        venue_name = booking.Show.Venue.name
        show_name = booking.Show.name
        rating = booking.Show.rating
        seats= booking.seats_booked
        cost = booking.booked_cost

        booking_info = {
            'venue_name': venue_name,
            'show_name': show_name,
            'rating': rating,
            'seats' : seats,
            'cost': cost,
        }
        user_bookings.append(booking_info)

    return user_bookings

def send_monthly_report_email(data, lastmonth):
    user_id = data.id  
    bookings = get_user_bookings(user_id, lastmonth)


    message = format_message("monthly_report.html", lastmonth=lastmonth, data=data, bookings=bookings)
    send_email(data.email, subject="Monthly Report", message=message)


@celery.task()
def SendMonthlyReport():
    print("Starting SendMonthlyReport Task")

    users = db.session.query(User).filter_by(is_admin=False).all()

    today = datetime.utcnow()
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    last_month = first_day_of_previous_month

    for user in users:
        send_monthly_report_email(data=user, lastmonth=last_month)


#-------------------------------------------------------------------------------------------------------------------------



# database initialization
db.init_app(app)

# API initialization
api = Api(app)
api.init_app(app)

# JWT initialization
JWTManager(app)

# Flask Security
security.init_app(app, user_datastore)


# Flask Caching
cache.init_app(app)

api.add_resource(SignupAPI, '/api/signup')
api.add_resource(AdminSignupAPI, '/api/adminsignup')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(AdminLoginAPI, '/api/admin/login')
api.add_resource(AdminAddTheatreAPI, '/api/admin/venue')
api.add_resource(AdminGetTheatreAPI, '/api/admin/venue')
api.add_resource(AdminEditTheatreAPI, '/api/admin/venue/<venue_id>')
api.add_resource(AdminAddShowAPI, '/api/admin/shows/<int:venue_id>')
api.add_resource(AdminGetShowAPI, '/api/admin/shows/<int:venue_id>')
api.add_resource(AdminEditShowAPI, '/api/admin/shows/<int:venue_id>/<int:show_id>')
api.add_resource(AdminDeleteVenueAPI, '/api/admin/venue/<int:venue_id>')
api.add_resource(AdminDeleteShowAPI, '/api/admin/shows/<int:venue_id>/<int:show_id>')
api.add_resource(PostedVenuesAPI, '/api/user/venues')
api.add_resource(PostedShowsAPI, '/api/user/venue/<int:venue_id>/shows')
api.add_resource(VenueDetailAPI, '/api/book/venue/<int:venue_id>')
api.add_resource(ShowDetailAPI, '/api/book/venue/<int:venue_id>/<int:show_id>')
api.add_resource(BookShowAPI, '/api/book/venue/<int:venue_id>/show/<int:show_id>/bookings')
api.add_resource(GetSeatsAPI, '/api/book/venue/<int:venue_id>/show/<int:show_id>/seats')
api.add_resource(BookDashAPI, '/api/user/bookings')
api.add_resource(SearchVenuesAPI, '/api/search')
api.add_resource(Trigger, '/api/trigger/<int:venue_id>')
api.add_resource(Download, '/api/download')
api.add_resource(SummaryAPI, '/api/admin/summary')


if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            app.run(debug=True)