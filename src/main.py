from flask import Flask,render_template, request, session,redirect, url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
import funciones
from Usuarios import Users
import alertas_mensages









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

@app.route("/ResetPassword")
def ResetPassword():
    return render_template("reestablecer_contraseña.html")



@app.route("/RecuperarPassword", methods = ["POST", "GET"])
def RecuperarPassword():
    if request.method  == 'POST':
        email = request.form["correo_electronico"]
        email = funciones.verificar_correo(email)
        if email != None:
            funciones.enviar_email(email)
            flash(alertas_mensages.Mensaje1(),alertas_mensages.CategoriaDeMensaje())
            return redirect(url_for('ResetPassword'))
        else:
            flash(alertas_mensages.mensaje3(),alertas_mensages.CategoriaDeMensaje())
            return redirect(url_for('ResetPassword'))

        

        
    # if request.method  == 'POST':
    #         email = request.form["correo_electronico"]
    #         email = funciones.verificar_correo(email)
    #         if email != None:
    #             funciones.enviar_email(email)
    #             flash(alertas_mensages.Mensaje1(),alertas_mensages.CategoriaDeMensaje())
    #             return redirect(url_for('ResetPassword'))
    #         else:
    #             return redirect(url_for('index'))
    # else:
    #     pass
    



            
  
           




    #         return redirect(url_for('ResetPassword'))
    #     elif email != None:
    #         funciones.verificar_correo(email)
    #         return redirect(url_for('ResetPassword'))
    #     elif email == None:
    #         flash(alertas_mensages.mensaje4(),alertas_mensages.CategoriaDeMensaje())
    #         return redirect(url_for('ResetPassword'))
    #     elif email != None:
    #         flash(alertas_mensages.Mensaje1(),alertas_mensages.CategoriaDeMensaje())
            
    #         return redirect(url_for('ResetPassword'))
    #     else:
    #         return redirect(url_for('ResetPassword'))
    # else:
    #     pass












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


