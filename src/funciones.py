from basedatos import iniciar_conexion
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.message import EmailMessage
from main import app
from flask import url_for



def Iniciar_Sesion(correo):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT *FROM ingreso_quimica WHERE correo_electronico=%s",(correo))
        regitro = cursor.fetchone()
        return regitro
        
def registrar_usuario(email,password):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:cursor.execute("INSERT INTO ingreso_quimica(correo_electronico, password) VALUES (%s,%s)",(email,password)) 
    conexion.commit()
    conexion.close()


def verificar_correo(correo):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT  correo_electronico  FROM ingreso_quimica WHERE correo_electronico=%s",(correo))
        regitro = cursor.fetchone()
        return regitro
    
def TOKEN(token):
    token_expired = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = token_expired.loads(token, salt='email-confirmacion-salt',max_age=20)  
    return email

    
        
def enviar_email(email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    confir_url = url_for('ResetPassword',token = confirm_serializer.dumps(email,salt='email-confirmacion-salt'), _external =True)
    remitente = "javieraugustosanchezmartinez@gmail.com"
    destinatario = email
    mensaje = f"holaaaa\n{confir_url}"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "recupere su contraseña aqui"
    email.set_content(mensaje)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(remitente,"ifjuomcczvhwupmf")
    server.sendmail(remitente,destinatario,email.as_string())

def cambio_contraseña(NuevaPassword,email):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET password =%s WHERE correo_electrónico =%s",(NuevaPassword,email))
        conexion.commit()
        conexion.close()


    
