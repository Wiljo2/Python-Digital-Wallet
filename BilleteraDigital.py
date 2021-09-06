#Se hace los imports necesarios
from os import read
import requests
import datetime
import sys


# Se hace el "import"  de los archivos para utilizar los archivos y se almacena 
archivos = "datos.txt"
archivo = open(archivos,"r")
datos = archivo.read()
archivo.close()
  
#variables de uso global 
guion = "--------------------------------------------"
fecha = datetime.datetime.now()
fechaFormato = fecha.strftime("%c")
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': "5a13391c-0a14-4591-8cbf-267f55f9ff71"  
}
monedas = ["BTC","BNB","LTC","ETH","ETC"]

#manejo de request 
info = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",headers=headers).json()
monedero = {}

for cripto in info["data"]:
    monedero[cripto["symbol"]] = cripto["quote"]["USD"]["price"]


#manejo de datos del archivo datos.txt 
lineas = datos.splitlines()
diccionario={}

for linea in lineas:
  termino = linea.split(":")
  diccionario[termino[0]]=termino[1].split(",")
  for x in range(5):
      diccionario[termino[0]][x]= float(diccionario[termino[0]][x])


#*-----------------------------------------parte inicial(verifiación)--------------------------------------------------
def esUsuario(usuario):
    encontrado = diccionario.get(str(usuario))
    return encontrado
print("     |------------------------------------ BIENVENIDOS ------------------------------------|     ")
print("")

print("     -------------------------------------| Verificación |----------------------------------     ")
print("")
codigoUsuario = input("----->  Introduzca su codigo de usuario: ")

while not esUsuario(codigoUsuario):
        print("Codigo Invalido.")
        codigoUsuario = input("Introduzca su codigo de usuario: ")

def guardarTransaccion(monedaRecibir,tipoOperacion,codigoDestino,cantidadNueva,precio,montoNuevo):
  transacciones = open('transacciones.txt','a')
  transacciones.write("\n"+f'Fecha: {fechaFormato}| Codigo con que se inicio sesión:{codigoUsuario}|Codigo con el que se interactuo:{codigoDestino}|'
                     +"\n"+f'Tipo de operaccion: {tipoOperacion}| Moneda:{monedaRecibir}|Cantidad: {cantidadNueva}| Monto: {montoNuevo}'+"\n")
  transacciones.close()
  print(f'Fecha: {fechaFormato}| Codigo con que se inicio sesión:{codigoUsuario}|Codigo con el que se interactuo:{codigoDestino}|'
         +"\n"+f'Tipo de operaccion: {tipoOperacion}| Moneda:{monedaRecibir}|Cantidad: {cantidadNueva}|Precio:{precio}| Monto: {montoNuevo}')

#-------------------------------------------------------------------------------------------------------
#+                       ------------------------OPCIONES---------------------------
#-------------------------------------------------------------------------------------------------------
#parte 1 y parte 2
def Opcion(alternativa):
  print(guion)

  opcion = alternativa
  operador = 0  
  if opcion == 1:
    tipoOperacion = "Recibir Moneda"
    print("           1.Recibir cantidad         ")
    operador = 1
  elif opcion == 2:
    print("           2.Transferir monto         ")
    tipoOperacion = "Transferir Moneda"
    operador = -1
    
  #? inputs 
  print("") 
  monedaRecibir = (input("Introduzca el nombre de la moneda: ")).upper()
  print("")
  cantidadMoneda = float(input("Introduzce el monto de la moneda: "))
  print("")
  codigoDestino = input("Introduzca el codigo del emisor: ")
  print("")
  

  if monedaRecibir in monedas and isinstance(cantidadMoneda,float) and codigoDestino != codigoUsuario:
    diccionario[codigoUsuario][monedas.index(monedaRecibir)] += (cantidadMoneda * operador)
    cantidadNueva = diccionario[codigoUsuario][monedas.index(monedaRecibir)]
    precio = monedero[monedaRecibir]
    montoNuevo = precio * cantidadNueva
    guardarTransaccion(monedaRecibir,tipoOperacion,codigoDestino,cantidadNueva,round(precio,2),round(montoNuevo,2))
    print("")
    print("Transacción Exitosa! ")
    menu()
  else:
    print("Transacción fallida, por favor verifique los valores.")
    Opcion(alternativa)

