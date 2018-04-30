## Author: Victor Dibia
## Serves up the SkyFall Game

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, )


@app.route("/")
def hello():
    return render_template('mousecontrol.html')


@app.route("/hand")
def test():
    return render_template('handcontrol.html')
 

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#  Allow external access using host 0.0.0.0 address.
if __name__ == '__main__':
    app.config['APPLICATION_ROOT'] = "/static"
    app.run(host='0.0.0.0', debug=True, port=5005)
