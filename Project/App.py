import os
import logging
import socket
from datetime import datetime, timedelta
from functools import wraps

import MySQLdb
import jwt
from faker import Faker
from flask import request, Flask, jsonify, session
from flask_mysqldb import MySQL
from marshmallow import ValidationError, Schema, fields, validate
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'media/images'  # 'media/images'
ALLOWED_EXTENSIONS = (['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

# live database
app.config['MYSQL_HOST'] = '35.213.140.165'
app.config['MYSQL_USER'] = 'uwgwdvoi7jwmp'
app.config['MYSQL_PASSWORD'] = 'Clinicalfirst@123'
app.config['MYSQL_DB'] = 'dbim4u0mfuramq'
app.config['SECRET_KEY'] = 'secret-key'

# local database
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'raghu'
# app.config['MYSQL_DB'] = 'clinicalfirst_services'
# app.config['SECRET_KEY'] = 'secret-key'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql = MySQL(app)


# default root:-
# @app.route("/")
# def default():
#     return "<h1>Test Message from Empty root !!!</h1>"

# Validations:-
class User_SignUp(Schema):
    # user_signupid = fields.String(validate=validate.Regexp(r'[A-Za-z0-9]+'))
    username = fields.String(validate=validate.Regexp(r'[A-Za-z]+'))
    email = fields.Email(required=True)
    phone = fields.String(validate=validate.Regexp(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'),
                          required=True)
    password = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9@#$%^&+=]{8,32}'))
    ip = fields.String(validate=validate.Regexp(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|'
                                                r'[01]?[0-9][0-9]?)$'))
    # date = fields.String(validate=validate.Regexp(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$'))


class PATIENT_PERSONAL_DETAILS(Schema):
    # user_signupid = fields.String(validate=validate.Regexp(r'[A-Za-z0-9]+'))
    username = fields.String(validate=validate.Regexp(r'[A-Za-z]+'))
    email = fields.Email(required=True)
    phone = fields.String(validate=validate.Regexp(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$'),
                          required=True)
    password = fields.String(validate=validate.Regexp(r'^[A-Za-z0-9@#$%^&+=]{8,32}'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/image', methods=['POST'])
def index():
    now = datetime.now()
    if request.method == 'POST':
        userDetails = None
        path = request.form['user_folder_path + filename']
        mail_id = request.form['mail_id']
        if request.files['image']:
            userDetails = request.files['image']
        # else:
        #     userDetails = users(request.form)
        if userDetails and allowed_file(userDetails.filename):
            filename = secure_filename(userDetails.filename)
            user_folder_path = app.config['UPLOAD_FOLDER'] + '/pics/'
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)
            userDetails.save(os.path.join(user_folder_path, filename))
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO Images(file_name,mail_id,uploaded_on) VALUES(%s,%s,%s)',
                               (user_folder_path + filename, mail_id, now))
                mysql.connection.commit()
                cursor.close()
            except Exception as e:
                print(e)
                return "Unable to insert image metadata to db"
            return "Image uploaded successfully."


# ==================================PATIENT SIGNUP==================================== #
# Signup:-
@app.route('/user/insert', methods=['POST'])
def User_signup():
    # @wraps()
    # def wrappersUserSignup(*args, **kwargs):
    if 'username' in request.json and 'password' in request.json \
            and 'email' in request.json and 'phone' in request.json:

        request_data = request.json
        username = request_data['username']
        email = request_data['email']
        phone = request_data['phone']
        password = request_data['password']
        # date = request.json['date']

        hassedpassword = generate_password_hash(password)
        # userip = request_data['ip']
        ex = Faker()
        ip = ex.ipv4()
        print(ip)
        # date = request_data['date']
        device = socket.gethostname()
        print(device)

        # UserId Pattern for Insert Operation:-
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT PATIENT_ID FROM PATIENT_SIGNUP")
        last_user_id = cursor.rowcount
        print('----------------------------------')
        print("Last Inserted ID is: " + str(last_user_id))
        pattern = 'PA000'  # pattern = ooo
        last_user_id += 1
        # add_value = 00
        # pattern += 1 # pattern incremnting always by 1:-
        user_id = pattern + str(last_user_id)  # pass 'user_id' value in place holder exactly
        # User Id pattern Code End #

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM PATIENT_SIGNUP WHERE PATIENT_MAIL_ID = %s OR PATIENT_PHONE_NUMBER = %s',
                       (email, phone))
        account = cursor.fetchone()

        if account and account[3] == email:
            return 'Your Email already exist please enter new Email !', 400

        elif account and account[4] == phone:
            return "Your Phone number is duplicate please enter new number!!!", 400

        # elif account:
        #     return fun(account, args, *kwargs)

        result = User_SignUp()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into PATIENT_SIGNUP(PATIENT_ID, PATIENT_NAME, PATIENT_MAIL_ID, PATIENT_PHONE_NUMBER, PATIENT_PASSWORD,"
                "PATIENT_IP, PATIENT_DEVICE) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (user_id, username, email, phone, hassedpassword, ip, device))
            mysql.connection.commit()
            logging.info("successfully registered")

            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200

@app.route('/new/user', methods=['POST'])
def PATIENT_PERSONAL_DETAILS():
    # @wraps()
    # def wrappersUserSignup(*args, **kwargs):
    if 'username' in request.json and 'email' in request.json \
            and 'phone' in request.json and 'password' in request.json:
        # Variables:
        request_data = request.json
        username = request_data['username']
        email = request_data['email']
        phone = request_data['phone']
        password = request_data['password']
        # date = request.json['date']

        hassedpassword = generate_password_hash(password)
        # userip = request_data['ip']
        # ex = Faker()
        # ip = ex.ipv4()
        # print(ip)
        # # date = request_data['date']
        # device = socket.gethostname()
        # print(device)

        # UserId Pattern for Insert Operation:-
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT PATIENT_ID FROM PATIENT_PERSONAL_DETAILS")
        last_user_id = cursor.rowcount
        print('----------------------------------')
        print("Last Inserted ID is: " + str(last_user_id))
        pattern = 'PA000'  # pattern = ooo
        last_user_id += 1
        # add_value = 00
        # pattern += 1 # pattern incremnting always by 1:-
        user_id = pattern + str(last_user_id)  # pass 'user_id' value in place holder exactly
        # User Id pattern Code End #

        # Cursor:-
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM PATIENT_PERSONAL_DETAILS WHERE PATIENT_MAIL_ID = %s OR PATIENT_PHONE_NUMBER = %s',
                       (email, phone))
        account = cursor.fetchone()

        if account and account[3] == email:
            return 'Your Email already exist please enter new Email !', 400

        elif account and account[4] == phone:
            return "Your Phone number is duplicate please enter new number!!!", 400

        # elif account:
        #     return fun(account, args, *kwargs)

        result = User_SignUp()
        try:
            # Validate request body against schema data types
            result.load(request_data)
            cur = mysql.connection.cursor()
            cur.execute(
                "insert into PATIENT_PERSONAL_DETAILS(PATIENT_ID, PATIENT_NAME, PATIENT_MAIL_ID, PATIENT_PHONE_NUMBER, PATIENT_PASSWORD) VALUES(%s, %s, %s, %s, %s)",
                (user_id, username, email, phone, hassedpassword))
            mysql.connection.commit()
            logging.info("successfully registered")
            # return fun("successfully inserted", args, *kwargs), 201
            return "Succesfully Inserted", 200
        except ValidationError as e:
            # logTo_database("/user/insert", "user_signup", e, 401)
            return (e.messages), 400
    return "Invalid input", 200


# return wrappersUserSignup

# Session's Added:-
# Login:-
def logined(func):
    @wraps(func)
    def Wrapperlogin(*args, **kwargs):
        if 'email' in request.json and 'password' in request.json:
            email = request.json["email"]
            pw = request.json["password"]

            logging.warning('Watch out!')

            cur = mysql.connection.cursor()
            # cur.execute("select USER_PASSWORD from user_signup where USER_MAIL_ID = %s", (email,))
            cur.execute('SELECT * FROM PATIENT_SIGNUP WHERE PATIENT_MAIL_ID = %s', (email,))
            details = cur.fetchone()

            if details is None:
                return 'Email not registered', 401
            # else:
            #     session['loggedin'] = True
            #     # session['id'] = details['USER_ID']
            #     session['id'] = details['ID']

            # if details:
            #     # Create session data, we can access this data in other routes
            #     session['loggedin'] = True
            #     session['id'] = details['ID']
            #     session['username'] = details['USER_NAME']
            # else:
            #     # Account doesnt exist or username/password incorrect
            #     msg = 'Incorrect username/password!'

            hashed_password = details[5]
            password_match = check_password_hash(hashed_password, pw)
            if password_match:

                #     session['USER_ID'] = details['USER_ID']
                #     return "Successfully Loggedin"
                # else:
                #     logging.error("Invalid Credentials")

                # generate the JWT Token
                data = {
                    'user_mail': email,
                    'password': hashed_password,
                    "user_id": details[1],
                    'exp': datetime.utcnow() + timedelta(minutes=2)}
                token = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
                data['token'] = token
                return func(data, *args, **kwargs)
            else:
                logging.error("Invalid credentials")
            return "invalid credentials", 401
        return "Insufficient parameters", 400

    return Wrapperlogin


@app.route('/user/login', methods=["POST"])
@logined
def login_testing(data):
    # log_data(data)
    return data['token']


def token_validate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({"message": "Token is invalid"})

        return f(data, *args, **kwargs)

    return decorated


@app.route('/user/logined', methods=['GET'])
@token_validate
def token_testing(data):
    return data


@app.route('/patient_login', methods=["POST"])
def login():
    if 'email' in request.json and 'password' in request.json:
        email = request.json["email"]
        logging.info('Admin logged in')
        pw = request.json["password"]
        logging.warning('Watch out!')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("select * from PATIENT_PERSONAL_DETAILS WHERE (PATIENT_MAIL_ID = %s )", (email,)) # PATIENT_PERSONAL_DETAILS, PATIENT_SIGNUP
        details = cur.fetchone()
        if details is None:
            return ({"message": "No details"}), 401
        # if details and details["PATIENT_MAIL_ID"]!= email:
        #     return "invalid mailid"
        hashed_password = details["PATIENT_PASSWORD"]
        password_match = check_password_hash(hashed_password, pw)
        if password_match:
            session['loggedin'] = True
            session['PATIENT_ID'] = details['PATIENT_ID']
            return "successfully login"
        else:
            logging.error("Invalid credentials")
        return ({"Error": "invalid credentials"}), 401
    return "Insufficient parameters", 400


# Logout:-
@app.route('/user/logout', methods=['POST'])
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('PATIENT_ID', None)
    return "User Loggedout Successfully !!!"


    # # session.pop('username', None)
    # # Cursor Initialized:-
    # cur = mysql.connection.cursor()
    # cur.execute('select PATIENT_MAIL_ID from PATIENT_SIGNUP')
    # Email_id = cur.fetchall()
    # Login_Email_id = Email_id[-1]
    # print(Login_Email_id)
    # =============================== #
    # date and time object:-
    # now = datetime.now()
    # logout_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # cur = mysql.connection.cursor()
    # cur.execute('insert into logins_data(LOGIN_EMAIL_ID, LOGOUT_TIME) values(%s, %s)', (id, logout_time))
    # return "User " + Login_Email_id + "Logged Out Successfully !!!"



# AMB_BOOKING
@app.route('/amb/booking', methods=["POST"])
def book():
    if 'loggedin' in session:
        if 'situation_type' in request.json and 'cause_type' in request.json \
                and 'amb_type' in request.json and "price" in request.json and "advance_type_or_basic" in request.json:

            patient_id = session['PATIENT_ID']
            situation_type = request.json["situation_type"]
            amb_type = request.json["amb_type"]
            advance_name_or_basic = request.json["advance_type_or_basic"]
            price = request.json["price"]
            cause = request.json["cause_type"]

            try:
                cur = mysql.connection.cursor()
                cur.execute("select SITUATION_ID from AMB_SITUATIONS where (SITUATION_TYPE = %s)", (situation_type,))
                data1 = cur.fetchone()
                if data1 is None:
                    return "No details in account"
                cur = mysql.connection.cursor()
                cur.execute("select AMB_TYPE_ID from AMB_AMBULANCE_TYPES where (AMB_TYPE = %s)", (amb_type,))
                data2 = cur.fetchone()
                if data2 is None:
                    return "No data in your account"
                cur = mysql.connection.cursor()
                cur.execute("select BASIC_TYPE_ID from AMB_BASIC_TYPES where (BASIC_TYPE_NAME = %s)",
                            (advance_name_or_basic,))
                data3 = cur.fetchone()
                if data3 is None:
                    cur = mysql.connection.cursor()
                    cur.execute("select ADVANCED_TYPE_ID from AMB_ADVANCED_TYPES where (ADVANCED_TYPE_NAME = %s)",
                                (advance_name_or_basic,))
                    data3 = cur.fetchone()
                    if data3 is None:
                        return "No data in your account"
                cur = mysql.connection.cursor()
                cur.execute("select CAUSE_ID from AMB_CAUSES where (CAUSE_TYPE = %s)", (cause,))
                data5 = cur.fetchone()
                if data5 is None:
                    return "No data in your account"

                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into AMB_BOOKING(PATIENT_ID,SITUATION_ID, AMB_TYPE_ID, BASIC_OR_ADVANCE, CAUSE_ID, PRICE)"
                    "values(%s,%s,%s,%s,%s,%s)", (patient_id, data1, data2, data3, data5, price))

                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)

        return "invalid parameters"
    return "User not loggedin, please login first"

# DOC_BOOKING
@app.route("/doc/booking", methods=["POST"])
def doc_booking():
    if 'loggedin' in session:
        if 'specilization_name' in request.json and 'date' in request.json and 'time' in request.json \
                and 'consultation_fee' in request.json:

            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            specilization_name = request.json["specilization_name"]
            date = request.json["date"]
            time = request.json["time"]
            consultation_fee = request.json['consultation_fee']

            try:
                cur = mysql.connection.cursor()
                cur.execute("select SPECIALIZATION_ID from IDC_SPECIALIZATION where (SPECIALIZATION_NAME = %s)",
                            (specilization_name,))
                data = cur.fetchone()
                if data is None:
                    return "No details in account"
                # Txn code
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into DOCTOR_BOOKING(SPECILIZATION_ID, PATIENT_ID, DATE, TIME, CONSULTATION_FEE)"
                    " values(%s, %s, %s, %s, %s)",
                    (data, PATIENT_ID, date, time, consultation_fee))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# BLOOD_RECEIVE
