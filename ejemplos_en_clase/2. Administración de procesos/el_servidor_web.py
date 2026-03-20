#!/usr/bin/python3
import threading
import time
import random
import curses

NUM_TRABAJADORES = 5
sem_trab = [threading.Semaphore(0) for i in range(NUM_TRABAJADORES)]
solicitudes = []
sem_solicitudes = threading.Semaphore(1)
solicitud_lista = threading.Semaphore(0)
trab_atendidos = {i: 0 for i in range(NUM_TRABAJADORES)}
sem_trab_atendidos = threading.Semaphore(1)

def trabajador(n):
    # ¿En qué espacio me toca escribir?
    mi_col = n * 20
    window.addstr(5, mi_col, f'Trab {n} ({mi_col})')
    window.refresh()
    time.sleep(0.3)
    while True:
        sem_trab[n].acquire()
        window.addstr(6, mi_col, 'REQ')
        window.refresh()

        sem_solicitudes.acquire()
        sol = solicitudes.pop()
        sem_solicitudes.release()

        window.addstr(7, mi_col, sol)
        window.refresh()
        time.sleep(random.random())

        # Terminé de atender: limpio el estado resultante
        window.addstr(6, mi_col, '     ')
        window.addstr(7, mi_col, '            ')
        window.refresh()


def jefe():
    global solicitudes, trab_atendidos

    # Inicializo trabajadores
    for i in range(NUM_TRABAJADORES):
        threading.Thread(target=trabajador, args=[i]).start()

    while True:
        solicitud_lista.acquire()
        window.addstr(10, 10, 'Conexión recibida por el jefe')
        window.refresh()

        # Elegimos a un trabajador para atender la solicitud
        el_trab = random.choice(range(NUM_TRABAJADORES))
        sem_trab[el_trab].release()
        sem_trab_atendidos.acquire()
        trab_atendidos[el_trab] += 1
        sem_trab_atendidos.release()
        window.addstr(10, 10, '                             ')
        window.refresh()

def asist_cont():
    global trab_atendidos
    while True:
        sem_trab_atendidos.acquire()
        window.addstr(1, 0, '----- Reporte de atención de trabajos -----')
        window.addstr(2, 0, f'Hay {len(threading.enumerate())} hilos activos:')
        window.addstr(3, 0, f'{trab_atendidos}')
        window.refresh()
        sem_trab_atendidos.release()
        time.sleep(5)

def genera_eventos():
    global solicitudes, sem_solicitudes
    paginas = ['index', 'about', 'projects', 'acerca_de',
               'proyectos', 'directorio']

    while True:
        solicitud = random.choice(paginas)

        sem_solicitudes.acquire()
        solicitudes.append(solicitud)
        sem_solicitudes.release()

        solicitud_lista.release()

        time.sleep(5 * random.random())


window = curses.initscr()

threading.Thread(target = jefe).start()
threading.Thread(target = asist_cont).start()
threading.Thread(target = genera_eventos).start()

