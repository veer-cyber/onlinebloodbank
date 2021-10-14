from flask import render_template

from project import app


@app.route('/user/loadContact')
def userLoadContact():
    try:
        return render_template('user/contact.html')
    except Exception as ex:
        print(ex)
