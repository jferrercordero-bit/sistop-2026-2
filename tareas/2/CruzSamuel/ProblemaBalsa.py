import threading
import time
import random
from enum import Enum

class Bando(Enum):
    HACKER = "Hacker"
    SERF = "Serf"

class Balsa:
    def __init__(self):   
        self.mutex = threading.Lock()
        self.condicion = threading.Condition(self.mutex)  
        self.hackers_esperando = 0
        self.serfs_esperando = 0
        self.grupo_actual = []
        self.balsa_ocupada = False
        self.viajes_realizados = 0
        self.finalizado = False
        self.personas_restantes = 0  # contador de personas que faltan por cruzar, IMPORTANTE! sino se queda esperando indefinidamente

        self.allowed_hackers = 0  
        self.allowed_serfs = 0    
    def _puede_formar_grupo(self):
        #Se implementan las reglas para formar un grupo valido, 4 del mismo bando o 2 de cada uno
        return (self.hackers_esperando >= 4 or 
                self.serfs_esperando >= 4 or 
                (self.hackers_esperando >= 2 and self.serfs_esperando >= 2))
    def _formar_grupo(self):
        # 2 hackers y 2 serfs
        if self.hackers_esperando >= 2 and self.serfs_esperando >= 2:
            self.grupo_actual = [Bando.HACKER] * 2 + [Bando.SERF] * 2
            self.hackers_esperando -= 2
            self.serfs_esperando -= 2
        # 4 hacekrs
        elif self.hackers_esperando == 4:
            self.grupo_actual = [Bando.HACKER] * 4
            self.hackers_esperando -= 4
        # 4 serfs
        elif self.serfs_esperando >= 4:
            self.grupo_actual = [Bando.SERF] * 4
            self.serfs_esperando -= 4

        
        self.allowed_hackers = sum(1 for b in self.grupo_actual if b == Bando.HACKER)  
        self.allowed_serfs = sum(1 for b in self.grupo_actual if b == Bando.SERF)       
        
        print(f"Grupo formado: {[b.value for b in self.grupo_actual]}")
        
# definicion de la funcion persona con atributos balsa, bando e id_persona
def persona(balsa, bando, id_persona):
    time.sleep(random.uniform(0.1, 2.0))
    balsa.abordar(bando, id_persona)
def zarpar(self):
        while not self.finalizado:
            with self.mutex:
                while not self.balsa_ocupada and not self.finalizado:               # espera a que se forme un grupo o finalice
                    self.condicion.wait()

                if self.finalizado:
                    break
                
                self.viajes_realizados += 1
                composicion = [b.value for b in self.grupo_actual]
                print(f"Balsa zarpa! ============ Viaje #{self.viajes_realizados}")
                print(f"Tripulacion: {composicion}")
                print(f"Quedan esperando: {self.hackers_esperando}H, {self.serfs_esperando}S")
                print("----------------------------------")
            
            # simulacion de viaje con time.sleep()                      
            # chequear si es necesario ajustar tiempo
            time.sleep(1)
            
            with self.mutex:
                self.grupo_actual = []
                self.balsa_ocupada = False
                # resetear allowed por seguridad
                self.allowed_hackers = 0
                self.allowed_serfs = 0
                self.condicion.notify_all()
def _formar_grupo(self):
        # 4 hacekrs
        if self.hackers_esperando >= 4:
            self.grupo_actual = [Bando.HACKER] * 4
            self.hackers_esperando -= 4
        # 4 serfs
        elif self.serfs_esperando >= 4:
            self.grupo_actual = [Bando.SERF] * 4
            self.serfs_esperando -= 4
        # 2 hackers y 2 serfs
        elif self.hackers_esperando >= 2 and self.serfs_esperando >= 2:
            self.grupo_actual = [Bando.HACKER] * 2 + [Bando.SERF] * 2
            self.hackers_esperando -= 2
            self.serfs_esperando -= 2
        
        # establecer cuantos de cada bando pueden subir en este viaje
        self.allowed_hackers = sum(1 for b in self.grupo_actual if b == Bando.HACKER)
        self.allowed_serfs = sum(1 for b in self.grupo_actual if b == Bando.SERF)

        print(f"Grupo formado: {[b.value for b in self.grupo_actual]}")

