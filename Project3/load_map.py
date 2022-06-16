import osmnx as ox
import networkx as nx
import requests
import pandas as pd


addr = "UBC Vancouver, BC, Canada"

graph = ox.graph_from_address(addr, dist=4000, dist_type="network", network_type='walk', simplify=True)
ox.add_edge_bearings(graph, precision=1)

# convert to GeoDataFrames
# our application uses the geodfs to simplify the assembly of elevation data at each node
gdfs = ox.graph_to_gdfs(graph)
node_gdfs, edge_gdfs = gdfs


# =======================================
# Attach elevation data to each node using open-elevation API
# The API is quite slow and isn't very reliable 1000 records at a time. 
# It might fail with 504 but eventually will work after a few tries :D 
# (Please double check the code, maybe it's something that I've overlooked)
# Chose this API because it doesn't limit the number of records with its post requests.


# get elevation of nodes
BASE_URL = "https://api.open-elevation.com/api/v1/lookup"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

locations = node_gdfs.loc[:, ['y', 'x']]
locations.columns = ["latitude", "longitude"]
locations = locations.to_dict('records')


max_altitude_query_size = 1000
count = 0
altitude_records = []
while count < len(locations):
    query_end_ind = min(count + max_altitude_query_size, len(locations))
    data = {
        "locations": locations[count:query_end_ind]
    }
    response = requests.post(BASE_URL, headers=headers, json=data)
    if response:
        content = response.json()
        altitude_records += content['results']
        count = query_end_ind
        print("retrieved %d altitude records" % query_end_ind)
    else:
        print("retrieval failed at %d, retrying..." % query_end_ind)


result = pd.DataFrame.from_records(altitude_records, index=node_gdfs.index)
nx.set_node_attributes(graph, name="elevation", values=result["elevation"].to_dict())

# save graph to GraphML on disk for later use
ox.io.save_graphml(graph, filepath='graph_ubc.gml')

# =================================
# Visualize general map
fig, ax = ox.plot_graph(graph)
fig.savefig('ubc_map.png')

# =================================
# Visualize map with elevation

nc = ox.plot.get_node_colors_by_attr(graph, 'elevation', cmap='plasma')
fig, ax = ox.plot_graph(graph, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')
fig.savefig('ubc_map_elevation.png')

