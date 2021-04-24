#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob
import mgz
from mgz.summary import Summary

input_file = glob.glob('./*.mgx')[0]

to_spanish = {'fast':'rádida', 'normal':'normal'}

with open(f'{input_file}', 'rb') as data:
        sumario = Summary(data)
        duracion_partida = mgz.util.convert_to_timestamp(sumario.get_duration()/1000)
        punto_de_vista = sumario.get_players()[sumario.get_owner()-1]['name']
        mapa_revelado = sumario.get_settings()['map_reveal_choice'][1]
        velocidad = to_spanish[sumario.get_settings()['speed'][1]]
        poblacion = sumario.get_settings()['population_limit']
        diplomacia = sumario.get_diplomacy()['type']
        nombre_mapa = sumario.get_map()['name']
        tamano_mapa = sumario.get_map()['size']
        teams = ''
        if diplomacia == 'TG':
            teams = sumario.get_diplomacy()['team_size']

print(f"Info sobre la partida grabada {input_file}")
print(f"Duración de la partida: {duracion_partida}")
print(f"Punto de vista de: {punto_de_vista}")
print()
print(f"Mapa jugado: {nombre_mapa}")
print(f"Tamaño mapa: {tamano_mapa}")
print(f"Revelar mapa: {mapa_revelado}")
print(f"Velocidad del juego: {velocidad}")
print(f"Población máxima: {poblacion}")
print(f"Diplimacia: {diplomacia}")
if teams: print(f"Diplomacia de los equipos: {teams}")  
print()
print("Equipos")
for team in sumario.get_teams():
	for jugador in team:
		print(sumario.get_players()[jugador-1]['name'])
		civ = str(sumario.get_players()[jugador-1]['civilization'])
		print(sumario.reference['civilizations'][civ]['name'])
		if sumario.get_players()[jugador-1]['winner']:
			print(f"Perdedor")
		else:
			print("Ganador")
		id_color = str(sumario.get_players()[jugador-1]['color_id'])
		#print(f'id_color: {id_color}')
		color = mgz.reference.get_consts()['player_colors'][id_color]
		print(color)
	print()
