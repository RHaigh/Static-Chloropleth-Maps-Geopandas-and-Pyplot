# Import required libraries

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import contextily as ctx
import folium

# Note that setup of geopandas can be tricky when utilising pip rather than conda as there are several key dependencies which may not install fully.
# Guidance on correct install can be found here: https://geopandas.org/install.html

# Read in datasets given in reposotory. In this case, we will look at the new cases of Coronavirus reported in the UK on the 16th October 2020 at the local authority level. 
local_auth_data = pd.read_csv('./local_auth_cases.csv')

# We will require the boundary shapefiles of these UK local authorities. These can be found in ESRI shapefile format at: https://geoportal.statistics.gov.uk/datasets/6638c31a8e9842f98a037748f72258ed_0
local_auth_shape = gpd.read_file('./Counties_and_Unitary_Authorities__December_2017__Boundaries_GB-shp/Counties_and_Unitary_Authorities__December_2017__Boundaries_GB.shp')
# Shapefile are read in from the direct user root with geopands read_file function. Note that you must download the entire database and include the .shp layer in your path.

# We will rename local auth name columns for simplicity
local_auth_data = local_auth_data.rename(columns={'name': 'Region'})
local_auth_shape = local_auth_shape.rename(columns={'ctyua17nm': 'Region'})

# Merge by this common column
joined_df = local_auth_shape.merge(local_auth_data, on='Region')

# As with all UK shapefiles, these will be eastings and northings and so must be converted to latitude and longitude
joined_df = joined_df.to_crs(epsg=3857)

# Now we enter in our details
variable = 'Region'
# Enter in our desired min / max bins which will be sorted by shade automatically
vmin, vmax = 0, 200
fig, axis = plt.subplots(1, figsize=(30, 10))
axis.axis('off')
axis.set_title('New Cases', fontdict={'fontsize': '25', 'fontweight' : '3'})
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])
fig.colorbar(sm)

# We are ready to plot and style. cmap may be passed any colorBrewer argument. 
map = joined_df.plot(column=variable, cmap='Blues', linewidth=0.8, ax=axis, edgecolor='0.8', alpha=0.5)

# This will only draw the chloropleth boundaries, we may overlay this onto any of the leaflet provider basemaps
ctx.add_basemap(map, source=ctx.providers.Stamen.TonerLite)
