import pytz
from flask import Flask, request
from flask_mysqldb import MySQL
from twilio.twiml.messaging_response import MessagingResponse
from operator import itemgetter
import threading
from twilio.rest import Client
import itertools
import time
from datetime import datetime

app = Flask(__name__, template_folder='./templates')

app.config['SECRET_KEY'] = 'otp'
app.config['MYSQL_HOST'] = 'firstpharmcy.com'
app.config['MYSQL_USER'] = 'u3a9uet4oxglm'
app.config['MYSQL_PASSWORD'] = 'b#@y9b@{83D3'
app.config['MYSQL_DB'] = 'db0zx1rnsrwts8'

mysql = MySQL(app)

existedId = []
existedList =[]


def s_m():
    with app.app_context():
        cur1 = mysql.connection.cursor()
        cur1.execute("select * from fp_customer")
        mysql.connection.commit()
        info1 = cur1.fetchall()
        print("excuted")
        print(info1)
        account_sid = 'ACb7f39384a577dad02ac9ad1263911bd1'
        auth_token = '6de4a3f460a35e27991bfb20c6b1eda5'
        client = Client(account_sid, auth_token)
        company_name = "*FIRST PHARMCY*"
        print(info1)
        for i in info1:
            s1 = "whatsapp:+91"
            s2 = i[7]
            name1 = i[4]
            name = name1.capitalize()
            telephone = "{}{}".format(s1, s2)
            print(telephone)
            print(len(telephone))
            nam = f"*{name}*"
            data1 = "*50,000*"
            data2 = "*50*"
            data3 = "*20*"
            data4 = "*65*"
            if i[7] not in existedList:
                existedList.append(i[7])
                msg = f"Namaste {nam}  🙏 !!\nWelcome to {company_name}  ⚕ !!\n\n{company_name} is online pharmacy offering over {data1}+ products.\n⭐ Upto {data2}% discount on all Medicines\n⭐Upto {data3}% discount on all Personal and Healthcare products.\n⭐ Upto {data4}% discount on Medical devices.\n\n🤩 Hey  checkout our offers on products 👇\nhttps://firstpharmcy.com/specials\n\n➡ If you wish to go through our services type Hi or Hello 🙋"
                message = client.messages.create(
                    from_="whatsapp:+13094855558",
                    body=msg,
                    to=telephone
                )

    return True

def m():
    i = 0
    while i <= 10:
        timezone = pytz.timezone('Asia/Kolkata')
        now1 = datetime.now(timezone)
        current_time = now1.strftime("%H:%M:%S")
        data = current_time.split(':')
        if data[0] == "11":
            s_m()
            existedList.clear()
            time.sleep(60*60)


b = threading.Thread(target=m)
b.start()

def check_orders():
    with app.app_context():
        timezone = pytz.timezone('Asia/Kolkata')
        now1 = datetime.now(timezone)
        datetime_1 = now1.strftime("%Y-%m-%d %H:%M:%S")

        print(datetime_1)
        cur = mysql.connection.cursor()
        query1 = 'select date_added from fp_order'
        cur.execute(query1)
        data_fetch = cur.fetchall()
        print(data_fetch)
        var_fixed_order_date = []
        for rowing1 in data_fetch:
            var_fixed_order_date.append(tuple(map(str, tuple(rowing1))))
        print(var_fixed_order_date)
        out = list(itertools.chain(*var_fixed_order_date))
        print(out)
        list_defined = []

        x_text = datetime_1.split(' ')
        y_text = ",".join(x_text)
        a_text = y_text.split('-')
        z_text = ",".join(a_text)
        b_text = z_text.split(':')
        c_text = ",".join(b_text)
        print(c_text)
        data_1 = c_text.split(',')
        print(data_1)
        for dt in out:
            # print(dt)
            x1_text = dt.split(' ')
            y1_text = ",".join(x1_text)
            a1_text = y1_text.split('-')
            z1_text = ",".join(a1_text)
            b1_text = z1_text.split(':')
            c1_text = ",".join(b1_text)
            # print(c1_text)
            data_11 = c1_text.split(',')
            # print(data_11)
            if data_1[0] == data_11[0] and data_1[1] == data_11[1] and data_1[2] == data_11[2] and data_1[3] == data_11[
                3] and data_1[4] == data_11[4]:
                print("Hello  " + dt)
                cur1 = mysql.connection.cursor()
                cur1.execute('select order_id,firstname,telephone,date_added from fp_order where date_added = %s',
                             (dt,))
                data_fetch1 = cur1.fetchall()
                print(data_fetch1)
                for rowing2 in data_fetch1:
                    list_defined.append(tuple(map(str, tuple(rowing2))))

    return list_defined


