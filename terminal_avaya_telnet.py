# script para conexion a Avaya Communication Manager 6.2.1
# Protocol: Telnet

import telnetlib

# Settings Generales

avaya_server = '10.85.123.110'
avaya_port   = '5023'
user_cm      = 'mgomez\n'
pass_cm      = 'Conmutador1#\n'

command = 'cdisplay policy 9\n'


tn_cm = telnetlib.Telnet(avaya_server, avaya_port) # conexion a CM Avaya Port 5023
tn_cm.read_until('login'.encode())                 # Espera string 'login'
tn_cm.write(user_cm.encode())                      # Envia user valido en CM Avaya
tn_cm.read_until('Password'.encode())              # Espera string 'Password' 
tn_cm.write(pass_cm.encode())
tn_cm.read_until('Terminal'.encode())              # Espera string 'Terminal'
tn_cm.write('ossi\n'.encode())                    # Envia Terminal ossit (avaya)
tn_cm.read_until('t\n'.encode())                   # Espera caracter t finalizacion login

# Terminal lista para recibir comando a ejecutar

tn_cm.write(command.encode())                      # Envia comando Avaya cm 
tn_cm.write('t\n'.encode())                        # Envia caracter t finalizacion comando
out_command = tn_cm.read_until('t\n'.encode())     # Recibe data arrojada por comando
out_command = out_command.decode('utf-8')          # Format a Resultado comando ejecutado
tn_cm.close()                                      # Cierra Session Telnet Terminal CM avaya

# Separa lineas con Datos de Campos que arroja comando
# y lineas con Datos que arroja el comando.

fields = {}                                        # Campos del reporte Salida Comando
data = {}                                          # Datos  del reporte Salida Comando
lines = out_command.split('\n')                    # Crea lista con lineas de salida comando
for line in lines:                                 # Lee linea por linea de salida de comando
    if line.startswith('d'):                       # Busca lineas de Datos
        data.update({
            len(data): line[1:]                    # Actualiza directorio con Datos de Comando
	})
    elif line.startswith('f'):                     # Busca lineas de Campos
        fields.update({
	    len(fields): line[1:]                      # Actualiza directorio de Campos 
	})
    elif line.startswith('t'):                     # Busca lineas con Caracter t (terminate)
        break

    else:                                          # omite cualquier linea diferente.
        pass


# Arma directorio con datos de Campos y Data  del comando ejecutado

parse = {

    'fields': fields,
    'data': data,

}

