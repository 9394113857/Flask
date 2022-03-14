from flask import Flask, render_template, request,jsonify
from flask_mysqldb import MySQL
from operator import itemgetter
import pymysql
import socket
import re
import pandas as pd
import datetime
import itertools
current_time = datetime.datetime.now()
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'otp'

local_db = pymysql.connect(host='firstpharmcy.com',
                           user='u3a9uet4oxglm',
                           password='b#@y9b@{83D3',
                           db='db0zx1rnsrwts8')

app.config['MYSQL_HOST'] = 'firstpharmcy.com'
app.config['MYSQL_USER'] = 'u3a9uet4oxglm'
app.config['MYSQL_PASSWORD'] = 'b#@y9b@{83D3'
app.config['MYSQL_DB'] = 'db0zx1rnsrwts8'

mysql = MySQL(app)
ID = "null"
x_text = []
url_list=[]
L1=[]

@app.route('/customerinfo', methods=['GET', "POST"])
def customerinfo():
    req = request.get_json()
    try:
        var = {
            "queryInput": {
                "text": {
                    "text": "END_USER_INPUT"
                },
                "languageCode": "en"
            },
            "queryParams": {
                "timeZone": "America/Los_Angeles"
            }
        }
        global ID
        ID = req.get("text")
        print(ID)
        return (ID)
    except:
        return ("exception occured")

@app.route('/customerdetails', methods=['GET', "POST"])
def customerdetails():
    if request.method=="POST":
        regen = '^[!=a-z]'
        regex = '^[6,7,8,9][0-9]{9}'
        if(re.search(regex,ID) or re.search(regen,ID) ):
            cur = mysql.connection.cursor()
            print("cur")
            cur.execute("select telephone from fp_customer where telephone=%s",(ID,))
            print("excuted")
            mysql.connection.commit()
            fetchdata = cur.fetchone()
            print("fetchdata")
            if fetchdata:
                print(fetchdata)
                if ID == fetchdata[0]:
                    response = {
                        "fulfillment_response": {
                            "messages": [{
                                "payload":
                                    {
                                        "richContent": [
                                            [
                                                {
                                                    "title": "Our Services",
                                                    "color": "#808000",
                                                    "type": "info",
                                                    "subtitle": "Please choose one of the services below👇👇."
                                                },
                                                {
                                                    "type": "chips",
                                                    "options": [
                                                        {
                                                            "text": [
                                                                "Order Tracking🚛"
                                                            ]
                                                        },
                                                        {
                                                            "text": [
                                                                "My Orders🧺"
                                                            ]
                                                        },
                                                        {
                                                            "text": [
                                                                "Notifications🔔"
                                                            ]
                                                        },
                                                        {
                                                            "text": [
                                                                "Support👩💻"
                                                            ]
                                                        }

                                                    ]
                                                }
                                            ]
                                        ]
                                    }
                            }]
                        }
                    }
                    return response
            else:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "type": "description",
                                                "title": "📱Mobile Number Varification status",
                                                "text": [
                                                    "Sorry😔 it seems like you are not registered with us. if you want to use the service you have to register with firstpharmacy Ecommerce website"]
                                            },
                                            {
                                                "event": {
                                                    "name": "firstpharmacyEcommerce Website Link🔗👇",
                                                    "languageCode": "en"
                                                },
                                                "type": "button",
                                                "link": "https://firstpharmcy.com/index.php?route=account/register",
                                                "text": "firstpharmacy websitelink🔗👇",
                                                "icon": {
                                                    "type": "chevron_right",
                                                    "color": "#FF9800"
                                                }
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
            return response
        else:
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Phone number validation👇",
                                            "text": ["After refreshing the website, please enter a valid mobile number.😊"]
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            return response
    else:
        return ("exception occured")

@app.route('/customerconformation', methods=['GET', "POST"])  # URL pattern
def customerconformation():
    req = request.get_json()
    try:
        global ID
        print(ID)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            P_D = '"' + ID + '"'
            P_D = ''.join('(' + P_D + ')')
            print(P_D)
            cur.execute("select order_id from fp_order as fpo inner join fp_customer as fpc on fpo.customer_id = fpc.customer_id where fpc.telephone in" +P_D)
            print("cur")
            mysql.connection.commit()
            info = cur.fetchall()
            print(info)
            cur.close()
            if info:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "title": "Orders List📃",
                                                "type": "info",
                                                "subtitle": "select particular Order Id which you want to track the details from the given OrderIds👇"
                                        },
                                        {
                                            "type": "chips",
                                            "options": [

                                            ]
                                        }
                                    ]
                                ]
                            }
                        }]
                    }
                }
                for i in info:
                    response['fulfillment_response']['messages'][0]['payload']['richContent'][0][1]['options'].append(
                    {'text': i})
            # time.sleep(3)
                return response
            else:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "type": "description",
                                                "title": "order details👇",
                                                "text": ["Currently, you haven't ordered any products yet.😞"]
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                return response

        #return jsonify('tests added successfully')
    except:
        return ("exception occured")

