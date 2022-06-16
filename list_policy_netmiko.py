# Script Python to Connect SSH Avaya Lib Netmiko
#
# Author: Mario Gomez

from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

# Test commmand Avaya SSH

command_1 = 'clist policy\r'
command = 'cdisplay policy 20\r'

# Connect to Terminal SSH Avaya

# Set parameters connection 
net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="10.85.123.110",
    username="mgomez",
    password=getpass(),
)
# nuevo cm : 10.86.98.104 , ESS: 
output = net_connect.send_command(
    command_string='sat',
    expect_string=r"Terminal",
    strip_prompt=False,
    strip_command=False

)

# Connect to terminal ossi

output += net_connect.send_command(
    command_string='ossi\n',
    expect_string=r"t\n",
    strip_prompt=False,
    strip_command=False

)
# Send Command to Avaya SSH
output_command = net_connect.send_command_timing(
    command_string= command,
    strip_prompt=False,
    strip_command=False

)

output_command += net_connect.send_command(
    command_string='t\n',
    expect_string=r"t\n",
    strip_prompt=False,
    strip_command=False

)
# show command result
print(output_command)
net_connect.disconnect()

# Separa lineas con data y con fields, Crea directorio fields y data


fields = {}                               # Campos del reporte Salida Comando
data = {}                                 # Datos  del reporte Salida Comando
lines = output_command.split('\n')           # Crea lista con lineas de salida comando

for line in lines:                                   
    if line.startswith('d'):              # Busca Lineas de data
        data.update({
            len(data): line[1:]           # Actualiza directorio data
    })
    elif line.startswith('f'):            # Busca lineas de fields
        fields.update({
        len(fields): line[1:]             # Actualiza directorio fields 
    })
    elif line.startswith('t'):            # Busca lineas con Caracter t (terminate)
        break

    else:                                 # omite cualquier linea diferente.
        pass
        

# crea directorio con fields(addres) data(datos) del comando ejecutado

parse = {
    'fields': fields,
    'data'  : data,
}

# Show data result formated in json file 
pprint(parse)
print()
print('line_data:   ', len(data))
print('line_fields: ', len(fields))
print()