# script para conexion a Avaya Communication Manager 6.2.1
# Protocol: Telnet

import telnetlib
from pprint import pprint

# Settings Generales

avaya_server = '10.85.123.110'
avaya_port   = '5023'
user_cm      = 'mgomez\n'
pass_cm      = 'Conmutador1#\n'

command_1 = 'cdisplay vect 305\n'
command = 'cdisplay pol 29\n'
# Login a Terminal
tn_cm = telnetlib.Telnet(avaya_server, avaya_port) # conexion a CM Avaya Port 5023
tn_cm.read_until('login'.encode())                 # Espera string 'login'
tn_cm.write(user_cm.encode())                      # Envia user valido en CM Avaya
tn_cm.read_until('Password'.encode())              # Espera string 'Password' 
tn_cm.write(pass_cm.encode())
tn_cm.read_until('Terminal'.encode())              # Espera string 'Terminal'
tn_cm.write('ossi\n'.encode())                     # Envia Terminal ossit (avaya)
tn_cm.read_until('t\n'.encode())                   # Espera caracter t finalizacion login

# Terminal lista para recibir comando a ejecutar

tn_cm.write(command.encode())                      # Envia comando Avaya cm 
tn_cm.write('t\n'.encode())                        # Envia caracter t finalizacion comando
out_command = tn_cm.read_until('t\n'.encode())     # Recibe data arrojada por comando
out_command = out_command.decode('utf-8')          # Format a Resultado comando ejecutado
tn_cm.close()                                      # Cierra Session Telnet Terminal CM avaya

# Separa lineas con data y con fields, Crea directorio fields y data


fields = {}                                        # Campos del reporte Salida Comando
data = {}                                          # Datos  del reporte Salida Comando
lines = out_command.split('\n')                    # Crea lista con lineas de salida comando

for line in lines:                                   
    if line.startswith('d'):                       # Busca Lineas de data
        data.update({
            len(data): line[1:]                    # Actualiza directorio data
    })
    elif line.startswith('f'):                     # Busca lineas de fields
        fields.update({
        len(fields): line[1:]                      # Actualiza directorio fields 
    })
    elif line.startswith('t'):                     # Busca lineas con Caracter t (terminate)
        break

    else:                                          # omite cualquier linea diferente.
        pass
        

# crea directorio con fields(addres) data(datos) del comando ejecutado

parse = {
    'fields': fields,
    'data'  : data,
}

pprint(parse)
print()
print('line_data:   ', len(data))
print('line_fields: ', len(fields))
print()


# crea directorio map con key=address, Value=dato

mapeo = {}                                          # diccionario que almacena direcciones memoria-Vs-Data

for i in range(len(parse['fields'])):               # Explora directorio de campos linea x linea
    fids = parse['fields'][i].split('\t')           # crea lista con direcciones de memoria
    dids = parse['data'][i].split('\t')             # crea lista con data en misma posicion de memoria
    for j in range(len(fids)):                      # crea relacion memoria: data
        mapeo.update({
            fids[j]: dids[j]
            })

pprint(mapeo)

# crea dictionario con datos de resultado comando:
# display policy x (x numero de policy)

