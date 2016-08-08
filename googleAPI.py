# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:30:46 2015

@author: westerr
"""
import urllib, json, urllib2, time

class GoogleMapsAPI(object):
    def __init__(self, key):
        # Initializing class object
        self.key = key # google maps api key
        self.dailylimit = 2500
        self.limitpersecond = 50
        
    def get_geocode(self, address, optional_args=None, time_delay=0.5, error='Error'):
        """
        Takes an address as a string and returns the lat/long in a dictionary
        
        optional_args is a dictionary of key value pairs where the key is the optional
        param and the value is the query value 
        
        time_delay specifies a delay do to call limits
        
        if error in response will fill results with value specified by error
        
        """      
        # Checking input vaues
        if isinstance(address, str):
            # Define api url        
            GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
            
            # Define query params
            encode_params = {'key': self.key, 'address': address} # required
            if optional_args:
                encode_params.update(optional_args) # add optional args

            # Request and read results
            encodedParams = urllib.urlencode(encode_params)
            request = urllib2.Request(GEOCODE_URL+encodedParams)
            response = urllib2.urlopen(request)
            json_result = json.loads(response.read())
            self.geocode_result = json_result # make accessible from main
            
            # Process api results
            if json_result['status'] == 'OK':
                lon = json_result['results'][0]['geometry']['location']['lng']
                lat = json_result['results'][0]['geometry']['location']['lat']
            else:
                print 'Requested failed with error code: ' + json_result['status']
                lon = error
                lat = error    
            time.sleep(time_delay) # delay for request limits 
            return {'longitude': lon, 'latitude': lat}
        else:
            raise TypeError("address must be a string , got %s" % type(address))
        
    def get_distance(self, origin, destination, optional_args=None, time_delay=0.5, error='Error'):
        """
        Providing the origin and a destination address as strings will 
        return the travel time in minutes and travel distance in miles
        of the shortest route
        
        optional_args is a dictionary of key value pairs where the key is the optional
        param and the value is the query value 
        
        time_delay specifies a delay do to call limits
        
        if error in response will fill results with value specified by error
        
        """        
        
        # Checking input values
        shape = [1,1]
        if isinstance(origin, list):
            orign = '|'.join(origin)
            shape[0] = len(origin)
        elif isinstance(origin, str):
            orign = origin
        else:
            raise TypeError("origin must be a string or list/tuple of strings, got %s" % type(origin))
        if isinstance(destination, list):
            dest = '|'.join(destination)
            shape[1] = len(destination)
        elif isinstance(destination, str):
            dest = destination
        else:
            raise TypeError("destination must be a string or list/tuple of strings, got %s" % type(destination))            
        
        # Define api url        
        DIST_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        
        # Define query params
        encode_params = {'key': self.key, 'origins': orign, 'destinations': dest}
        if optional_args:
            encode_params.update(optional_args)
        
        # Request and read results
        encodedParams = urllib.urlencode(encode_params)
        request = urllib2.Request(DIST_MATRIX_URL+encodedParams)
        response = urllib2.urlopen(request)
        json_result = json.loads(response.read())
        self.dist_result = json_result # make accessible from main
        
        # Process api results
        results = {}
        if json_result['status'] == 'OK':
            for i in xrange(shape[0]):
                for j in xrange(shape[1]):
                    results['origin-'+str(i)+'_destination-'+str(j)] = {'duration': json_result['rows'][i]['elements'][j]['duration']['value'] / 60., # time in minuts
                                                            'distance': json_result['rows'][i]['elements'][j]['distance']['value'] * 0.000621371, # distance in miles
                                                            'origin': json_result['origin_addresses'][i],
                                                            'destination': json_result['destination_addresses'][j]}
        else:
            print 'Requested failed with error code: ' + json_result['status']
        time.sleep(time_delay) # delay to not get locked out of api
        return results

if __name__ == '__main__':
    # Using class
    maps = GoogleMapsAPI('google_maps_api_key')
    rgn_bounds = {'MA': '41.189388,-73.561282|42.978918,-69.672122'}
    boston_geocode = maps.get_geocode('Boston, MA', optional_args={'bounds': rgn_bounds['MA']})
    print boston_geocode
    
    dist_matrx = maps.get_distance(['Boston, MA', 'Burlington, VT'], ['New York, NY'])
    #waltham_to_boston = maps.get_distance('Boston, MA', 'New York, NY')
    print dist_matrx

