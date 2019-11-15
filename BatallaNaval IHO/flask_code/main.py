import flask
from flask import Flask, render_template
import json
import random

#Creacion de la aplicacion Flask
app = Flask(__name__)

#Ruta raiz de la direccion de la pagina
@app.route("/", methods=["GET", "POST"]) 
def pagina_principal():
    return flask.render_template("inicial.html")


global tablero_objetivos, tablero, tablero_rival
global jugadas
global tipo_barcos
global cant_disparos_ganar_rival,cant_disparos_ganar_mio,score_actual
global puntosRival,puntosMios,fallasMias,fallasRival,turno,can
global partidasGanadas, partidasPerdidas,Numero_partida

#Inicializan las variables 
puntosRival=0
puntosMios=0
cant_disparos_ganar_rival=17
cant_disparos_ganar_mio=17
partidasGanadas=0
partidasPerdidas=0
fallasRival=0
fallasMias=0
score_actual=2
jugadas=1
Numero_partida=0

#MATRIZ QUE REPRESENTA EL TABLERO DEL JUGADOR, EN DONDE SE ENCUENTRAN LOS BARCOS
tablero=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]

#MATRIZ QUE REPRESENTA EL TABLERO DE OBJETIVOS
tablero_objetivos=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]

#MATRIZ QUE REPRESENTA EL TABLERO DEL OPONENTE
tablero_rival=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]