addr = {
    
      0 : {
         'number' : '7800ff01',
         'name' : '8003ff01',
         'type' : '7801ff01',
         'period' : '7802ff01',        
           },

      1 : { 
         'route_to_vdn' : '7808ff01', 
         'vdn_name' : '7809ff01',
         'target' : 'f816ff01',
         'actual_percent_int' : '780aff01',
         'actual_percent_dec' : '780cff01', 
         'actual_priority' : '780dff01',   
         'call_counts' : '780bff01',              
           },

      2  : { 
         'route_to_vdn' : '7808ff02', 
         'vdn_name' : '7809ff02',
         'target' : 'f816ff02',
         'actual_percent_int' : '780aff02',
         'actual_percent_dec' : '780cff02', 
         'actual_priority' : '780dff02',   
         'call_counts' : '780bff02',              
           },

      3  : { 
         'route_to_vdn' : '7808ff03', 
         'vdn_name' : '7809ff03',
         'target' : 'f816ff03',
         'actual_percent_int' : '780aff03',
         'actual_percent_dec' : '780cff03', 
         'actual_priority' : '780dff03',   
         'call_counts' : '780bff03',              
            },

      4  : { 
         'route_to_vdn' : '7808ff04', 
         'vdn_name' : '7809ff04',
         'target' : 'f816ff04',
         'actual_percent_int' : '780aff04',
         'actual_percent_dec' : '780cff04', 
         'actual_priority' : '780dff04',   
         'call_counts' : '780bff04',              
            },

      5  : { 
         'route_to_vdn' : '7808ff05', 
         'vdn_name' : '7809ff05',
         'target' : 'f816ff05',
         'actual_percent_int' : '780aff05',
         'actual_percent_dec' : '780cff05', 
         'actual_priority' : '780dff05',   
         'call_counts' : '780bff05',              
            },

      6  : { 
         'route_to_vdn' : '7808ff06', 
         'vdn_name' : '7809ff06',
         'target' : 'f816ff06',
         'actual_percent_int' : '780aff06',
         'actual_percent_dec' : '780cff06', 
         'actual_priority' : '780dff06',   
         'call_counts' : '780bff06',              
            },

      7  : { 
         'route_to_vdn' : '7808ff07', 
         'vdn_name' : '7809ff07',
         'target' : 'f816ff07',
         'actual_percent_int' : '780aff07',
         'actual_percent_dec' : '780cff07', 
         'actual_priority' : '780dff07',   
         'call_counts' : '780bff07',              
            },

      8  : { 
         'route_to_vdn' : '7808ff08', 
         'vdn_name' : '7809ff08',
         'target' : 'f816ff08',
         'actual_percent_int' : '780aff08',
         'actual_percent_dec' : '780cff08', 
         'actual_priority' : '780dff08',   
         'call_counts' : '780bff08',              
            },

      9  : { 
         'route_to_vdn' : '7808ff09', 
         'vdn_name' : '7809ff09',
         'target' : 'f816ff09',
         'actual_percent_int' : '780aff09',
         'actual_percent_dec' : '780cff09', 
         'actual_priority' : '780dff09',   
         'call_counts' : '780bff09',              
            },
      10 : { 
         'route_to_vdn' : '7808ff0a', 
         'vdn_name' : '7809ff0a',
         'target' : 'f816ff0a',
         'actual_percent_int' : '780aff0a',
         'actual_percent_dec' : '780cff0a', 
         'actual_priority' : '780dff0a',   
         'call_counts' : '780bff0a',              
            },    

      11 : { 
         'route_to_vdn' : '7808ff0b', 
         'vdn_name' : '7809ff0b',
         'target' : 'f816ff0b',
         'actual_percent_int' : '780aff0b',
         'actual_percent_dec' : '780cff0b', 
         'actual_priority' : '780dff0b',   
         'call_counts' : '780bff0b',              
            }, 
            
      12 : { 
         'route_to_vdn' : '7808ff0c', 
         'vdn_name' : '7809ff0c',
         'target' : 'f816ff0c',
         'actual_percent_int' : '780aff0c',
         'actual_percent_dec' : '780cff0c', 
         'actual_priority' : '780dff0c',   
         'call_counts' : '780bff0c',              
            }, 

      13 : { 
         'route_to_vdn' : '7808ff0d', 
         'vdn_name' : '7809ff0d',
         'target' : 'f816ff0d',
         'actual_percent_int' : '780aff0d',
         'actual_percent_dec' : '780cff0d', 
         'actual_priority' : '780dff0d',   
         'call_counts' : '780bff0d',              
            }, 

      14 : { 
         'route_to_vdn' : '7808ff0e', 
         'vdn_name' : '7809ff0e',
         'target' : 'f816ff0e',
         'actual_percent_int' : '780aff0e',
         'actual_percent_dec' : '780cff0e', 
         'actual_priority' : '780dff0e',   
         'call_counts' : '780bff0e',              
            }, 

      15 : { 
         'route_to_vdn' : '7808ff0f', 
         'vdn_name' : '7809ff0f',
         'target' : 'f816ff0f',
         'actual_percent_int' : '780aff0f',
         'actual_percent_dec' : '780cff0f', 
         'actual_priority' : '780dff0f',   
         'call_counts' : '780bff0f',              
            }, 
                                                                       
      16  : {
         'totals_target' : '7803ff01',
         'totals_calls_count' : '7805ff01',
      }
}

db_cmd = {}

for ky, data in addr.items():
     db_cmd[ky] = {}
     for field, address in data.items():
          if address in mapeo:
               db_cmd[ky][field] = { address : mapeo[address] }
          else:
               db_cmd[ky][field] = { address : ''}

pprint(db_cmd)