@app.route("/blood/receive", methods=["POST","GET"])
def blood_available():
    if "loggedin" in session:
        if "blood_group" in request.json and "component_type" in request.json and "pickup" in request.json:
            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            N_NAME = 'RECEIVE'
            blood_group = request.json["blood_group"]
            component_type = request.json["component_type"]
            pickup = request.json["pickup"]
            try:
                # BookId Pattern
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT BOOK_ID FROM BBS_BOOKING_FOR_RECEIVE")
                last_booking_id = cursor.rowcount
                pattern = 'BOOK00'  # pattern = ooo
                last_booking_id += 1
                # add_value = 00
                # pattern += 1 # pattern incremnting always by 1:-
                BOOK_ID = pattern + str(last_booking_id)  # pass 'user_id' value in place holder exactly
                cur = mysql.connection.cursor()
                cur.execute("select N_ID from BBS_NECESSITY where (N_NAME = %s)",
                            (N_NAME,))
                NID = cur.fetchone()
                if NID is None:
                    return "No necessity details found"

                cur = mysql.connection.cursor()
                cur.execute("select B_ID from BBS_BLOOD_GROUP where (BLOOD_GROUP = %s)",
                            (blood_group,))
                BID = cur.fetchone()
                if BID is None:
                    return "No details Blood Found"

                cur = mysql.connection.cursor()
                cur.execute("select CMP_ID from BBS_COMPONENTS where CMP_NAME = %s",
                            (component_type,))
                CMPID = cur.fetchone()
                if CMPID is None:
                    return "No Component details found"

                cur = mysql.connection.cursor()
                cur.execute("select DISPATCH_ID from BBS_DISPATCH where (DISPATCH_NAME = %s)",
                            (pickup,))
                DISPATCHID = cur.fetchone()
                if DISPATCHID is None:
                    return "No pickup type details found"
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into BBS_BOOKING_FOR_RECEIVE(BOOK_ID, PATIENT_ID, B_ID, CMP_ID, DISPATCH_ID)"
                    "values(%s, %s, %s, %s, %s)",
                    (BOOK_ID, PATIENT_ID, BID, CMPID, DISPATCHID))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
                return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# BLOOD_DONATE
