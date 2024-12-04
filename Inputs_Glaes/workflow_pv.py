# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:29:40 2023

@author: Alycia Leonard, University of Oxford

workflow.py

This script implements land exclusions for the countries defined in country_names
It then allocates PV and wind installations over the allowed area
The outputs are saved as .shp files.

"""

import glaes as gl
import time
import os
import pickle

# Define country name (used for output filenames)
country_names = ["Laos"] 

# Record the starting time
start_time = time.time()

# Get path to this file and then also path to data
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, 'data')
output_dir = os.path.join(dirname, 'processed')

# Check whether there are directories for "data" and "processed" - make them if they're missing.
os.makedirs(data_path, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# create a for loop that can loop through a list of country names

for country_name in country_names:
    print("Land exclusions for " + country_name)

    # Load the pickled EPSG code for the country
    with open(os.path.join(data_path, f'{country_name}_EPSG.pkl'), 'rb') as file:
        EPSG = pickle.load(file)

    # calculating exclusions

    print(" - Initializing exclusion calculator...")
    ec = gl.ExclusionCalculator(os.path.join(data_path,  f'{country_name}.geojson'), srs=EPSG, pixelSize=100)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Applying exclusions - coast...")
    ec.excludeVectorType(os.path.join(data_path,  f'{country_name}_oceans.geojson'), buffer=250)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    # print(" - Applying exclusions - protected areas...")
    # ec.excludeVectorType(os.path.join(data_path,  f'{country_name}_protected_areas.geojson'), buffer=250)
    # current_time = time.time() - start_time
    # print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")
    
    print(" - Applying exclusions - national biodiversity conservation areas...")
    ec.excludeVectorType(os.path.join(data_path,  f'{country_name}_national_conversation.geojson'), buffer=250)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")
    
    print(" - Applying exclusions - forest protection areas...")
    ec.excludeVectorType(os.path.join(data_path,  f'{country_name}_protection_area.geojson'), buffer=250)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")
    
    print(" - Applying exclusions - Slope above 6.28 degrees (N/E/W) and 33 degrees (S)...")
    ec.excludeRasterType(os.path.join(data_path, f'Laos_slope_excluded_pv.tif'), value=1, prewarp=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Applying exclusions - herbaceous wetland...")
    ec.excludeRasterType(os.path.join(data_path, f'{country_name}_CLC.tif'), value=90, prewarp=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Applying exclusions - built-up area...")
    ec.excludeRasterType(os.path.join(data_path, f'{country_name}_CLC.tif'), value=50, prewarp=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Applying exclusions - permanent water bodies...")
    ec.excludeRasterType(os.path.join(data_path, f'{country_name}_CLC.tif'), value=80, prewarp=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")
    ec.draw()

    print(" - Applying exclusions - agriculture...")
    ec.excludeRasterType(os.path.join(data_path, f'{country_name}_CLC.tif'), value=40, prewarp=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Saving excluded areas for PV as .tif file...")
    ec.save(os.path.join(output_dir, f'{country_name}_pv_exclusions.tif'), overwrite=True)
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")

    print(" - Distributing pv plants and saving placements as .shp...")
    ec.distributeItems(separation=224, output=os.path.join(output_dir, f'{country_name}_pv_placements.shp'))
    current_time = time.time() - start_time
    print(f"   Done! Time elapsed so far: {current_time:.4f} seconds")
