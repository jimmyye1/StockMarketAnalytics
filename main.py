from flask import Flask, render_template
from flask import jsonify
import yfinance as yf

app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append([num, coin_lookup[coin]])

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append([num,coin_lookup[coin]])
    return res

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

tick=['qqq','spy','iwm','xbi','aapl','msft']


# qqq=yf.Ticker('qqq')
# p_qqq = qqq.history(interval='1m', start="2021-01-01")['Close']

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')
import io
from io import BytesIO
import base64


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    spy=yf.Ticker('spy')
    pr = spy.history(interval='1d', period='3y').Close
    img = pr.plot().get_figure()
    # https://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask
    buf = io.BytesIO()
    img.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    b2 = base64.b64encode(buffer)
    plotx = b2.decode('utf-8')
    return render_template('home.html', pts = posts, plotx=plotx)

@app.route('/echo/<name>')
def echo(name):
    print(f"This was placed in the url: new-{name}")
    val = {"I Love You": name}
    return jsonify(val)

@app.route('/change/<dollar>.<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    print(type(result))
    print(result)
    return render_template("change.html", result = result, amount=amount, title="Money")
#    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