@app.route("/blood/donate", methods=["POST"])
def blood_donate():
    if "loggedin" in session:
        if "blood_group" in request.json and "age" in request.json:
            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            blood_group = request.json["blood_group"]
            age = request.json["age"]
            try:
                # BookId Pattern
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT DONOR_ID FROM BBS_DONATE_BLOOD")
                last_donor_id = cursor.rowcount
                pattern = 'DON00'  # pattern = ooo
                last_donor_id += 1
                # add_value = 00
                # pattern += 1 # pattern incremnting always by 1:-
                DONOR_ID = pattern + str(last_donor_id)  # pass 'user_id' value in place holder exactly
                cur = mysql.connection.cursor()
                cur.execute("select B_ID from BBS_BLOOD_GROUP where BLOOD_GROUP = %s",
                            (blood_group,))
                BloodGroup = cur.fetchone()
                if BloodGroup is None:
                    return "Given Blood Group Details Not Found"
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into BBS_DONATE_BLOOD(DONOR_ID, PATIENT_ID, BLOOD_GROUP, AGE) values(%s, %s, %s, %s)",
                    (DONOR_ID, PATIENT_ID, BloodGroup, age))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# Local connections

# brain_disease
@app.route("/brain/disease", methods=["POST"])
def brain_disease():
    if "loggedin" in session:
        if "brain_disease" in request.json and "brain_disease_symptom" in request.json and "medications" in request.json:
            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            brain_disease = request.json["brain_disease"]
            brain_disease_symptom = request.json["brain_disease_symptom"]
            medications = request.json['medications']
            try:
                cur = mysql.connection.cursor()
                cur.execute("select BRAIN_DISEASES_ID from BRAIN_DISEASES_TYPES where (BRAIN_DISEASE_NAME = %s)",
                            (brain_disease,))
                BrainDisease = cur.fetchone()
                if BrainDisease is None:
                    return "No details in account"
                cur = mysql.connection.cursor()
                cur.execute("select BRAIN_DISEASES_SYMPTOMS_ID from BRAIN_DISEASE_SYMPTOM where (BRAIN_DISEASES_SYMPTOMS_NAME = %s)",
                            (brain_disease_symptom,))
                BrainDiseaseSymptom = cur.fetchone()
                if BrainDiseaseSymptom is None:
                    return "No details in account"
                # Txn Table
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into BRAIN_DISEASE(PATIENT_ID, BRAIN_DISEASE_ID, BRAIN_DISEASE_SYMPTON, MEDICATIONS) values(%s, %s, %s, %s)",
                    (PATIENT_ID, BrainDisease, BrainDiseaseSymptom, medications))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# kidney_disease
