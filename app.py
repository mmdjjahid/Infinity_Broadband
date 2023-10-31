from flask import Flask, render_template, request, redirect, url_for, flash
import ros_api
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# MikroTik API configuration
API_HOST = '103.93.34.126'
API_USERNAME = 'sof'
API_PASSWORD = 'sof123'
API_PORT = 1122


@app.route('/secret')
def secret():
    pack={
    "5M": "300",
    "6M": "400",
    "7M": "500",
    "10M": "500",
    "12M": "700",
    "15M": "800",
    "20M": "1000",
    "30M": "1500",
    "ARK_5Mbps": "500",
    "ARK_8Mbps": "500",
    "ARK_10Mbps": "500",
    "ARK_12Mbps": "800",
    "ARK_15Mbps": "1000",
    "ARK_20Mbps": "1200",
    "ARK_30Mbps": "1500",
    "ARK_40Mbps": "2000",
    "ARK_50Mbps": "2500",
    }
    packlist= list(pack.items())

    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    
    # Retrieve all ppp
    ppp = api.talk("/ppp/secret/print")

    return render_template('mikusers.html', ppps=ppp, s=packlist)
    

@app.route('/add', methods=['POST'])
def add_ppp():
    # Get form data
    name = request.form['name']
    password = request.form['password']
    description = request.form['description']
    
    profile = request.form['profile']
    address = request.form['address']
    email = request.form['email']
    bill = request.form['bill']
    charge = request.form['charge']
    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    
    # Add new ppp
    api.talk(f'/ppp/secret/add =name={name} =comment={description} =password={password} =profile={profile} =service=pppoe')

    return redirect('/secret')

@app.route('/edit/<ppp_id>', methods=['GET', 'POST'])
def edit_ppp(ppp_id):
    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    

    if request.method == 'POST':
        # Get updated form data

        name = request.form['name']
        password = request.form['password']
        description = request.form['description']
        bill = request.form['bill']
        profile = request.form['profile']
        address = request.form['address']
        email = request.form['email']
        charge = request.form['charge']
        # Update ppp
        api.talk(f'/ppp/secret/set =name={name} =password={password} =profile={profile} =numbers={ppp_id}')

        return redirect('/secret')

    else:
        pack={
        "5M": "300",
        "6M": "400",
        "7M": "500",
        "10M": "500",
        "12M": "700",
        "15M": "800",
        "20M": "1000",
        "30M": "1500",
        "ARK_5Mbps": "500",
        "ARK_8Mbps": "500",
        "ARK_10Mbps": "500",
        "ARK_12Mbps": "800",
        "ARK_15Mbps": "1000",
        "ARK_20Mbps": "1200",
        "ARK_30Mbps": "1500",
        "ARK_40Mbps": "2000",
        "ARK_50Mbps": "2500",
        }
        packlist= list(pack.items())
        # Retrieve ppp details
        ppp = api.talk("/ppp/secret/print")
        us = ""
        for use in ppp:
            if use.get('name') == ppp_id:
                us = use
        return render_template('edit.html', ppp=us, s=packlist)

@app.route('/delete/<ppp_id>', methods=['POST'])
def delete_ppp(ppp_id):
    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    

    # Delete ppp
    api.talk(f'/ppp/secret/remove =numbers={ppp_id}')
    
    # Close API connection
    

    return redirect('/secret')

@app.route('/disable/<ppp_id>', methods=['POST'])
def disable_ppp(ppp_id):
    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    

    # disable ppp
    api.talk(f'/ppp/secret/disable =numbers={ppp_id}')
    
    # Close API connection
    

    return redirect('/secret')


@app.route('/enable/<ppp_id>', methods=['POST'])
def enable_ppp(ppp_id):
    # Connect to MikroTik API
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    

    # enable ppp
    api.talk(f'/ppp/secret/enable =numbers={ppp_id}')
    
    # Close API connection
    

    return redirect('/secret')





@app.route('/active')
def active():
    api = ros_api.Api(API_HOST, user=API_USERNAME, password=API_PASSWORD, port=API_PORT, verbose=False, use_ssl=False)
    return render_template("active.html", q=api.talk('/ppp/active/print'))
    

@app.route('/user_info')
def user_info():

    file_path = 'user_info.csv'
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
   
    return render_template("user_csv.html", q=df)

if __name__ == "__main__":
    app.run(use_reloader=True,debug=True,)
    
