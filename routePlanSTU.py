import osmnx as ox
import networkx as nx
from collections import deque
from folium.features import DivIcon
import folium
import random

# # =================================
# STEP 1: LOAD AND SANITY CHECK DATA

# load graph from GML (created via load_map.py)
graph = ox.io.load_graphml('graph_ubc.gml')

# ...................................
# Visualize map for sanity check
fig, ax = ox.plot_graph(graph)
fig.savefig('ubc_map.png')

# ...................................
# Visualize map with elevation for sanity check

nc = ox.plot.get_node_colors_by_attr(graph, 'elevation', cmap='plasma')
fig, ax = ox.plot_graph(graph, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')
fig.savefig('ubc_map_elevation.png')

# =================================
# Route planning with length, bearing, and elevation:
# 1) find any path in the UBC graph whose total distance is > target using dfs
# 2) above plus: take the "straightest" direction out of any vertex
# 3) above plus: report total elevation gain

# Helper function that determines if edge (v,w) is a valid candidate for adding to the graph
def good(gst, d, v, w):
    return v not in list(gst.adj[w]) and \
           graph.edges[v, w, 0]['length'] > 0 \
           and d <= goal_dist

# Helper function that returns the absolute difference between any 2 given directions.
# Note that the value should never be more than 180, since a left turn of x is equivalent to a right turn of (360 - x).
def get_bearing_diff(b1,b2):
    bdiff = min(abs(b1-b2),360-(abs(b1-b2))) # report bdiff such that a diff of 315 deg is equivalent to 45 deg.
    return bdiff

# Main dfs function. Given a start node, goal distance, and graph of distances:
# return a subgraph whose edges are a trail with distance at least goal_distance, and where the definition
# of "neighbors" is such that at every node, the direction of the next edge is as close as possible
# to the current direction.

def find_route(start, goal_dist, graph):
    # distances and feasible edges will come from 'graph', solution built in 'gstate'
    gstate = nx.DiGraph()
    gstate.add_nodes_from(graph)

    # need stack of: (gstate, prev node, curr node, totlen so far, number of edges in route so far)
    # init stack & push start vertex
    stack = deque()
    stack.append((gstate, start, start, 0, 0))
    # next two lines are necessary for part 2) so that every current bearing has a previous bearing to compare against
    graph.add_edge(start, start, 0)
    graph.edges[start, start, 0]['bearing'] = 300 # facing the beach

    while stack:
        gst, prev, curr, lensofar, clock = stack.pop()  # gst, previous node, curr node, dist so far, edges so far

        if curr not in list(gst.neighbors(prev)):
            gst.add_edge(prev, curr)
            gst.edges[prev, curr]['time'] = clock # need this for path drawing

            # stopping criteria: if we've gone far enough, return our solution graph and the number of edges
            if lensofar >= goal_dist:
                return gst, clock

            # neighbors
            neighbors = sorted(graph.neighbors(curr),
                               key=lambda x: get_bearing_diff(graph.edges[prev, curr, 0]['bearing'],
                                                              graph.edges[x,curr, 0]['bearing']))

            for w in neighbors:
                if good(gst, lensofar, curr, w):
                    gstnew = gst.copy() # copy the path so we don't have to deal w backtracking. ok for small graphs.
                    stack.append((gstnew, curr, w, lensofar + graph.edges[curr, w, 0]['length'], clock + 1))

# returns the total elevation gain in gr, over the route described by rt (list of vertices).
# edges whose elevation gain is negative should be ignored.

def total_elevation_gain(gr,rt):
    eg = 0
    # your code here
    for k in range(len(rt)-1):
        gain = gr.nodes[rt[k + 1]]['elevation'] - gr.nodes[rt[k]]['elevation']
        if gain > 0:
            eg += gain
    return eg

# =======================================================
# Main routing code starts here
#
# Choose a starting location.
# Wesbrook Save-On Foods
lat, lon = 49.255, -123.236

start = ox.get_nearest_node(graph, (lat, lon))
startlat, startlon = graph.nodes[start]['y'], graph.nodes[start]['x']


goal_dist = 5000  # meters, must go at least this far

route, time = find_route(start, goal_dist, graph) # call the main dfs function

# variable 'route' is a DiGraph, but we want a sequence of vertices along the solution path.
sorted_lst = sorted(route.edges(), key=lambda x: route.edges[x[0], x[1]]['time'])
routevertices = [i[1] for i in sorted_lst] # edges are tuples of nodes (u,v). 1st set of tuples is pair of start coords, therefore index the 1st

# find coordinates of stopping point: last node on the route
endlat, endlon = graph.nodes[routevertices[-1]]['y'], graph.nodes[routevertices[-1]]['x'] # BUG: previously x, y (places you outside map)

# Part 3
# add an accumulator that sums the total elevation gain over the course of the
# workout. If an edge (u,v) in the graph corresponds to a downhill segment (difference
# in elevations from u to v is negative), then it is ignored.
eg = total_elevation_gain(graph,routevertices) # sums the elevation gain over the route



# =================================
# VISUALIZATION

# Initialize the map plot
kwargs = {'opacity': 0}
m = ox.plot_graph_folium(graph, tiles='openstreetmap', **kwargs)

# Color each edge. route_map=m plots on map m
for k,x in enumerate(sorted_lst[1:]):
    kwargs = {'opacity': 1.0}
    ox.plot_route_folium(graph, x, route_map=m, weight=5, color='blue', **kwargs)

# Need to get the right zoom level for the whole route.
# Going to take a 1200m radius from the start location. bbox stands for bounding box
bbox = ox.utils_geo.bbox_from_point((startlat, startlon), dist=1200)
swne = [(min(bbox[0:2]),min(bbox[2:4])),(max(bbox[0:2]),max(bbox[2:4]))]
m.fit_bounds(swne)

# Place the elevation gain on the map at the end point of the workout.
folium.map.Marker(
    [endlat, endlon],
    icon=DivIcon(
        icon_size=(250,36),
        icon_anchor=(0,0),
        html=f'<div style="font-size: 20pt">Elevation Gain: {eg}m</div>',
    )
).add_to(m)

# add green start circle
folium.CircleMarker((startlat,startlon),
                    color='green',radius=5,fill=True).add_to(m)
# add red end circle
# your code here
folium.CircleMarker((endlat,endlon),
                    color='red',radius=5,fill=True).add_to(m)

filepath = "route_graph_workout.html"
m.save(filepath)