#DICCIONARIO CON LAS LETRAS DEL ABECEDARIO EN DONDE COMO DATO TIENE LA POSICION QUE OCUPA EN ESTE
dic={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10,1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J"}

#LISTA CON LA LONGITUD DE CADA UNO DE LOS BARCOS
tb=[5,4,3,3,2]

#LISTA CON LAS LETRAS CON LAS QUE SE RECONOCERAN CADA BARCO
tipo_barcos=["X","W","Y","Z","M"]


"_----------------------------------------------------------------------------------------------------------------------------"
#FUNCION QUE PERMITE AGREGAR EN UNA MATRIZ TEMPORAL LAS PARTIDA GANADAS, PERDIDAS,PUNTOS DE CADA JUGADOR PARA SER UTILIZADAS EN EL html
def datos():
     temp_datos=[]
     user = open("../nickgame.txt", mode="r")
     ganadas = open("../partidas_ganadas.txt", mode="r")
     perdidas = open("../partidas_perdidas.txt", mode="r")
     puntos = open("../usuarios_points.txt", mode="r")
     
     usuarios =user.readlines()
     pganadas =ganadas.readlines()
     pperdidas =perdidas.readlines()
     puntoss = puntos.readlines()
     
     ganadas.close()
     perdidas.close()
     user.close()
     puntos.close()

     pos = 0
     for _user in usuarios:
          name = _user.split()
          if( name == [usuarioActual]):
               partidasganadas=pganadas[pos]
               partidasperdidas=pperdidas[pos]
               puntos=puntoss[pos]
               temp_datos.append(partidasganadas)
               temp_datos.append(partidasperdidas)
               temp_datos.append(puntos)
          pos+=1
     return temp_datos

#FUNCION QUE ASIGNA EL SCORE AL JUGADOR SI GANO Y LO VA ACTUALIZANDO EN EL ARCHIVO usuarios_points.txt
def scoreAcomulado():
     global usuarioActual
     user_point = open("../usuarios_points.txt", mode="r")
     user = open("../nickgame.txt", mode="r")
     usuarios =user.readlines()
     datos = user_point.readlines()
     user_point.close()
     user.close()
     pos = 0
     for _user in usuarios:
          name = _user.split()
          if( name == [usuarioActual]):
               print("<<<true>>>")
               puntos = int(datos[pos]) + 100
               datos[pos] = str(int(datos[pos]) + 100 )+'\n'
               user_point = open("../usuarios_points.txt", mode="w")
               user_point.writelines(datos)
               user_point.close()
               score_actual = puntos
          pos+=1
     return score_actual

#FUNCION QUE ORGANIZA POR PUNTOS EL RANKING DE CADA UNO DE LOS USUARIOS
@app.route("/ranking/", methods=['GET'])
def ranking():

     nicks = []
     lista = []
     point = open("../usuarios_points.txt", mode="r")
     user = open("../nickgame.txt", mode="r")
     nicks = user.readlines()
     lista = point.readlines()
     n = len(lista)
     
     for i in range(1, n):
          for j in range(n-i):
               if int(lista[j]) < int(lista[j+1]):
                    lista[j], lista[j+1] = lista[j+1], lista[j]
                    nicks[j], nicks[j+1] = nicks[j+1], nicks[j]
     point.close()
     user.close()
     user_punt = []
     i = 0
     while(i < len(lista)):
          tmp2 = lista[i].split('\n')
          tmp1 = nicks[i].split('\n')
          user_score = tmp1[0] + ": " + tmp2[0]
          user_punt.append(user_score)
          i+=1
     return flask.render_template('ranking.html',datos={'user_ranking':user_punt})

#FUNCION QUE PERMITE ACTUALIZAR LAS PARTIDAS GANADAS DEL JUGADOR EN EL ARCHIVO partidas_ganadas.txt
def partidas_ganadas():

     global usuarioActual
     ganadas = open("../partidas_ganadas.txt", mode="r")
     user = open("../nickgame.txt", mode="r")
     usuarios =user.readlines()
     datos = ganadas.readlines()
     ganadas.close()
     user.close()
     pos = 0
     for _user in usuarios:
          name = _user.split()
          if( name == [usuarioActual]):               
               print("<<<true>>>")
               puntos = int(datos[pos]) + 1
               datos[pos] = str(int(datos[pos]) + 1 )+'\n'
               ganadas = open("../partidas_ganadas.txt", mode="w")
               ganadas.writelines(datos)
               ganadas.close()
               score_actual = puntos
          pos+=1
     return score_actual

#FUNCION QUE PERMITE ACTUALIZAR LAS PARTIDAS PERDIDAS DEL JUGADOR EN EL ARCHIVO partidas_perdidas.txt
def partidas_perdidas():
     global usuarioActual
     perdidas = open("../partidas_perdidas.txt", mode="r")
     user = open("../nickgame.txt", mode="r")
     usuarios =user.readlines()
     datos = perdidas.readlines()
     perdidas.close()
     user.close()
     pos = 0
     for _user in usuarios:
          name = _user.split()
          if( name == [usuarioActual]):
               print("<<<true>>>")
               puntos = int(datos[pos]) + 1
               datos[pos] = str(int(datos[pos]) + 1 )+'\n'
               perdidas = open("../partidas_perdidas.txt", mode="w")
               perdidas.writelines(datos)
               perdidas.close()
               score_actual = puntos
          pos+=1
     return score_actual


"-----------------------------------------------------------------------------------------------------------------------"

#FUNCIONES QUE SE ENCARGAN DE RENDERIZAR LAS VISTAS (html)

@app.route("/instrucciones/", methods=['GET'])
def instrucciones():
    return flask.render_template('instrucciones.html') 

@app.route("/instruccioness/", methods=['GET'])
def instruccioness():
    return flask.render_template('instrucciones1.html') 

@app.route("/regresar1/", methods=['GET'])
def regresar1():
    return flask.render_template('menu_jugador.html',datos={'usuario':usuarioActual})

@app.route("/menu_jugador/", methods=['GET'])
def menu_jugador():
     global can
     return flask.render_template('menu_jugador.html',datos={'usuario':usuarioActual}) 

@app.route("/menuinicial/", methods=['GET'])
def menuincial():
     return flask.render_template('inicial.html')

@app.route("/cerrarSesion/", methods=['GET'])
def cerrarSesion():
    global can
    can=0
    return flask.render_template('menu_jugador.html',datos={'usuario':usuarioActual})

@app.route("/salirdeljuego/", methods=['GET'])
def salirdeljuego():
    return flask.render_template('inicial.html')

@app.route("/entrar/", methods=['GET'])
def entrar():
    return flask.render_template('entrar.html')

"-----------------------------------------------------------------------------------------------------------------------"

'''FUNCION QUE PERMITE EL REGISTRO DE NUEVOS USUARIOS A LA BASE DE DATOS,
AQUI SE VERIFICA SI EL username INGRESADO NO SE ENCUENTRA REGISTRADO PARA AGREGARLO '''

@app.route("/registro", methods=['POST'])
def registro():
    print("Registrado")
    if (flask.request.method == 'POST'):
          _nick = flask.request.form['username2']
          nicks = open("../nickgame.txt", mode="a") #ABRE EL ARCHIVO PLANO PARA ESCRIBIR
          nicks.write(_nick)
          nicks.write('\n')
          nicks.close()
         
          _pin = flask.request.form['password2']
          claves = open("../claves.txt", mode="a")
          claves.write(_pin)
          claves.write('\n')
          claves.close()

          user_point = open("../usuarios_points.txt", mode="a")
          user_point.write('0')
          user_point.write('\n')
          user_point.close()

          partidas_ganadas = open("../partidas_ganadas.txt", mode="a")
          partidas_ganadas.write('0')
          partidas_ganadas.write('\n')
          partidas_ganadas.close()

          partidas_perdidas = open("../partidas_perdidas.txt", mode="a")
          partidas_perdidas.write('0')
          partidas_perdidas.write('\n')
          partidas_perdidas.close()

    return flask.render_template('entrar.html')

'''FUNCION QUE PERMITE EL INGRESO DE UN USUARIO VALIDANDO SI TANTO EL USERNAME COMO EL PASSWORD HA SIDO
ALMACENADO EN LA BASE DE DATOS Y DIGITADOS CORRECTAMENTE, EN CASO DE QUE SEA VERDADERO, SE RENDERIZA LA
VISTA DEL MENU DEL JUGADOR'''

@app.route("/login", methods=['POST'])
def login():
    global usuarioActual
    inicio=False
    print("Registrado")

    _nick = flask.request.form['username1'] #ALMACENA EN UNA VARIABLE EL USUARIO QUE ESTA INGRESANDO DESDE EL HTML(INPUT)
    _pin =  flask.request.form['password1']#ALMACENA EN UNA VARIABLE EL USUARIO QUE ESTA INGRESANDO DESDE EL HTML(INPUT)
    print("NICK",_nick)
    _usuarios = open("../nickgame.txt", "r")
    _contrasenas = open("../claves.txt","r")
    usuarios = _usuarios.readlines()
    contrasenas = _contrasenas.readlines()
    print("CLAVE", _nick)

    for _user in usuarios:
        for _pass in contrasenas:
            nicks = _user.split()
            clave = _pass.split()
            for it in range(0, len(nicks)):
                #Si el usuario y la contraseña estan en "base de datos (arch txt) en la misma posicion se cumple la condicion
                if( _nick == nicks[it] and _pin == clave[it]): 
                    inicio=True
                    usuarioActual = _nick
                    break

        #Se cierran los archivos txt
        _usuarios.close() 
        _contrasenas.close()

    if(inicio == False):
        return flask.render_template('entrar.html')
    else:
        return flask.render_template('menu_jugador.html',datos={'usuario':usuarioActual})

"-----------------------------------------------------------------------------------------------------------------------"

#FUNCION QUE VALIDA QUE LA COORDENADA SE ENCUENTRE EN EL RANGO DE 1 A 10 Y RETORNA TRUE O FALSE
def check(f,c):
     if (f>0 and f<11) and (c>0 and c<11):
          return True

#FUNCIONES QUE PERMITEN SEPARAR LA COORDENADA EN VARIABLES FILA Y COLUMNA    
def fila(fila_colu):
     f=fila_colu[0]
     return f

def columna(fila_colu):
     c=int(fila_colu[1:])
     return c

#Funciones que se encargan de agregar los barcos en la matriz respectiva (En el tablero del jugador o en el tablero rival)
def agregar_barcos(tablero,temp,can,tipo_barcos):
     for y in range (len(temp)):
          f=temp[y][0]
          c=temp[y][1]
          tablero[f][c]=tipo_barcos[can]
     return tablero

def agregar_rival(tablero_rival,temp,can2,tipo_barcos):
     for y in range (len(temp)):
          f=temp[y][0]
          c=temp[y][1]
          tablero_rival[f][c]=tipo_barcos[can2]
     return tablero_rival

"-----------------------------------------------------------------------------------------------------------------------"

#FUNCION QUE SE ENCARGA DE REALIZAR EL TABLERO DEL CONTRINCANTE
global can2
can2=0
def contrincante(tablero_rival):
     global can2
     can2=can2    
     while can2<5:
          #Las variables f (Fila), c (Columna) y d (Direccion) almacenan los valores que se generan de manera  
          # aleatoria teniendo en cuenta la condicion
          f=random.randint(1,10)
          c=random.randint(1,10)
          d=random.randint(1,4)
          c2=c
          fi=f
          if check(f,c):
               temp=[]
               if d==1:
                    for x in range (tb[can2]):
                         f=fi-x
                         if (check(f,c)) and (tablero_rival[f][c]==0):
                              temp.append([f,c])
               if d==2:
                    for x in range (tb[can2]):
                         f=fi+x
                         if (check(f,c)==True) and (tablero_rival[f][c]==0):
                              temp.append([f,c])
               if d==3:
                    for x in range (tb[can2]):
                         c=c2+x
                         if (check(f,c)==True) and (tablero_rival[f][c]==0):
                              temp.append([f,c])
               if d==4:
                    for x in range (tb[can2]):
                         c=c2-x
                         if (check(f,c)==True) and (tablero_rival[f][c]==0):
                              temp.append([f,c])

          if len(temp)==tb[can2]:
               agregar_rival(tablero_rival,temp,can2,tipo_barcos)
               can2+=1   
     return tablero_rival 

"-----------------------------------------------------------------------------------------------------------------------"
#FUNCION QUE SE ENCARGA DE AGREGAR LOS BARCOS DEL USUARIO TENIENDO EN CUENTA LA VARIABLE Y DIRECCION DIGITADA EN EL FORMULARIO DEL html

global can
can=0

#Funcion con metodo GET que permite renderizar el html organizarbarcos con las variables vacias
@app.route("/organizarbarcos", methods=['GET'])
def organizarbarcosGet():
     global tablero, tablero_objetivos, tablero_rival, can,cant_disparos_ganar_rival,cant_disparos_ganar_mio,can2,Numero_partida
     can=0
     can2=0
     Numero_partida=0
     tablero=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]

     tablero_objetivos=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]
     tablero_rival=[[" ",1,2,3,4,5,6,7,8,9,10],
          ["A",0,0,0,0,0,0,0,0,0,0],
          ["B",0,0,0,0,0,0,0,0,0,0],
          ["C",0,0,0,0,0,0,0,0,0,0],
          ["D",0,0,0,0,0,0,0,0,0,0],
          ["E",0,0,0,0,0,0,0,0,0,0],
          ["F",0,0,0,0,0,0,0,0,0,0],
          ["G",0,0,0,0,0,0,0,0,0,0],
          ["H",0,0,0,0,0,0,0,0,0,0],
          ["I",0,0,0,0,0,0,0,0,0,0],
          ["J",0,0,0,0,0,0,0,0,0,0]]

     cant_disparos_ganar_mio=17
     cant_disparos_ganar_rival=17

     print(organizarbarcosGet)
     print(tablero)
     return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,'MiTablero':tablero,'Numeropartida':Numero_partida,
                                                       'TableroRival':tablero_objetivos,'TableroRivalBase':tablero_rival,
                                                       'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival})


