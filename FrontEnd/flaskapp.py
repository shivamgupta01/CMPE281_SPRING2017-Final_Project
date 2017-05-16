from flask import Flask, render_template, json, request, redirect
from flask.ext.mysql import MySQL
from flask import session
from flask import (render_template, redirect,
                   url_for, request,make_response)
import json
import os

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'cmpe281'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root1234'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'mydbinstance.cnqobngvit0z.us-west-2.rds.amazonaws.com'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('test.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/userHome')
def userHome():

    if session.get('user'):
        return
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateInput', methods=['POST', 'GET'])
def homePage():
    try:
        _Name = request.form['Name']
        _DOB = request.form['DOB']
        _PlateNo = request.form['PlateNo']
        _Zip_Code = request.form['Zip_Code']
        _Experience = request.form['Experience']
        _Mileage = request.form['Mileage']
        _Gender = request.form['Gender']
        _Marital_Status = request.form['Marital_Status']

        _DOB = int(_DOB[:4])
        _age = 2017 - _DOB

        if _Gender == "female":
            _intGender = 1
        else:
            _intGender = 2

        if _Marital_Status == "Married":
            _intMaritalStatus = 1
        else:
            _intMaritalStatus = 2

        #temp = formatInput(_age,3,int(_Experience),int(_Zip_Code),int(_Mileage),int(_intGender),int(_intMaritalStatus))
        temp = ""
        print "temp "
        print temp[0]
        if temp[0] == 1:
            #progressColor = "progress-bar progress-bar-success"
            risk = 30
            riskp = "width:30%"
            text = "Low Risky"
        elif temp[0] == 2:
            #progressColor = "progress-bar progress-bar-warning"
            risk = 60
            riskp = "width:60%"
            text = "Moderate Risky"
        elif temp[0] == 3:
            #progressColor = "progress-bar progress-bar-danger"
            risk = 90
            riskp = "width:90%"
            text = "High Risky"

        DMVScore = temp[1]
        CreditScore = temp[2]
        VehicleScore = temp[3]

        return render_template('Output.html', name = _Name, risk = risk, riskp = riskp,text = text, dmvScore = DMVScore,cScore=CreditScore,vScore = VehicleScore,Mileage = _Mileage, Exp = _Experience)


    except Exception as e:
        return json.dumps({'error': str(e)})



@app.route('/validateDriverInput', methods=['POST', 'GET'])
def validateDriverInput():
    try:
        print "------- INSIDE -----"
        _Name = request.form['select']
    except Exception as e:
        return json.dumps({'error': str(e)})

def getURLFromShivam(finalCommunity):
    return "http:google.com"

@app.route('/save', methods=['POST'])
def save():
    finalCommunity = "cNone"
    print dict(request.form.items())
    baseLocation = ""
    baseLocation = dict(request.form.items()).get('baseLocation')
    communityName = dict(request.form.items()).get('communityName')
    finalCommunity = baseLocation + "/" + communityName
    print finalCommunity
    url = getURLFromShivam(finalCommunity)
    insertIntoDB(finalCommunity,url)
    response = make_response(redirect(url_for('builder')))
    return response


@app.route('/searchRes', methods=['POST'])
def searchRes():
    with open("communityData.txt", "r+") as f:
        fileContent = f.read()
        jsonDataDict = {'OSSN': 'google.com'}
        if os.path.getsize("communityData.txt") > 0:
            jsonDataDict = json.loads(fileContent)
    selectedOssn = dict(request.form.items()).get('searchForm')
    url = jsonDataDict.get(selectedOssn)
    print url
    response = make_response(redirect(url_for('builder')))
    return response


def saveWordsToFile(path, url):
    with open("communityData.txt", "r+") as f:
        fileContent = f.read()
        jsonDataDict = {}
        if os.path.getsize("communityData.txt") > 0:
            jsonDataDict = json.loads(fileContent)

        jsonDataDict[path] = url

        f.seek(0)
        json_data = json.dumps(jsonDataDict, encoding='ascii')
        f.write(json_data)
        f.truncate()


def insertIntoDB(finalCommunity,url):
    con = mysql.connect()
    cursor = con.cursor()
    id = 1

    query1 = ("INSERT INTO CopmmunityData2 "
          "(id, data, url) "
          "VALUES (%s, %s, %s)")
    data_query1 = (id, finalCommunity, url)
    cursor.execute(query1, data_query1)
    cursor.execute("commit")


def checkAllFromDB():
    print "hell"
    list = []
    con = mysql.connect()
    cursor = con.cursor()
    query = ("SELECT * FROM CopmmunityData2 ")
    cursor.execute(query)
    for row in cursor.fetchall():
        checkFlag = 1
        print row[0]
        print row[1]
        print row[2]
        list.append(row[1])
    return list

@app.route('/builder')
def builder():
    return render_template("layout.html")


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()

        list = []
        list = checkAllFromDB()
        query = ("SELECT * FROM tbl_user "
                 "WHERE user_username = %s")

        cursor.execute(query, _username)

        for row in cursor.fetchall():
            user1 = row[1]
            Val = row[3]

        print str(Val)
        print str(_password)
        if Val:
            if str(Val) == str(_password):
                session['user'] = user1
                return render_template('UserHomeTest.html',name=user1,savedList = list)
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')




    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5004,debug=True)