@app.route('/order_tracking', methods=["POST"])
def order_tracking():
    req = request.get_json()
    try:
        status = req.get("text")
        print(status)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            order_id = '"' + status + '"'
            order_id = ''.join('(' + order_id + ')')
            print(order_id)
            cur.execute("SELECT cf2os.name from fp_order  join fp_order_status as cf2os on fp_order.order_status_id = cf2os.order_status_id WHERE order_id  in" + order_id)
            print("executed")
            mysql.connection.commit()
            info = cur.fetchone()
            print(info)
            info1 =info[0]
            symbol="🚚"
            info_list= "{} {}".format(info1,symbol)
            print(info_list)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Here is the status of your selected order👇",
                                            "text": []
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }

            response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(info_list)
            #time.sleep(3)
            return response
        return jsonify('tests added successfully')
    except:
        return "Exception occure"


@app.route('/orderhistory', methods=['GET', "POST"])
def orderhistory():
    try:
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            P_D = '"' + ID + '"'
            P_D = ''.join('(' + P_D + ')')
            print(P_D)
            cur.execute("select order_id from fp_order as cfo inner join fp_customer as cfc on cfo.customer_id = cfc.customer_id where cfc.telephone in" +P_D)
            print(cur)
            mysql.connection.commit()
            info = cur.fetchall()
            print(info)
            cur.close()
            if info:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "title": "Orders List📃",
                                                "type": "info",
                                                "subtitle": "select particular Order Id which you want to know the details from the given OrderIds👇👇"
                                            },
                                            {
                                                "type": "chips",
                                                "options": [

                                                ]
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                for i in info:
                    response['fulfillment_response']['messages'][0]['payload']['richContent'][0][1]['options'].append(
                    {'text': i})
            # time.sleep(3)
                return response
            else:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "type": "description",
                                                "title": "order details👇",
                                                "text": ["Currently, you haven't ordered any products yet.😞"]
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                return response
    except:
        return ("exception occured")

@app.route('/orderinfo', methods=["POST"])
def orderinfo():
    req = request.get_json()
    try:
        status = req.get("text")
        print(status)
        if request.method == "POST":
            cur = mysql.connection.cursor()
            print("cur")
            order_id = '"' + status + '"'
            order_id = ''.join('(' + order_id + ')')
            print(order_id)
            cur.execute("select fp_order.order_id,fp_order_product.name,fp_order_product.quantity,fp_order_product.price,fp_order_product.total,fp_order.date_added, cf2os.name from fp_order join fp_order_product on fp_order.order_id = fp_order_product.order_id join fp_order_status as cf2os on fp_order.order_status_id = cf2os.order_status_id where fp_order.order_id in" + order_id)
            print("executed")
            mysql.connection.commit()
            fetchdata = cur.fetchall()
            print(fetchdata)
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

            details =(f"OrderID : {orderid}\n\nProduct_Name: {productname}\n\nQuantity: {quantity}\n\nUnit_Price: {unit_price}\n\nTotal_Price Of Product: {total_price}\n\nTotal Amount Of Order: {total_amount}\n\nDate_Time: {date_time}\n\nStatus Of the Order: {status}")
            print(details)
            cur.close()
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Here is the order details of your selected order👇",
                                            "text": []
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(details)
            #time.sleep(3)
            return response
        return jsonify('tests added successfully')
    except:
        return "Exception occure"

def get_list_of_dict(keys, list_of_tuples):
    list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
    return list_of_dict

@app.route('/coupons', methods=["POST"])
def coupons():
    if request.method=="POST":
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
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "these are the coupons which are available for the particular products and here is the link for Ecommerece website to utilize those coupons👇👇",
                                            "text": []
                                        },
                                        {
                                            "event": {
                                                "name": "firstpharmacyEcommerce Website",
                                                "languageCode": "en"
                                            },
                                            "type": "button",
                                            "link": "https://firstpharmcy.com/",
                                            "text": "firstpharmacy",
                                            "icon": {
                                                "type": "chevron_right",
                                                "color": "#FF9800"
                                            }
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(data_list)
            # time.sleep(3)
            return response
        #return jsonify('tests added successfully')
        else:
            response = {
                "fulfillment_response": {
                    "messages": [{
                        "payload":
                            {
                                "richContent": [
                                    [
                                        {
                                            "type": "description",
                                            "title": "Here is the status for the coupons service👇",
                                            "text": ["STAY TUNED WITH US TO GET AMAZING COUPONS"]
                                        }
                                    ]
                                ]
                            }
                    }]
                }
            }
            return response
            #return "Exception occure"

@app.route('/wishlist', methods=["POST"])
def wishlist():
    if request.method=="POST":
        cur = mysql.connection.cursor()
        cur.execute("select customer_id from fp_customer where telephone=%s", (ID,))
        info = cur.fetchall()
        print(info)
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
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "type": "description",
                                                "title": "Here is the information regarding your wishlist📃👇",
                                                "text": []
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                response['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['text'].append(data_list)
                return response
            else:
                response = {
                    "fulfillment_response": {
                        "messages": [{
                            "payload":
                                {
                                    "richContent": [
                                        [
                                            {
                                                "type": "description",
                                                "title": "Here is the status of your wishlist👇",
                                                "text": ["Sorry😔  it seems like you haven't added any products in your wishlist."]
                                            }
                                        ]
                                    ]
                                }
                        }]
                    }
                }
                return response
                #return "Exception occure"


if __name__ == '__main__':
    app.run(debug=True)

