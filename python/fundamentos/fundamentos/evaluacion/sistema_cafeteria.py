import time
import sys
def carga():
    an = ["/", "-", "\\"]
    for i in range(20):
        print(f"\rCargando {an[i % len(an)]}", end="")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\rPrograma cargado con exito")
import os
def limpiarConsola():
    os.system('cls')
carga()
class CafeteriaCliente:

    total_cl = 0
    membresia = ["Bronce", "Plata", "Oro"]

    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.saldo = 0
        self.membresia = "Bronce"

        CafeteriaCliente.total_cl += 1

    def realizar_compra(self, monto):
        self.saldo += monto
        pts_ganados = (monto // 1000) * 10
        self.puntos += pts_ganados

        print(f"\n{self.nombre} compró {monto}")
        print(f"Puntos ganados: {pts_ganados}")

    def pagar_saldo(self, monto):
        if monto > self.saldo:
            print(f"\nPago rechazado: monto mayor al saldo ({monto})")
        elif monto < 0:
            print("\nError: monto inválido")
        else:
            self.saldo -= monto
            print("\nPago realizado con éxito")
            print(f"Saldo pendiente: {self.saldo}")

    @classmethod
    def total_cls(cls):
        print(f"\nTotal clientes: {cls.total_cl}")

    @staticmethod
    def validar_membresia(tipo):
        return tipo in CafeteriaCliente.membresia

#PRUEBAS DEL SISTEMA

cl1 = CafeteriaCliente("Juan")
cl2 = CafeteriaCliente("Ana")
cl3 = CafeteriaCliente("Pedro")

print("\n====================================")
print("Sistema de Clientes para una Cafetería")
print("=====================================")

print("\nValidaciones:")
print("Bronce:", CafeteriaCliente.validar_membresia("Bronce"))
print("OroUltraChetadoConCosmoEspacial:", CafeteriaCliente.validar_membresia("OroUltraChetadoConCosmoEspacial"))

print("\nRESUMEN CLIENTE:")
while True: 
    print("\n=====================================")
    print("         Mostrar info de:")
    print("======================================")
    print("\nOpcion 1: Juan")
    print("Opcion 2: Ana")
    print("Opcion 3: Pedro")
    print("Opcion 4: Total clientes")
    
    opcion = input("\nIngresa la opcion: ")

    if opcion == "1":
        limpiarConsola()
        print("Nombre:", cl1.nombre)
        print("Puntos:", cl1.puntos)
        print("Saldo:", cl1.saldo)
        print("Membresía:", cl1.membresia)
        op = input("\nDeseas agregar monto a tu saldo: (si/no) ")
        if op == "si":
            cl1.realizar_compra(int(input("\nIngresa el monto que quieres comprar: ")))
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl1.saldo}")
                cl1.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
        else:
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl1.saldo}")
                cl1.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
        print("\n===============================")
    if opcion == "2":
        limpiarConsola()
        print("Nombre:", cl2.nombre)
        print("Puntos:", cl2.puntos)
        print("Saldo:", cl2.saldo)
        print("Membresía:", cl1.membresia)
        op = input("\nDeseas agregar monto a tu saldo: (si/no) ")
        if op == "si":
            cl2.realizar_compra(int(input("\nIngresa el monto que quieres comprar: ")))
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl2.saldo}")
                cl2.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
        else:
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl2.saldo}")
                cl2.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
        print("\n===============================")
    if opcion == "3":
        limpiarConsola()
        print("Nombre:", cl3.nombre)
        print("Puntos:", cl3.puntos)
        print("Saldo:", cl3.saldo)
        print("Membresía:", cl3.membresia)
        op = input("\nDeseas agregar monto a tu saldo: (si/no) ")
        if op == "si":
            cl3.realizar_compra(int(input("\nIngresa el monto que quieres comprar: ")))
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl3.saldo}")
                cl3.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
        else:
            opcion = input("\nDeseas realizar una compra (si / no): ")
            if opcion == "si":
                print(f"Saldo: {cl3.saldo}")
                cl3.pagar_saldo(int(input("Pago: ")))
                continue
            else:
                continue
    if opcion == "4":
        limpiarConsola()
        CafeteriaCliente.total_cls()
        continue
    else:
        op = input("Seguro que deseas salid?(si/no)  ")
        if op == "si":
            break
        else:
            continue