#Del formulario del html se recibe la coordenada y ubicacion dada por el usuario para procesarla y actualizar el template con los datos dados
@app.route("/organizarbarcos", methods=['POST'])
def organizarbarcos():
     global cant_disparos_ganar_rival, cant_disparos_ganar_mio, partidasGanadas, partidasPerdidas, MisPuntos,usuarioActual, can
     global Numero_partida
     print("----------")
     print(tablero)

     fila_colu= flask.request.form['coordenada']
     try:

          #FILAS Y COLUMNAS
          f=fila(fila_colu)
          c=columna(fila_colu)

          #VUELVE LA LETRA DE LA COORDENADA EN MAYUSCULA
          f=f.upper()

          #VARIABLE QUE RECIBE DEL html LA DIRECCION DADA POR EL USUARIO
          d=flask.request.form['direccion']

          #FILAS Y COLUMNAS BASES
          f=dic[f]
          c2=c
          fi=f
     except:
          return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,
                                                            'MiTablero':tablero,
                                                            'TableroRival':tablero_objetivos,
                                                            'TableroRivalBase':tablero_rival})

     
     #SE EVALUA SI LA COORDENADA DIGITADA SE ENCUENTRE EN EL TABLERO Y SI ADEMAS SE ENCUENTRA VACIA PARA COLOCAR LOS BARCOS
     if check(f,c)==True and tablero[f][c]==0:
          temp=[]
          #EVALUA QUE LA DIRECCION DIGITADA EN EL FORMULARIO SEA LA CORRECTA 
          if d=="1" or d=="2" or d=="3" or d=="4":

               #TENIENDO EN CUENTA LA DIRECCION DIGITADA SE ORGANIZAN LOS BARCOS 
               if d=="1":
                    for x in range (tb[can]):
                         f=fi-x
                         if (check(f,c)==True) and (tablero[f][c]==0):
                              temp.append([f,c])   

               elif d=="2":
                    for x in range (tb[can]):
                         f=fi+x
                         print(f)
                         if (check(f,c)==True) and (tablero[f][c]==0):
                              temp.append([f,c])  
               elif d=="3": 
                    for x in range (tb[can]):
                         c=c2+x
                         if (check(f,c)==True) and (tablero[f][c]==0):
                              temp.append([f,c])
                              
               elif d=="4":
                    for x in range (tb[can]):
                         c=c2-x
                         if (check(f,c)==True) and (tablero[f][c]==0):
                              temp.append([f,c])

               #Valido que el tamaño de la matriz temp sea igual a el tipo de barco actual para que 
               # los envie a una funcion que permitira agregarlos            
               if len(temp)==tb[can]:
                    agregar_barcos(tablero,temp,can,tipo_barcos)
                    can+=1

                    #CONDICION QUE EVALUA QUE SE HALLAN ORGANIZADO LOS 5 BARCOS
                    if not (can == 5):
                         return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,
                                                                      'MiTablero':tablero,
                                                                      'TableroRival':tablero_objetivos,
                                                                      'TableroRivalBase':tablero_rival})
                    #SI LOS 5 BARCOS HAN SIDO UBICADOS RENDERIZA EL TEMPLATE GAME
                    
                    else:
                         contrincante(tablero_rival)
                         print("CONTRINCANTE",tablero_rival)
                         
                         #Inicializo las variables para enviarlas el template game
                         temp_datos=datos()
                         partidasGanadas=temp_datos[0]
                         partidasPerdidas=temp_datos[1]
                         MisPuntos=temp_datos[2]
                         print(temp_datos)
                         Numero_partida=1
                         return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'MisPuntos':MisPuntos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival})
               else:
                    return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,
                                                            'MiTablero':tablero,
                                                            'TableroRival':tablero_objetivos,
                                                            'TableroRivalBase':tablero_rival})
          else:
               return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,
                                                            'MiTablero':tablero,
                                                            'TableroRival':tablero_objetivos,
                                                            'TableroRivalBase':tablero_rival})
     else:
          return flask.render_template('organizarbarcos.html',datos={'usuario':usuarioActual,
                                                            'MiTablero':tablero,
                                                            'TableroRival':tablero_objetivos,
                                                            'TableroRivalBase':tablero_rival})



