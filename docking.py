#!/usr/bin/env python

import json
from vina import Vina
import pandas as pd
import numpy as np
import os
import six
from datetime import datetime
from collections import namedtuple, Iterable



def iterable(arg):
    return (
        isinstance(arg, Iterable) 
        and not isinstance(arg, six.string_types)
    )


Coord = namedtuple("Coord", "x y z")


parametros_docking = {
	"center" : Coord(x = 19.828,y = 77.917, z = - 35.364),
	"box_size" : Coord(x = 22.5, y = 22.5, z = 22.5),
	"exhaustiveness" : 32,
	"n_poses": 9,
	"forcefield" : "vina" 
}


def build_report( PROTOCOL : dict ) -> None:
	"""
	Builds a Markdown Report from PROTOCOL dict 
	"""
	title = "# Reporte de docking"
	file = PROTOCOL.pop("readme_file", "readme_file.md")
	with open(file, "w") as file:
		file.write(title)
		for (key, val) in PROTOCOL.items():
			file.write(f"\n ### {key}")
			if iterable(val):
				for _val in val:
					file.write(f"\n* {_val}")
			else:
				file.write(f"\n* {val}")
	
	



def define_protocol(**kwargs):
	filename = "config.json"
	if os.path.isfile(filename):
		with open(filename) as file:
			protocol = json.load(file)
	else: 
		protocol = kwargs 
	
	return protocol

def perform_docking_protocol(protocol : dict, )


PROTOCOL = define_protocol(
	date = datetime.now().strftime("%d-%m-%y"),
	receptor = [os.path.join("pdbqts",file) for file in os.listdir("pdbqts") if file.endswith(".pdbqt")],
	ligandos = [os.path.join("pdbqts",file) for file in os.listdir("ligandos") if file.endswith(".pdbqt")],
	observaciones =  "Redocking cristal",
	output_file_template =  "output_ligando-{}_receptor-{}.dat",
	readme_file = "readme.md",
	**parametros_docking
	)




if __name__ == "__main__":
	build_report(PROTOCOL)
	print(PROTOCOL)