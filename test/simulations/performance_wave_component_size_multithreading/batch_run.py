#!/usr/bin/env python3

# Data processing
import numpy as np 
import pandas as pd 
from pandas import DataFrame
import subprocess
import os
import sys
import shutil

include_string = str("""
#ifndef CONSTANTS_H
#define CONSTANTS_H

#ifdef WIN32
#define _USE_MATH_DEFINES
#endif

#include <math.h>

#define PI M_PI
#define G 9.81 /*!< Acceleration due to gravity in m/s2 */ 
#define SEA_WATER_DENSITY 1025 /*!< Sea water density in Kg/m3 */
#define AIR_DENSITY 1.2 /*!< Kg/m3 */

#define COUNT_WAVE_SPECTRAL_FREQUENCIES {count_freq}/*!< Number of frequency bands in the 
                                            wave spectrum. */
#define COUNT_WAVE_SPECTRAL_DIRECTIONS  {count_directions} /*!< Number of direction bands in the 
                                            wave spectrum. Ideal if this is an 
                                            odd number.*/

#define COUNT_ASV_SPECTRAL_DIRECTIONS 360 /*!< Number of directions in 
                                            the wave force spectrum. */
#define COUNT_ASV_SPECTRAL_FREQUENCIES 100 /*!< Number of frequencies in the
                                             wave force spectrum. */

#define COUNT_DOF 6 /*!< Number of degrees of freedom for the motion of ASV. */
#define COUNT_PROPELLERS_MAX 4 /*!< Maximum number of propellers an ASV can 
                                 have.*/

#define COUNT_WAYPOINTS_MAX 20 /*!< Maximum number of waypoints through which 
                                 the ASV will navigate. */

#define OUTPUT_BUFFER_SIZE 200000 /*!< Output buffer size. */

#endif // CONSTANTS_H
""")

wave_frequencies = [5,10,15,15,15,20]
wave_directions = [3,3,5,9,13,13]

wave_count_dir = "wave_count_{count}"
include_dir = wave_count_dir + "/include"

build_dir = "{dir}/build"
build_dir_threading_disabled = build_dir + "/threading_disabled"
build_dir_threading_with_sync = build_dir + "/threading_with_sync"
build_dir_threading_without_sync = build_dir + "/threading_without_sync"

def create_include_dirs():
	for i in range(len(wave_frequencies)):
		wave_count = wave_frequencies[i] * wave_directions[i]
		os.mkdir(wave_count_dir.format(count=wave_count))

def create_include_files():
	for i in range(len(wave_frequencies)):
		wave_count = wave_frequencies[i] * wave_directions[i]
		shutil.copytree("../../../include", include_dir.format(count=wave_count)) 
		# overwite constants.h
		file_name = include_dir + "/constants.h"
		file = open(file_name.format(count=wave_count),"w")
		file.write(include_string.format(count_freq=wave_frequencies[i], count_directions=wave_directions[i]))
		# copy the cmakelist file
		shutil.copyfile("./CMakeLists.txt", wave_count_dir.format(count=wave_count)+"/CMakeLists.txt")

def create_build_dir(wave_dir):
	os.mkdir(build_dir.format(dir=wave_dir))
	os.mkdir(build_dir_threading_disabled.format(dir=wave_dir))
	os.mkdir(build_dir_threading_with_sync.format(dir=wave_dir))
	os.mkdir(build_dir_threading_without_sync.format(dir=wave_dir))

# Function to configure and build the binaries.
# This test rely on the asv_swarm binaries created in each of the subforders.
# Create the binaries if it does not exist by calling this function.
def build_all():
	create_include_dirs()
	create_include_files()
	project_dir = "../../"
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for wave_dir in subfolders:
		create_build_dir(wave_dir)
		# Build with threading disabled
		ps = subprocess.Popen(["cmake", "-DENABLE_MULTI_THREADING=OFF", "--config", "Release", project_dir], cwd=build_dir_threading_disabled.format(dir=wave_dir))
		ps.wait()
		ps = subprocess.Popen(["make"], cwd=build_dir_threading_disabled.format(dir=wave_dir))
		ps.wait()
		# Build with sync enabled
		ps = subprocess.Popen(["cmake", "-DENABLE_TIME_SYNC=ON", "--config", "Release", project_dir], cwd=build_dir_threading_with_sync.format(dir=wave_dir))
		ps.wait()
		ps = subprocess.Popen(["make"], cwd=build_dir_threading_with_sync.format(dir=wave_dir))
		ps.wait()
		# Build with sync disabled
		ps = subprocess.Popen(["cmake", "-DENABLE_TIME_SYNC=OFF", "--config", "Release", project_dir], cwd=build_dir_threading_without_sync.format(dir=wave_dir))
		ps.wait()
		ps = subprocess.Popen(["make"], cwd=build_dir_threading_without_sync.format(dir=wave_dir))
		ps.wait()

# remove all asv_out dir
def clean_bin():
	# remove asv_out from sub-directories
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for dir in subfolders:
		build_dir = dir + "/build"
		# check if asv_out dir exist
		if(os.path.isdir(build_dir)):
			print("removing " + build_dir)
			shutil.rmtree(build_dir)

# remove all asv_out dir
def clean_output():
	# remove the file with time recording
	time_file = "./run_time"
	if(os.path.isfile(time_file)):
		print("removing " + time_file)
		os.remove(time_file)
	# remove asv_out from sub-directories
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for dir in subfolders:
		path_to_asv_out = dir + "/asv_out"
		# check if asv_out dir exist
		if(os.path.isdir(path_to_asv_out)):
			print("removing " + path_to_asv_out)
			shutil.rmtree(path_to_asv_out)

def clean_all():
	# remove wave count dirs
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for dir in subfolders:
		# check if dir exist
		if(os.path.isdir(dir)):
			print("removing " + dir)
			shutil.rmtree(dir)

def write_summary(time_file, summary_file, build_type, wave_count):
	data = pd.read_csv(time_file, sep=" ", header=None)
	df = DataFrame(data)
	summary_file.write("{size} {build} {real_time} {sim_time} {ratio} \n".format(
		size=wave_count, 
		build=build_type,
		real_time=df[1].mean(), 
		sim_time=df[3].mean(), 
		ratio=df[5].mean()).encode())

# Run the simulation defined in each subdirectory
def run_all():
	wave_ht = 1.0
	wave_heading = 180
	# Write the simulation run times to file
	summary_file = open("./run_time", "wb", buffering=0)
	summary_file.write("swarm_size real_time(s) sim_time(s) real_to_sim_ratio\n".encode())
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for dir in subfolders:
		print("Run simulation in directory - " + dir)
		ps = subprocess.Popen(["../simulate.py", str(wave_ht), str(wave_heading)], cwd=dir)
		# Run each simulation one after the other
		ps.wait()
		
		time_file_name = dir + "/asv_out/time_threading_disabled"
		write_summary(time_file_name, summary_file, "threading_disabled", dir)

		time_file_name = dir + "/asv_out/time_threading_without_sync"
		write_summary(time_file_name, summary_file, "time_threading_without_sync", dir)

		time_file_name = dir + "/asv_out/time_threading_with_sync"
		write_summary(time_file_name, summary_file, "time_threading_with_sync", dir)

# Iterate through each subdirectory and find the average run time
def get_simulation_time(file, build_type):
	subfolders = [ f.path for f in os.scandir(".") if f.is_dir() ]
	for dir in subfolders:
		time_file = dir + "/asv_out/run_time"
		data = pd.read_csv(time_file, sep=" ", header=None)
		df = DataFrame(data)
		file.write("{directory} {real_time} {sim_time} {ratio} \n".format(
			build=build_type,
			real_time=df[1].mean(), 
			sim_time=df[3].mean(), 
			ratio=df[5].mean()).encode())
		#file.write(dir + str(df[0].mean()) + " " + str(df[2].mean()) + " " + str(df[4].mean()) + "\n")

def print_error_msg():
	print('''\nError! Incorrect command. Valid options are:

Build all binaries:
python3 batch_run.py build_all

Run all simulations: 
python3 batch_run.py wave_height wave_heading rand_seed

Clean all binaries and output files: 
python3 batch_run.py clean_all

Clean only output file: 
python3 batch_run.py clean_output

Clean only binaries: 
python3 batch_run.py clean_bin''')

# Extract the command line args
if len(sys.argv) == 2:
	if sys.argv[1] == "clean_all":
		clean_all()
	elif sys.argv[1] == "clean_bin":
		clean_bin()
	elif sys.argv[1] == "clean_output":
		clean_output()
	elif sys.argv[1] == "build_all":
		build_all()
	elif sys.argv[1] == "run_all":
		run_all()
	else:
		print_error_msg()
else:
	print_error_msg()
		
