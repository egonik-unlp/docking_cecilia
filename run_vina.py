# coding=utf-8
#Python Script para correr AutoDock VINA
#Author: Emilia Barrionuevo
#Date: 02/2022

import os
from vina import Vina 
import pandas as pd
from datetime import datetime

print("Running...")

#%% SETEO DE PARÁMETROS DEL DOCKING (MODIFICAR SÓLO LO QUE ESTA EN VERDE O AMARILLO)
Receptor = "./pdbqts/" + "6N1S_curada.pdbqt"

Receptores = [os.path.join("pdbqts",file) for file in os.listdir("pdbqts") if file.endswith(".pdbqt")]
print(Receptores)
#Grid = "/home/disco/Escritorio/validacion_pose_disco/"+ redockeos + "/receptor/"
#Receptor_rigid = '/directorio/1iep_rigid.pdbqt' #PARA DOCKING CON RESIDUOS FLEXIBLES
#Receptor_flex = '/directorio/1iep_flex.pdbqt'   #PARA DOCKING CON RESIDUOS FLEXIBLES
#Ligandos = '/home/disco/Escritorio/Docking/ligandos/LMFA_prep_Manu_filtrado' #Carpeta donde tenemos guardados los ligandos a dockear
#Outputs = '/home/disco/Escritorio/Docking/outputs/LMFA_filtrado_NaV1.1_002'

Ligandos = './ligandos' #Carpeta donde tenemos guardados los ligandos a dockear
Outputs = '.' + '/outputs'


Observaciones = "Redocking cristal" #Observaciónes importantes para el readme_file
#center_box=pd.read_csv(Grid + '/center_grid.txt',sep=" ",header=0) #Levanta las coordenadas para cada caja.
	
x=19.828
y=77.917
z=-35.364

Center =[x, y, z]
Box_size=[22.5, 22.5, 22.5]
Exhaustiveness = 32
N_poses = 9
Campo_fuerzas = 'vina'      #Si se desea usar otro campo de fuerzas como ad4 o vinardo cambiar la palabra vina por el campo deseado
output_file = Outputs +'/output_file.txt'
readme_file = Outputs + '/readme_file.txt'

hoy = datetime.today()
Fecha = hoy.strftime("%d/%m/%Y %H:%M:%S")
Ligandos_carpeta= os.listdir(Ligandos) 
Ligandos_carpeta.sort()
print(f"got here -> {Ligandos_carpeta}")

#%% ESCRITURA DE README FILE  
for Receptor in Receptores:
	print(f"Procesando -> {Receptor} Chechu :)")
	readme_file = os.path.join(Outputs, f"readme_file_{Receptor.split('/')[1]}")
	with open(readme_file,"w") as f:
		f.write("PROTOCOLO DE DOCKING:" + "\n")
		f.write("Fecha:" + Fecha + "\n" + "\n")
		f.write("Observaciones:" + Observaciones + "\n" + "\n")
		f.write("Configuración:" + "\n")
		f.write("Receptor:" + Receptor + "\n")
		f.write("Ligandos:" + Ligandos + "\n")
		f.write("Grilla:  CENTRO " + str(Center) + "  TAMAÑO " + str(Box_size) + "\n" + "\n")
		f.write("Parámetros usados:" + "\n")
		f.write("Campo de fuerzas:" + Campo_fuerzas + "\n")
		f.write("Exhaustiveness:" + str(Exhaustiveness) + "\n")
		f.write("Número de poses:" + str(N_poses) + "\n" + "\n")
		f.write("Outputs:" + Outputs + "\n")
		f.write("Archivo output:" + output_file + "\n")
		f.write("Archivo readme:" + readme_file + "\n")
	#%% CORRIDA Y ESCRITURA DE OUTPUTS

	v = Vina(sf_name= Campo_fuerzas)    #Crea el objeto Vina. sf_name especifica el campo de fuerzas que va a usar.
				
	v.set_receptor(Receptor)    #Carga del archivo del receptor. 
		#v.set_receptor(Receptor_rigid , Receptor_flex)   #PARA DOCKING CON RESIDUOS FLEXIBLES
				
	v.compute_vina_maps(center= Center,box_size=Box_size) #Computar los affinity maps para cada ligando

	output = []

	with open(output_file,"a") as f:
		f.write("Ligando,TOP_SCORE"+"\n")

	for ligando in Ligandos_carpeta:

		print(ligando)
		try:
			if ligando.endswith(".pdbqt"): 
				# Selección de ligandos de la carpeta especificada
				v.set_ligand_from_file(Ligandos+"/"+ligando)
		
				# Calculo de Scorear la pose DESCOMENTAR PARA RESCOREAR
				#energy = v.score()
				#print('Score before minimization: %.3f (kcal/mol)' % energy[0])

				# Minimización de la pose DESCOMENTAR PARA RESCOREAR
				#energy_minimized = v.optimize()
				#print('Score after minimization : %.3f (kcal/mol)' % energy_minimized[0])
				#v.write_pose(pdbqt_filename= Outputs+"/out_"+ligando, overwrite=True)

				# Docking del ligando
				v.dock(exhaustiveness= Exhaustiveness, n_poses= N_poses)
				# Escritura la pose
				v.write_poses(pdbqt_filename= Outputs+"/out_"+ligando, n_poses=9, overwrite=True)
				# Escritura output pose-score
				energies = v.energies()
				score = energies[0,0]
				#output.append(score)
				print ("docked...")
		
				with open(output_file,"a") as f:
					print("writing output...")
					f.write(ligando + ","+ str(score) +"\n")
					print("done...")
		except:
			print ("Error in ligand")
			with open(readme_file,"a") as f:
				f.write("Error en el ligando"+ligando+ "\n")
			pass