"--------------------------------------------------------------------------------------------------------------------------------------"        

#Funcion de lanzar cohete del rival, donde se genera una coordenada aleatoria como disparo para el jugador
def lanzarCoheteRival(tablero):
     global cant_disparos_ganar_rival, cant_disparos_ganar_mio, partidasGanadas, partidasPerdidas, MisPuntos,usuarioActual
     global Numero_partida
     
     #VARIABLES QUE ALMACEN EL NUMERO ALEATORIO ENTRE EL 1 Y EL 10 PARA DEFINIR LA COORDENADA
     f=random.randint(1,10)
     c=random.randint(1,10)
     #print("RIVAL [",f,",",c,"]")
     

     #CONDICION QUE EVALUA SI EN DICHA COORDENADA SE ENCUENTRA UN BARCO O NO
     
     if tablero[f][c]=="X" or tablero[f][c]=="W" or tablero[f][c]=="Y" or tablero[f][c]=="Z" or tablero[f][c]=="M":
          cant_disparos_ganar_rival-=1
          tablero[f][c]="P"
          return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})

     else:
          tablero[f][c]="K"
          return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})


#Funcion que recibe la coordenada digitada en el html game para procesarla y actualizar el formulario 
@app.route('/lanzarCohete', methods=["POST"])
def lanzarCohete():
     global cant_disparos_ganar_mio,cant_disparos_ganar_rival, tablero_rival,tablero_objetivos,tablero
     global partidasGanadas, partidasPerdidas, MisPuntos,Numero_partida

     final=0
     #INTENTA REALIZAR LA LECTURA DE LA COORDENADA
     try:
          #Variable que recibe de la formula la coordenada digitada
          fila_colu=flask.request.form['coordenada'] 
          #DE LA VARIABLE COORDENADA SE DIVIDE EL VALOR DE LA FILA Y COLUMNA 
          f=fila(fila_colu)
          c=columna(fila_colu)
          f=f.upper()
          f=dic[f]
     #EN CASO DE QUE OCURRA UN ERROR POR LA COORDENADA MAL ESCRITA RENDERIZA EL MISMO TEMPLATE
     except:
          return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})
                                                                   

     #PASA LA VARIABLES FILA Y COLUMNA A UNA FUNCION QUE EVALUA SI DICHA COORDENADA SE ENCUENTRAN EN EL TABLERO
     if check(f,c)==True: 
          #EVALUA SI LA COORDENADA YA HA SIDO DIGITADA PARA DAR OTRA OPORTUNIDAD
          if tablero_rival[f][c]=="P" or  tablero_rival[f][c]=="K":
               return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                  'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                  'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                  'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                  'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})

          #VALIDA SI HAY O NO BARCOS EN LA COORDENADA DADA
          elif tablero_rival[f][c]=="X" or tablero_rival[f][c]=="W" or tablero_rival[f][c]=="Y" or tablero_rival[f][c]=="Z" or tablero_rival[f][c]=="M":
               #SI HAY UN BARCO DEL OPONENTE EN LA COORDENADA EN EL TABLERO DE OBJETIVOS DEBE AGREGAR UNA "P" QUE SIMBOLIZA LA ESTRELLA

               tablero_objetivos[f][c]="P" 
               tablero_rival[f][c]="P"

               #SE RESTAN LOS DISPAROS PARA GANAR DEL JUGADOR
               cant_disparos_ganar_mio-=1 
               lanzarCoheteRival(tablero)
               Numero_partida+=1
               print(cant_disparos_ganar_mio)

               #ESTA CONDICION EVALUA SI LA CANTIDAD DE DISPAROS ES IGUAL A LA DADA PARA FINALIZAR EL JUEGO
               if cant_disparos_ganar_mio==final:
                    partidas_ganadas()
                    scoreAcomulado()
                    return flask.render_template('ganaste.html',datos={'usuario':usuarioActual})

               elif cant_disparos_ganar_rival==final:
                    partidas_perdidas()
                    return flask.render_template('perdiste.html',datos={'usuario':usuarioActual})

               return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                  'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                  'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                  'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                  'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})
                                                           
          #SI NO HAY NINGUN BARCO ENTONCES DEBE AGREGAR UNA K QUE SIMBOLIZA AGUA
          else: 
               tablero_objetivos[f][c]="K"
               tablero_rival[f][c]="K"
               lanzarCoheteRival(tablero)
               Numero_partida+=1
               #ESTA CONDICION EVALUA SI LA CANTIDAD DE DISPAROS ES IGUAL A LA DADA PARA FINALIZAR EL JUEGO
               if cant_disparos_ganar_mio==final:
                    partidas_ganadas()
                    scoreAcomulado()
                    
                    return flask.render_template('ganaste.html',datos={'usuario':usuarioActual})

               elif cant_disparos_ganar_rival==final:
                    partidas_perdidas()
                    return flask.render_template('perdiste.html',datos={'usuario':usuarioActual})

               return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                  'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                  'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                  'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                  'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})

     else:
          return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})
                                                                        