#parte 3
def Opcion3():
  print(guion)
  print("           3.Mostrar balance una moneda         ")
  monedaRecibir = (input("Introduzca el nombre de la moneda: ")).upper()
  print(guion)
  if monedaRecibir in monedas:
    cantidadNueva = diccionario[codigoUsuario][monedas.index(monedaRecibir)]
    precio = round(monedero[monedaRecibir],2)
    montoNuevo = precio * cantidadNueva
    print(guion)
    print(f'|_Moneda_ : {monedaRecibir}| |_Cantidad_: {cantidadNueva}|  |_Monto_: {montoNuevo}')
    print(guion)
    print("Quiere volver al menu ? SI / NO ")
    respuesta = input("--->").upper()
    if respuesta == "SI":
      menu()
    else:
      print(" Bye :)")
    
  else:
    print("Consulta fallida ;c , por favor verifique los valores.")
    Opcion3()

#parte 4
def Opcion4():
  print("___________________________________________________________")
  print("           4.Mostrar balance general         ")
  for moneda in monedas:
    cantidad = diccionario[codigoUsuario][monedas.index(moneda)]
    monto = round(monedero[moneda],2) * cantidad
    print(f'| Moneda: {moneda}, Cantidad: {cantidad}, Monto: {monto} | ')
  print("___________________________________________________________") 
  print("")
  print("Quiere volver al menu ? SI / NO ")
  respuesta = input("--->").upper()
  if respuesta == "SI":
    menu()
  else:
    print(" Bye :)")

#parte 5
def Opcion5():
  print("           5.Mostrar histórico de transacciones         ")
  transaccione = open("transacciones.txt",)
  historial = transaccione.read()
  print(historial)
  respuesta = input("--->").upper()
  if respuesta == "SI":
    menu()
  else:
    print(" Bye :)")
#parte 6
def Opcion6():
  print(guion)
  print("A salido del programa exisotasamente! :D")
  print(guion)
  sys.exit()

#!----------------------------------------------------------------------------------------------
#?    ---------------------------------------MENU------------------------------------------
#!----------------------------------------------------------------------------------------------

def menu():
  print("")
  print("     ------------------------------------| Menú |------------------------------------ ")
  print("           |---------------Opciones de la billetera digital -----------------|        ")
  print("")
  print('1.Recibir cantidad'+"\n"+ '2.Transferir monto'+"\n"+'3.Mostrar balance una moneda'+
  "\n"+'4.Mostrar balance general'+"\n"+'5.Mostrar histórico de transacciones'+"\n"+'6.Salir del programa')
  print("")
  print("Por favor digitar el numero de la opcion que requiere:")
  opciones = int(input("-----> "))
  if opciones == 1:
    Opcion(1)
  elif opciones == 2 :
    Opcion(2)
  elif opciones == 3:
    Opcion3()
  elif opciones == 4:
    Opcion4()
  elif opciones == 5:
    Opcion5()
  elif opciones == 6:
    Opcion6()
  else:
    print("Por favor ingrese un numero del 1 a 6 para escoger la acción de la billetera")
    menu()

#!----  Iniciar el proceso del menú ---
menu()


# la nueva información esta guardada en el diccionario por ende se sobre escribe el archivo con la nueva info 
borrarinfo = open("datos.txt","w")
for lin in diccionario:
    bora =str(diccionario[lin]).replace('[','')
    borrarinfo.write(lin + ":" + bora.replace(']',''))
    borrarinfo.write("\n") 
borrarinfo.close()

