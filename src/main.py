from flask import Flask,render_template, request, session,redirect, url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
import funciones
from Usuarios import Users
import alertas_mensages
from itsdangerous import SignatureExpired









app = Flask(__name__,template_folder="./templates")
app.secret_key = "abcd123"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ventana_inicio_sesion")
def ini_sesion():
    return render_template("iniciar_sesion.html")

@app.route("/ventana_registro")
def registro():
    return render_template("registro_prueba.html")

@app.route("/ver_registros1")
def registro1():
    return render_template("registros1.html")

@app.route("/quimica")
def quimica():
    return render_template("quimica.html")

@app.route("/ResetPassword/<token>", methods = ["POST", "GET"] )
def ResetPassword(token):
    try:
        email = funciones.TOKEN(token)
        return render_template("ingreso_nueva_contraseña.html", email = email )
    except: SignatureExpired
    return "lo sentimos el token espíro"
    

@app.route("/ VentanaResetPassword")
def VentanaResetPassword():
    return render_template("reestablecer_contraseña.html")




@app.route("/RecuperarPassword", methods = ["POST", "GET"])
def RecuperarPassword():
    if request.method  == 'POST':
        email = request.form["correo_electronico"]
        email = funciones.verificar_correo(email)
        if email != None:
            funciones.enviar_email(email)
            flash(alertas_mensages.Mensaje1(),alertas_mensages.CategoriaDeMensaje())
            return redirect(url_for('VentanaResetPassword'))
        else:
            flash(alertas_mensages.mensaje3(),alertas_mensages.CategoriaDeMensaje())
            return redirect(url_for('VentanaResetPassword'))
        

@app.route("/cambio_contraseña", methods = ["POST", "GET"])
def cambio_contra():
    if request.method == "POST":
        email = request.form["id"]
        NuevaPassword = request.form["nueva_password"]
        ConfirmarPassword = request.form["confirmar_password"]
        if NuevaPassword == ConfirmarPassword:
            NuevaPassword = generate_password_hash(request.form["nueva_password"])
            funciones.cambio_contraseña(NuevaPassword,email)
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('reset_pass'))
    else:
        return redirect(url_for('reset_pass'))

        

        
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method =="POST" and "correo_electronico" in request.form and "password" in request.form:
        usuario =Users(request.form["correo_electronico"],request.form["password"])
        registro = funciones.Iniciar_Sesion(usuario.correo)
        if registro:
            if check_password_hash(registro[2],usuario.password):
                session["login"] = True
                session["id"] = registro[0]
                session["password"] = registro[2]
                return render_template("quimica.html", registro = registro)
            else:
                return render_template("iniciar_sesion.html")
        else:
            return render_template("iniciar_sesion.html")
    else:
        render_template("iniciar_sesion.html")  


@app.route("/logout")        
def logout_sesion():
    session.clear()
    return redirect((url_for('index')))
 

@app.route("/registro_login", methods = ["POST", "GET"])
def registro_log():
    if request.method  == 'POST':
        usuario = Users(request.form["correo_electronico"],generate_password_hash(request.form["password"]))
        try:
            funciones.registrar_usuario(usuario.correo,usuario.password)
        except:
            return render_template("index.html")
        finally:
            return render_template("index.html")    
        

        
        


if __name__=="__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")


