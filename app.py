import openfoodfacts.products
from flask import Flask,render_template, request,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap
#from PIL import Image
#from pytesseract import pytesseract
import mysql.connector
import requests
import json
import base64
import io
import pyodbc
app = Flask(__name__,template_folder='templates',static_folder='static')
CORS(app)
Bootstrap(app)

# Yan bai has come


# Obtain connection string information from the portal
cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:foodallergyserver.database.windows.net,1433;"
            "Database=foodallergydb;"
            "UID=sagar_kudale;"
            "PWD=#Siddhivinayak123;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
            )

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testdemo'

mysql = MySQL(app)

selected_allergens = []

@app.route('/')
def HomePagev():
    opening_slogan = 'As a Parent of Children with Food Allergies,\nShopping Has Never been Easier!'
    sub_slogan = "Find out if the Food product you want to buy or use is suitable for your children by scanning"\
            " the product's barcode. Also, see different possible food substitutions that is safe from your child's allergy reaction."
    button_txt="Click to Start!"
    return render_template('home-v2.html',result = opening_slogan, subsl= sub_slogan,
                           btn_txt = button_txt)


@app.route('/options',endpoint='options')
def get_options():
    return render_template("options.html")


@app.route('/aboutus',endpoint='aboutus')
def get_aboutus():
    return render_template("about_us.html")


@app.route('/details',endpoint='details')
def get_allergy_details():
    return render_template("allergy_details.html")


@app.route('/Food_sub',endpoint='Food_sub')
def get_food_sub():
    return render_template("Food_sub.html")

@app.route('/wheat',endpoint='wheat')
def get_wheat():
    return render_template("wheat.html")

@app.route('/dairy',endpoint='dairy')
def get_dairy():
    return render_template("dairy.html")

@app.route('/egg',endpoint='egg')
def get_egg():
    return render_template("egg.html")

@app.route('/shellfish',endpoint='shellfish')
def get_shellfish():
    return render_template("shellfish.html")

@app.route('/soy',endpoint='soy')
def get_soy():
    return render_template("soy.html")

@app.route('/sesame',endpoint='sesame')
def get_sesame():
    return render_template("sesame.html")

@app.route('/treenut',endpoint='treenut')
def get_treenut():
    return render_template("treenut.html")

@app.route('/peanut',endpoint='peanut')
def get_peanut():
    return render_template("peanut.html")



@app.route('/getstudentdetails', methods=['GET'],endpoint='getStudentDetails')
def getStudentDetails():
    if request.method == 'GET':
        print("hello world")
        allergens = []
        cnxn = pyodbc.connect(cnxn_str)
        cursor = cnxn.cursor()
        """ list = []
        #dict = {"name": "jane doe", "salary": 9000, "email": "JaneDoe@pynative.com"}
        select_sql = "SELECT * FROM student"
        res = cursor.execute(select_sql)
        print(type(res))
        for ele in res:
            list.append(ele[1])
        print(cursor.fetchall())
        """
        demo = ["dairy", "wheat"]
       # in_params = ','.join(['%s'] * len(demo))
        #sql = "SELECT allergen_name,alternative_name FROM alternative_allergen_name WHERE allergen_name IN (%s)" % in_params
        #sql = "SELECT allergen_name,alternative_name FROM alternative_allergen_name WHERE allergen_name = 'dairy' "
        #cursor.execute(sql,demo)
        #myallergens = cursor.fetchall()

        execu = cursor.execute(
            """
            Select 
             allergen_name,
             alternative_name
            From
                alternative_allergen_name
            where
             allergen_name in ({})
            """.format(','.join("?" * len(demo))), demo)

        myallergens = cursor.fetchall()

        for x, y in myallergens:
            allergens.append(y)
        #dict['name'] = list
        response = jsonify({
            "result": allergens
        })
        return response


@app.route('/form',methods=['GET'],endpoint='form')
def form():
    code = '5000396015935'
    temp_url = "https://world.openfoodfacts.org/api/v0/product.json"
    url = '/'.join([temp_url, code])
    myResponse = requests.get(url, verify=True)
    # print (myResponse.status_code)

    # For successful API call, response code will be 200 (OK)
    if (myResponse.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)

        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        print(jData)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()
    pro = openfoodfacts.products.get_product('5000396015935')
    print(type(pro['product']['ingredients_hierarchy']))
    return str(pro['product']['ingredients_hierarchy'])

@app.route('/barcode_post', methods=['POST','GET'],endpoint='barcode_post')
@cross_origin()
def get_barcode_post():
    #if (request.method == 'POST'):
    print(selected_allergens)
    barcode = request.json
    print(barcode)
    barcode_data = barcode['barcode']
    code_id = barcode_data
    temp_url = "https://world.openfoodfacts.org/api/v0/product.json"
    url = '/'.join([temp_url, code_id])
    myResponse = requests.get(url, verify=True)
    # print (myResponse.status_code)

    # For successful API call, response code will be 200 (OK)
    if (myResponse.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)

        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        print(jData)

    else:
        # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

    alternate_allergens = getAllergendata()
    barcode_allergens = jData['product']['ingredients_hierarchy']

    barcode_allergens = [x.split(':')[1] for x in barcode_allergens]
    print(barcode_allergens)
    result = ""
    for barllergen in barcode_allergens:
        if barllergen in alternate_allergens:
            return jsonify({"result":"Avoid having the product"})
            #result = "Avoid having the product"
    result = "go ahead and have the product"
            #return "Avoid having the product"
    #return "go ahead and have the product"
    response = jsonify({
        "result": result
    })
    return response

    #return jData['product']['ingredients_hierarchy']

def getAllergendata():
    allergens = []
    demo = ["dairy","wheat"]
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    #cursor = mysql.connection.cursor()
    #in_params = ','.join(['%s'] * len(selected_allergens))
    #sql = "SELECT allergen_name,alternative_name FROM alternative_allergen_name WHERE allergen_name IN (%s)" % in_params
    #cursor.execute(sql, selected_allergens)
    #cursor.execute('''SELECT allergen_name FROM alternative_allergen_name WHERE allergen_name IN (%s)'''% in_params)
    execu = cursor.execute(
        """
        Select 
         allergen_name,
         alternative_name
        From
            alternative_allergen_name
        where
         allergen_name in ({})
        """.format(','.join("?" * len(selected_allergens))), selected_allergens)
    selected_allergens.clear()
    #selected_allergens = []
    #myallergens = cursor.fetchall()
    myallergens = cursor.fetchall()
    print(myallergens)
    for x,y in myallergens:
        allergens.append(y)
    print(allergens)
    cursor.close()
    return allergens
    #return allergens

@app.route('/user_allergies', methods=['POST'])
@cross_origin()
def user_allergies_post():
    if request.method == 'POST':
        user_allergies = request.json
        print(user_allergies)
        for ele in user_allergies['allergies']:
            if ele['Checked'] == True:
                selected_allergens.append(ele['Name'])
    print(selected_allergens)
    return "none"



