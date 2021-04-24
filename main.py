#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob

import mgz
from mgz.summary import Summary

from en_to_es import en_es

def get_info(input_file:str) -> dict():
    '''Obtiene la información más relevante de la partida'''
    info = dict()
    with open(f'{input_file}', 'rb') as data:
        sumario = Summary(data)
    info['nombre_archivo'] = input_file
    info['duracion_partida'] = mgz.util.convert_to_timestamp(sumario.get_duration()/1000)
    info['punto_de_vista'] = sumario.get_players()[sumario.get_owner()-1]['name']
    info['mapa_revelado'] = en_es['reveal_map'][sumario.get_settings()['map_reveal_choice'][1].capitalize()]
    info['velocidad'] = en_es['game_speeds'][sumario.get_settings()['speed'][1].capitalize()]
    info['poblacion'] = sumario.get_settings()['population_limit']
    info['diplomacia'] = sumario.get_diplomacy()['type']
    info['nombre_mapa'] = en_es['map_names'][sumario.get_map()['name']]
    info['tamano_mapa'] = sumario.get_map()['size'].capitalize()
    for map_size in en_es['map_sizes'].keys():
            if info['tamano_mapa'] in map_size:
                    info['tamano_mapa'] = en_es['map_sizes'][map_size]
    info['teams'] = ''
    if info['diplomacia'] == 'TG':
        info['teams'] = sumario.get_diplomacy()['team_size']
        info['diplomacia'] = 'Batalla de equipos'
        
    equipos = dict()
    for index, team in enumerate(sumario.get_teams()):
        index += 1
        equipos[index] = dict()
        for jugador in team:
            equipos[index][jugador] = dict()
            equipos[index][jugador]['nickname'] = sumario.get_players()[jugador-1]['name']
            civ = str(sumario.get_players()[jugador-1]['civilization'])
            civ = sumario.reference['civilizations'][civ]['name']
            equipos[index][jugador]['civ'] = en_es['civilizations'][civ]
            if sumario.get_players()[jugador-1]['winner']:
                equipos[index][jugador]['victoria'] = True
            else:
                equipos[index][jugador]['victoria'] = False
            id_color = str(sumario.get_players()[jugador-1]['color_id'])
            equipos[index][jugador]['color'] = mgz.reference.get_consts()['player_colors'][id_color]
    info['equipos'] = equipos

    return info

if __name__== "__main__":
    input_file = glob.glob('*.mgx')[0]
    info = get_info(input_file)
    print(f"Info sobre la partida grabada '{info['nombre_archivo']}'")
    print(f"Duración de la partida: {info['duracion_partida']}")
    print(f"Punto de vista de: {info['punto_de_vista']}")
    print()
    print(f"Mapa jugado: {info['nombre_mapa']}")
    print(f"Tamaño mapa: {info['tamano_mapa']}")
    print(f"Revelar mapa: {info['mapa_revelado']}")
    print(f"Velocidad del juego: {info['velocidad']}")
    print(f"Población máxima: {info['poblacion']}")
    print(f"Diplomacia: {info['diplomacia']}")
    if info['teams']:
        print(f"Diplomacia de los equipos: {info['teams']}")
    print()
    for indice, equipo in info['equipos'].items():
        print(f'Equipo {indice}')
        for jugador, dato in equipo.items():
            print(f'{jugador}) ', end='')
            print(dato['nickname'], end=' - ')
            print(dato['civ'], end=' - ')
            print(dato['color'])
            if dato['victoria']:
                print('Equipo ganador de la partida.')
            else:
                print('Equipo pierde esta ronda.')
        print()