def send_messages(people):
    account_sid = 'ACb7f39384a577dad02ac9ad1263911bd1'
    auth_token = '6de4a3f460a35e27991bfb20c6b1eda5'

    client = Client(account_sid, auth_token)
    print(people)
    for i in people:
        print(i[0])
        print(i[1])
        s1 = "whatsapp:+91"
        s2 = i[2]

        phone = "{}{}".format(s1, s2)
        print(phone)
        print (len(phone))
        name =i[1]
        order_id=i[0]
        date_added =i[3]

        msg =f"Hello {name} 😊 !!! Thank you for ordering 👉 Your order {order_id} has been placed on {date_added} ,To know the order status 🚚 👉 Enter 4:Your Order ID [Ex-4:000000]"
        if i[0] not in existedId:
            if len(phone)== 22:

                existedId.append(i[0])
                message = client.messages.create(

                    from_="whatsapp:+13094855558",
                    body=msg,
                    to=phone
                )
                return True

    return True
def main():
    var_fixed_order = check_orders()
    send_messages(var_fixed_order)
def hello():
    i = 0
    while i <= 10:
        main()


a = threading.Thread(target=hello)
a.start()

@app.route("/sms", methods=['POST', "GET"])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    if request.method == 'POST':
        msg = request.values.get('Body')
        resp = MessagingResponse()
        mesg = resp.message()

        if msg == "Hi" or msg == "hi" or msg == "hello" or msg == "Hello" or msg == 'a good day' or msg == 'A good day' or msg == 'Hello there' or msg == 'hello there' or msg == "Hai" or msg == "hai" or msg == "Hey" or msg == "hey":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            fetchdata = cursor.fetchone()
            print(fetchdata)
            company_name = "*FIRST PHARMCY*"
            if fetchdata:
                print(fetchdata[7])
                if phnum == fetchdata[7]:
                    mesg.body(
                        f"Welcome to {company_name}  ⚕ {fetchdata[4]} ☺ !!! Select a service from the list 🤔\n\n➡  1 👉 To view the cart 🛒 \n\n➡  2 👉 To view order history 🕙\n\n➡  3:Your Order ID 👉 To view the order details 🧾\n\n➡  4:Your Order ID 👉 To view the order status 🚚\n\n➡  5 👉 To view your coupons 🏷\n\n➡  6 👉 To view your wishlist 💟\n\n➡  7 👉 To view our contact details 📱\n\n➡  8 👉 To view main menu 📃\n\n➡ Hey checkout our offers 🤩 https://firstpharmcy.com/specials 🤩")

                    return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)

        elif msg == "8":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            company_name = "*FIRST PHARMCY*"
            print(validation)
            if validation:
                mesg.body(
                    "➡  1 👉 To view the cart 🛒 \n\n➡  2 👉 To view order history 🕙\n\n➡  3:Your Order ID 👉 To view the order details 🧾\n\n➡  4:Your Order ID 👉 To view the order status 🚚\n\n➡  5 👉 To view your coupons 🏷\n\n➡  6 👉 To view your wishlist 💟\n\n➡  7 👉 To view our contact details 📱\n\n➡  8 👉 To view main menu 📃\n\n➡ Hey checkout our offers 🤩 https://firstpharmcy.com/specials 🤩")
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        elif msg == "1":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            company_name = "First Pharmcy"
            print(validation)
            if validation:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "select fp_cart.product_id,fp_product_description.name, fp_cart.quantity , fp_product.price from fp_cart join fp_customer  on  fp_cart.customer_id = fp_customer.customer_id join fp_product_description on fp_cart.product_id = fp_product_description.product_id join fp_product on fp_cart.product_id = fp_product.product_id where telephone =%s",
                    (phnum,))
                fetchdata = cursor.fetchall()
                print(fetchdata)
                if fetchdata:
                    print(fetchdata)

                    var_fixed = []
                    for row in fetchdata:
                        var_fixed.append(tuple(map(str, tuple(row))))
                    print(var_fixed)
                    keys = ("Product_id", "Product_Name", "Quantity", "Unit_Price")
                    data = get_list_of_dict(keys, var_fixed)
                    print(data)
                    var_fixed_data = '\n\n'.join(str(feature) for feature in data)
                    mesg.body(f"Products in your cart 🛒:\n\n{var_fixed_data}\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                else:
                    mesg.body("Your Cart is empty ❗\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)

        elif msg == "2":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            company_name = "*FIRST PHARMCY*"
            print(validation)
            if validation:

                cursor = mysql.connection.cursor()
                cursor.execute(
                    "select fp_order.order_id,fp_order_product.name  from fp_order join fp_order_product on fp_order.order_id=fp_order_product.order_id where fp_order.telephone = %s",
                    (phnum,))
                fetchdata = cursor.fetchall()
                print(fetchdata)
                if fetchdata:
                    list_data = list(fetchdata)
                    print(list_data)
                    out = {}
                    for elem in list_data:
                        try:
                            out[elem[0]].extend(elem[1:])
                        except KeyError:
                            out[elem[0]] = list(elem)
                    b = [tuple(values) for values in out.values()]
                    print(b)
                    orders_list = '\n\n'.join(str(feature) for feature in b)
                    print(orders_list)
                    mesg.body(
                        f"Here's your OrderHistory with Order ID and Product Name 🕙 :\n{orders_list}\n\n➡  8 👉 To view main menu 📃")

                    return str(resp)

                else:
                    mesg.body("You haven't ordered anything ❗\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)

                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        elif msg == "3":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            print(validation)
            company_name = "*FIRST PHARMCY*"
            if validation:
                mesg.body(
                    "Please make sure that you have entered a valid Order_ID\n\nCheck the format\n[Ex-3:900599] 😞\n\n➡  8 👉 To view main menu 📃")
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)

        elif msg.split(":")[0] == "3":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            stat = msg.split(":")[1]
            print(stat)
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            print(validation)
            company_name = "*FIRST PHARMCY*"
            if validation:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "select fp_order.order_id,fp_order_product.name,fp_order_product.quantity,fp_order_product.price,fp_order_product.total,fp_order.date_added,fp_order_status.name from fp_order join fp_order_product on fp_order.order_id = fp_order_product.order_id join fp_order_status on fp_order.order_status_id = fp_order_status.order_status_id  where fp_order.order_id =%s and fp_order.telephone=%s",
                    (stat, phnum,))
                fetchdata = cursor.fetchall()
                if fetchdata:

                    var_fixed = []
                    for row in fetchdata:
                        var_fixed.append(tuple(map(str, tuple(row))))
                    print(var_fixed)
                    keys = ("OrderID", "Product_Name", "Quantity", "Unit_Price", "Total_Price", "Date_time", "Status")
                    data = get_list_of_dict(keys, var_fixed)
                    print(data)
                    orderid1 = list(map(itemgetter('OrderID'), data))
                    orderid = []
                    for i in orderid1:
                        if i not in orderid:
                            orderid.append(i)
                    productname = list(map(itemgetter('Product_Name'), data))
                    Quantitylist = list(map(itemgetter('Quantity'), data))
                    quantity = dict(zip(productname, Quantitylist))
                    Pricelist = list(map(itemgetter('Unit_Price'), data))
                    unit_price = dict(zip(productname, Pricelist))
                    individualtotallist = list(map(itemgetter('Total_Price'), data))
                    test_list = [float(i) for i in individualtotallist]
                    total_price = dict(zip(productname, individualtotallist))
                    print(test_list)
                    total_amount = [sum(test_list)]
                    Date_Time = list(map(itemgetter('Date_time'), data))
                    date_time = []
                    for i in Date_Time:
                        if i not in date_time:
                            date_time.append(i)
                    status_list = list(map(itemgetter('Status'), data))
                    status = []
                    for i in status_list:
                        if i not in status:
                            status.append(i)

                    print(orderid)
                    print(productname)
                    print(quantity)
                    print(unit_price)
                    print(total_price)
                    print(total_amount)
                    print(Date_Time)
                    print(status_list)
                    mesg.body(
                        f"{orderid} Details 🧾 :\n\nOrderID : {orderid}\n\nProduct_Name: {productname}\n\nQuantity: {quantity}\n\nUnit_Price: {unit_price}\n\nTotal_Price Of Product: {total_price}\n\nTotal Amount Of Order: {total_amount}\n\nDate_Time: {date_time}\n\nStatus Of the Order: {status}\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                else:
                    mesg.body(
                        "Please make sure that you have entered a valid Order_ID\n\nCheck the format\n[Ex-3:900599]  😞\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        elif msg == "4":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            company_name = "*FIRST PHARMCY*"
            print(validation)
            if validation:
                mesg.body(
                    "Please make sure that you have entered a valid Order_ID\n\nCheck the format\n[Ex-4:900599] 😞\n\n➡  8 👉 To view main menu 📃")
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with  {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)

        elif msg.split(":")[0] == "4":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            stat = msg.split(":")[1]
            print(stat)
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            print(validation)
            company_name = "*FIRST PHARMCY*"
            if validation:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "select fp_order_status.name  from fp_order join fp_order_status on fp_order.order_status_id = fp_order_status.order_status_id where fp_order.order_id=%s and fp_order.telephone=%s",
                    (stat, phnum,))
                fetchdata = cursor.fetchone()
                print(fetchdata)
                if fetchdata:

                    mesg.body(f"Your Order  {stat} Status 🚚 : {fetchdata[0]}\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                else:
                    mesg.body(
                        "Please make sure that you have entered a valid Order_ID\n\nCheck the format\n[Ex-4:900599] 😞\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with the {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        elif msg == "5":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            fetchdata = cursor.fetchone()
            company_name = "*FIRST PHARMCY*"
            print(fetchdata)
            if fetchdata:
                print(fetchdata[7])
                if phnum == fetchdata[7]:
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "select cf2cu.name, cf2pd.name from fp_coupon as cf2cu join fp_coupon_product as cf2cp on cf2cu.coupon_id=cf2cp.coupon_id join fp_product_description as cf2pd on cf2cp.product_id = cf2pd.product_id")
                    info = cur.fetchall()
                    print(info)

                    if info:
                        info_list = list(info)
                        print(info_list)
                        data_list = '\n\n'.join(str(feature) for feature in info_list)
                        print(data_list)
                        mesg.body(
                            f"You can find coupons for the specific products  🏷 :\n{data_list}\n\nhttps://firstpharmcy.com/\n\n➡  8 👉 To view main menu 📃")
                        return str(resp)
                    else:
                        mesg.body(
                            "We're sorry!! Coupons aren't available at the moment 😞\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with the {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        elif msg == "6":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cur = mysql.connection.cursor()
            cur.execute("select customer_id from fp_customer where telephone = %s or telephone = %s", (phnum, pnum))
            info = cur.fetchall()
            print(info)
            company_name = "*FIRST PHARMCY*"

            if info:

                cur.execute(
                    "select cf2pd.name, cf2p.price, cf2ss.name from fp_product_description as cf2pd join fp_customer_wishlist as cf2cw on cf2pd.product_id= cf2cw.product_id join fp_product as cf2p on cf2pd.product_id = cf2p.product_id join fp_stock_status as cf2ss on cf2p.stock_status_id = cf2ss.stock_status_id where customer_id=%s",
                    (info,))
                info_list = cur.fetchall()
                print(info_list)
                if info_list:
                    var_fixed = []
                    for row in info_list:
                        var_fixed.append(tuple(map(str, tuple(row))))
                    print(var_fixed)
                    keys = ("Product_Name", "Unit_Price", "Stock_Status")
                    data = get_list_of_dict(keys, var_fixed)
                    print(data)
                    data_list = '\n\n'.join(str(feature) for feature in data)
                    print(data_list)
                    mesg.body(f"Your Wishlist 💟 :\n\n{data_list}\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                else:
                    mesg.body("The wishlist is empty ❗\n\n➡  8 👉 To view main menu 📃")
                    return str(resp)
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with the {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
        elif msg == "7":
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone =%s or telephone =%s', (phnum, pnum))
            validation = cursor.fetchone()
            print(validation)
            company_name = "*FIRST PHARMCY*"
            if validation:
                phone = "+919963366913"
                mail = "info@clinicalfirst.com"
                mesg.body(
                    f"Our support team is available to you at :\n\nPhone ☎ :{phone}\nMail 📧 :{mail}\n\n➡  8 👉 To view main menu 📃")
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with the {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)
        else:
            num = request.values.get('From')
            print(num)
            pnum = num.split(":")[1]
            print(pnum)
            phnum = pnum[3:]
            print(type(phnum))
            company_name = "*FIRST PHARMCY*"
            cursor = mysql.connection.cursor()
            cursor.execute('select * from fp_customer where telephone = %s or telephone= %s', (phnum, pnum))
            validation = cursor.fetchone()
            print(validation)
            if validation:
                mesg.body(" 😞 It seems like you have't entered a valid text \n\n➡  8 👉 To view main menu 📃")
                return str(resp)
            else:
                mesg.body(
                    f"Seems you are not registered with the {company_name} 🙁\n\nPlease register with below link 👇\nhttps://firstpharmcy.com/index.php?route=account/register\n\n🤩 You can checkout our offers on all the products 👇\n\nhttps://firstpharmcy.com/specials\n\nWanna Known about health care tips,Do visit our blog 👇\n\nhttps://firstpharmcy.com/index.php?route=extension/simple_blog/article")
                return str(resp)
            return str(resp)

        return str(resp)
    else:
        return 'Hello'







def get_list_of_dict(keys, list_of_tuples):
    list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    return list_of_dict


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