@app.route("/kidney/disease", methods=["POST"])
def kidney_disease():
    if "loggedin" in session:
        if "kidney_symptom" in request.json and "medications" in request.json:
            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            kidney_symptom = request.json["kidney_symptom"]
            medications = request.json["medications"]
            try:
                cur = mysql.connection.cursor()
                cur.execute("select KIDNEY_DISEASE_SYMPTOMS_ID from KIDNEY_DISEASE_SYMPTOMS where (KIDNEY_DISEASE_SYMPTOMS_NAME = %s)",
                            (kidney_symptom,))
                KidneySymptom = cur.fetchone()
                if KidneySymptom is None:
                    return "No details in account"
                # Txn Table
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into KIDNEY_DISEASE(PATIENT_ID, KIDNEY_SYMPTON_ID, KIDNEY_MEDICATIONS) values(%s, %s, %s)",
                    (PATIENT_ID, KidneySymptom, medications))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# previous_health_issues
@app.route("/health/issues", methods=["POST"])
def health_issues():
    if "loggedin" in session:
        if "issue_name" in request.json and "TREATMENT_TAKEN_AT" in request.json and "SURGERIES" in request.json and \
            "COMPLICATIONS_DURING_TREATMENT" in request.json and "MEDICATIONS" in request.json and \
            "LIST_ANY_ALLERGIESTO_MEDICATIONS" in request.json:
            # Variables:-
            PATIENT_ID = session['PATIENT_ID']
            issue_name = request.json["issue_name"]
            TREATMENT_TAKEN_AT = request.json["TREATMENT_TAKEN_AT"]
            SURGERIES = request.json['SURGERIES']
            COMPLICATIONS_DURING_TREATMENT = request.json['COMPLICATIONS_DURING_TREATMENT']
            MEDICATIONS = request.json['MEDICATIONS']
            LIST_ANY_ALLERGIESTO_MEDICATIONS = request.json['LIST_ANY_ALLERGIESTO_MEDICATIONS']

            try:
                cur = mysql.connection.cursor()
                cur.execute("select ISSUE_ID from HEALTH_ISSUES where (ISSUE_NAME = %s)",
                            (issue_name,))
                IssueName = cur.fetchone()
                if IssueName is None:
                    return "No details in account"
                # Txn Table
                cur = mysql.connection.cursor()
                cur.execute(
                    "insert into PREVIOUS_HEALTH_ISSUES(USER_ID, ISSUE_ID, TREATMENT_TAKEN_AT, SURGERIES, COMPLICATIONS_DURING_TREATMENT, MEDICATIONS, LIST_ANY_ALLERGIESTO_MEDICATIONS) values(%s, %s, %s, %s, %s, %s, %s)",
                    (PATIENT_ID, IssueName, TREATMENT_TAKEN_AT, SURGERIES, COMPLICATIONS_DURING_TREATMENT, MEDICATIONS, LIST_ANY_ALLERGIESTO_MEDICATIONS))
                mysql.connection.commit()
                return "successfully inserted", 200
            except ValidationError as e:
                print(e)
            return jsonify(e.messages)
        return "invalid parameters"
    return "User not loggedin, please login first"

# MAIN app To Run the Flask Script:-
if __name__ == "__main__":
    app.run(debug=True)

    # app.run(host="0.0.0.0", port=8080, debug=True)

# ALTER TABLE `dbim4u0mfuramq`.`PATIENT_SIGNUP`
# CHANGE COLUMN `PATIENT_MAIL_ID` `PATIENT_MAIL_ID` VARCHAR(40) NULL DEFAULT NULL ;