def _esta_en_proximo_grupo(self, bando):
        # esta condicion determina si la proxima persona puede ser parte del grupo que se va a formar
        if self.hackers_esperando >= 4 and bando == Bando.HACKER:
            return True
        elif self.serfs_esperando >= 4 and bando == Bando.SERF:
            return True
        elif self.hackers_esperando >= 2 and self.serfs_esperando >= 2:
            return True
        return False

def abordar(self, bando, id_persona):
        with self.mutex:
            print(f"{bando.value} {id_persona} llega. Esperando: {self.hackers_esperando}H, {self.serfs_esperando}S")
            
            if bando == Bando.HACKER:
                self.hackers_esperando += 1
            else:
                self.serfs_esperando += 1
            
            # esperando a que se forme un grupo valido
            while True:
                # si ya finalizó y no hay posibilidad de formar grupo, salir
                if self.finalizado:
                    break

                if (self._puede_formar_grupo() and 
                    not self.balsa_ocupada):
                    
                    # formar el grupo y asignar slots por bando
                    self._formar_grupo()
                    self.balsa_ocupada = True
                    # despertar a todos para que los que tengan slots puedan tomar su lugar
                    self.condicion.notify_all()
                    # no break aquí: dejamos que la persona entre en la siguiente sección que verifica slots
                # ahora verificar si este hilo tiene un slot en el grupo formado
                if self.balsa_ocupada:
                    if bando == Bando.HACKER and self.allowed_hackers > 0:
                        # tomar slot de hacker
                        self.allowed_hackers -= 1
                        break
                    elif bando == Bando.SERF and self.allowed_serfs > 0:
                        # tomar slot de serf
                        self.allowed_serfs -= 1
                        break

                # caso normal: esperar a que se formen grupos o se notifique
                self.condicion.wait()
            
            # si finalizado fue activado mientras esperaba, salir sin cruzar
            if self.finalizado and not self.balsa_ocupada:
                return

            # esperando que la balsa zarpe (la balsa estará ocupada hasta que el hilo zarpe y la deje libre)
            while self.balsa_ocupada:
                self.condicion.wait()

            # persona cruzó exitosamente
            self.personas_restantes -= 1
            print(f"{bando.value} {id_persona} cruzó exitosamente! ")

            # no quedan personas, 'despertar' a la balsa para que termine
            if self.personas_restantes == 0:
                self.finalizado = True
                self.condicion.notify_all()

# simulacion principal
def main():
    print("SIMULACIÓN CRUCE DEL RIO - PROBLEMA DE SINCRONIZACIÓN")
    print("=" * 50)
    
    balsa = Balsa()
    
    # crear personas
    hilos = []
    id_counter = 1
    
    # 8 hackers y 8 serfs. importante inicializar el contador de personas restantes!!!
    total_personas = 16
    balsa.personas_restantes = total_personas
    for _ in range(8):                                              # iniciamos 8 hackers y 8 serfs
        hilos.append(threading.Thread(
            target=persona, args=(balsa, Bando.HACKER, id_counter)
        ))
        id_counter += 1
        
        hilos.append(threading.Thread(
            target=persona, args=(balsa, Bando.SERF, id_counter)
        ))
        id_counter += 1
    
    hilo_balsa = threading.Thread(target=balsa.zarpar)              # hilo para la balsa
    hilo_balsa.start()
    
    for hilo in hilos:              # iniciar todos los hilos
        hilo.start()
        time.sleep(0.1)
    
    for hilo in hilos:              # esperar a que todos terminen
        hilo.join()

    hilo_balsa.join()               # esperamos a que la balsa termine
    
    print("\n" + "=" * 50)
    print(f"Total de viajes: {balsa.viajes_realizados}")
    print("Simulacion completada...")

if __name__ == "__main__":
    main()