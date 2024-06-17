from basedatos import iniciar_conexion



def Iniciar_Sesion(correo):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT *FROM ingreso_quimica WHERE correo_electronico=%s",(correo))
        regitro = cursor.fetchone()
        return regitro
    
def registrar_usuario(email,password):
    conexion = iniciar_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO ingreso_quimica(correo_electronico, password) VALUES (%s,%s)",(email,password)) 
        conexion.commit()
        conexion.close()





    
