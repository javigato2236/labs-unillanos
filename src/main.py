from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/iniciar_sesion")
def ini_sesion():
    return render_template("iniciar_sesion.html")






if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")