"_----------------------------------------------------------------------------------------------------------------------------"

#FUNCION QUE SE ENCARGA DE LEER EL ARCHIVO JSON
@app.route("/cargarArchivo/", methods=['GET'])

def cargarArchivo():
    global tablero, tablero_rival,MisPuntos,partidasGanadas,partidasPerdidas,Numero_partida

    #Se abre el archivo json donde se encuentra la ubicacion de los barcos para leerlo
    with open('../tablero.json','r') as tablero:
        datoss = tablero.read()
    objeto = json.loads(datoss)

    #Del diccionario del json, unicamente guarda la llave que dice 'Mitablero' que es en la cual se encuentra la matriz
    tablero_cargado = objeto["Mitablero"] 
    tablero = tablero_cargado

    contrincante(tablero_rival)
    print("<<JSON",tablero)
    print("")
    print("CONTRINCANTE", tablero_rival)

    #De la matriz temp_datos guarda las partidas ganada, perdidas y puntos del jugador actual para enviarlo al html
    temp_datos=datos()
    partidasGanadas=temp_datos[0]
    partidasPerdidas=temp_datos[1]
    MisPuntos=temp_datos[2]
    #Inicializa el numero de partidas en 1
    Numero_partida=1
    
    return flask.render_template('game.html',datos={'usuario':usuarioActual,'MiTablero':tablero,
                                                       'TableroRival':tablero_objetivos,'Numeropartida':Numero_partida,
                                                       'TableroRivalBase':tablero_rival,'cant_disparos_ganar_mio':cant_disparos_ganar_mio,
                                                       'partidasPropia':partidasGanadas, 'Partidas_perdidas_propia': partidasPerdidas,
                                                       'cant_disparos_ganar_rival':cant_disparos_ganar_rival,'MisPuntos':MisPuntos})

"_----------------------------------------------------------------------------------------------------------------------------"
 
#Defino el puerto en el que deseo que se ejecute la app
if __name__ == "__main__":
    app.run(port = 58145, debug=True)

    
