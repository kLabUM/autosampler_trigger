#!/usr/bin/env python
# coding: utf-8

# In[13]:


from datetime import datetime

import numpy as np
import plotly.graph_objects as go

import requests
import pygrib


# In[14]:


# Function to get 12-hour total preciptation forecast updated at most each hour
def update_weather():
    response = requests.get(
        'http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl?file=hrrr.t{hour}z.wrfsfcf12.grib2&var_APCP=on&subregion=&leftlon=-87&rightlon=-82.25&toplat=45.75&bottomlat=41.5&dir=%%2Fhrrr.{date}%%2Fconus'.format(hour = str(int(datetime.utcnow().strftime('%H')) -2), date = datetime.utcnow().strftime('%Y%m%d')), stream=True)

    # Throw an error for bad status codes
    response.raise_for_status()
    
    # Open grib file we get from NOAA
    grbs = pygrib.open('grib_file.tmp')  
    
    # Rewind the iterator (needed grib operation - unsure what it's for)
    grbs.rewind() 
    
    # Seperate values from parameter name
    t2mens = []
    for grb in grbs:
        if grb.parameterName == 'Total precipitation':
            t2mens.append(grb.values)
    
    # Convert 1-mm to inches
    mm2in = 0.0394; #1 mm = 0.03937 in
    
    # Turn t2mens list into numpy array
    t2mens = np.array(t2mens)
    
    # Get the lats and lons for the grid
    lats, lons = grb.latlons()
    
    # Create numpy arrays
    precip = np.array([])
    lat = np.array([])
    lon = np.array([])

    for m in t2mens[0]:
        precip = np.concatenate( (precip, m) )

    for l in lats:
        lat = np.concatenate( (lat, l))

    for l in lons:
        lon = np.concatenate( (lon, l) )  
        
    # Keep only precip values greater than 0.01-mm (this may need updated)
    keep = precip > 0.01
    precip = precip[keep]
    lon = lon[keep]
    lat = lat[keep]
    
    return lat, lon, precip


# In[16]:


# lats, lons, precip = update_weather()
# fig = go.Figure(go.Densitymapbox(lat = lats, lon = lons, z = precip, radius = 10))


# In[17]:


# fig.update_layout(mapbox_style='stamen-terrain', mapbox_center_lon = np.mean(lons), mapbox_center_lat = np.mean(lats))
# # fig.update_layout(margin={"r":0, "t":0, "1":0, "b":0})
# fig.show()


# In[ ]:




