# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:29:17 2016

@author: westerr

Haversine formula to find closest geocode in a dataframe/matrix of other geocodes

"""
import numpy as np
import pandas as pd

def haversine(lat1, lon1, lat2, lon2, units='miles'):
    """
    Calculates arc length distance between two lat_lon points (must be in radians)
    
    lat2 & and lon2 can be numpy arrays
    
    units can be 'miles' or 'km' (kilometers)
    """
    earth_radius = {'miles': 3959., 'km': 6371.}
    a = np.square(np.sin((lat2 - lat1)/2.)) + np.cos(lat1) * np.cos(lat2) * np.square(np.sin((lon2 - lon1)/2.))        
    return 2 * earth_radius[units] * np.arcsin(np.sqrt(a))   

def closest_geocode(lat_lon_tuple, lat_lon_matrix, n_closest=1, return_dist=False, units='miles'):
    """
    Function to find the closest distance between a lat/long tuple and matrix of lat/long pairs, returns the n closest,
    
    lat_lon_tuple is in the format (Latitude, Longitude)
    
    lat_lon_matrix is a numpy matrix in the format [[Latitude1, Longitude1], [Latitude2, Longitude2], ...]
    
    n_closest will return the position (index #) of the n closest geocodes in lat_lon_matrix
    
    if return_dist is True, will return the position (index #) and distance of the closest or n closest geocodes 
    
    units can be 'miles' or 'km' (kilometers)
    
    Uses the Haversine formula to find the arclength of two points on a sphere where radius = earth.
    """    
    # Setup lat lon pairs and convert to radians
    lat, lon = np.radians(lat_lon_tuple)
    shape = lat_lon_matrix.shape
    if shape[1] <= 2:
        lats = np.radians(lat_lon_matrix[:,0])
        lons =  np.radians(lat_lon_matrix[:,1])
    else:
        raise ValueError("lat_lon_matrix should only be two columns of format [lat, lon]")

    # Call haversine formula and return distance
    dist = haversine(lat, lon, lats, lons, units=units)
    
    # Get index for n closest geocodes
    min_idx = dist.argsort()[:n_closest]
    
    if return_dist == True:
        return min_idx, dist
    else:
        return min_idx

def haversine_dist_matrix(lat_lon_matrix, units='miles'):
    """
    Creates a pairwise distance matrix using the haversine formula
    
    lat_lon_matrix is a numpy matrix  in the format [[Latitude1, Longitude1], [Latitude2, Longitude2], ...]
    
    units can be 'miles' or 'km' (kilometers)
    """
    
    shape = lat_lon_matrix.shape
    if shape[1] <= 2:
        X = np.radians(lat_lon_matrix) # convert to radians
        dist_mtrx = np.zeros((shape[0], shape[0])) # initialize matrix of zeros
        for i in xrange(shape[0]):
            lat_i = X[i, 0]
            lon_i = X[i, 1]
            lats = X[:, 0]
            lons = X[:, 1]
            dist_mtrx[i] = haversine(lat_i, lon_i, lats, lons, units=units) # call haversine formula and overwrite matrix of zeros
        return dist_mtrx
    else:
        raise ValueError("lat_lon_matrix should only be two columns of format [lat, lon]")
    
# Example implementation 
if __name__ == '__main__':
    geocode1 = np.radians((42.400930, -71.058486))
    geocode2 = np.radians((42.346939, -71.168314))
    print haversine(geocode1[0], geocode1[1], geocode2[0], geocode2[1])
    
    lat_lon_tuple = (42.396154, -71.272548)
    df = pd.DataFrame({"ID": ['A', 'B', 'C'],
                       "latitude": [42.529234, 42.400930, 42.346939],
                       "longitude": [-71.182604, -71.058486, -71.168314]})
    row_indexer, distance = closest_geocode(lat_lon_tuple, df[['latitude','longitude']].as_matrix(), 
                                            n_closest=2,
                                            return_dist=True
                                            )
    df_closest = pd.concat([df, pd.DataFrame({"Distance": distance})], axis=1).loc[row_indexer]
    print df_closest
    
    dist_matrix = haversine_dist_matrix(df[['latitude','longitude']].as_matrix())
    print dist_matrix
