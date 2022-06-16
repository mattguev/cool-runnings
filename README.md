# Beginner Runner’s Route Generator

## Motivation
The idea here was to build a program that beginner road runners could use to plan their speed work routes. The 3 most common types of speed work are:

1. Fartlek: unstructured runs where periods of faster running are mixed with periods of easy-paced or moderate-paced running
2. Tempo: sustained effort run that builds up your body’s ability to run faster for longer periods of time
3. Interval: alternating short bursts of intense activity with longer periods of less intense activity or even rest.

These training methods improve performance by polishing a runners' mechanics and sense of pace. All three require a level of 'flow' which is best achieved by access to a track or treadmill. Yet, beginners often find themselves without convenient access to such tools. As such, they risk spending their entire workout preoccupied with the navigation of unfamiliar terrain. 

## Audience and Features
With these factors in mind, the objective was to build a route generator for beginners which would eliminate these barriers to road training and improve race performance by offering three features:

1. Runners would be able to specify any land-based start point in the world.

2. Runners would be able to specify a general direction and distance, but would ideally choose 1 of the 4 most common World Athletics categories (5K, 10K, 21K, 42K).

3. The route generator would generate the straightest possible route to avoid overwhelming runners with constant directional changes.

## Engineering
Building these features required access to map data (UBC in my case) in Python using the OpenStreetMaps API (graph_ubc.gml), as well as the networkx and osmnx libraries to represent that data as a graph. In this representation, each vertex was a location marker and each node was a path (ubc_map.png). Only then was it possible to run the computations and algorithms required to enable each feature. For example:
- Feature 1 was realized because osmnx contains a function which allows users to specify a point anywhere in the loaded graph using vertex longitude and latitude markers.
- Feature 2 was realized because networkx and osmnx can compute the total length represented by a set of connected vertices (i.e. a route)
- Feature 3 was built by applying a Depth-First Search algorithm to the map data, constrained by the parameters of Features 1 and 2, in addition to a bias toward minimizing the bearing difference (amount of turning) to be done at each vertex.

## Results and Visualization
The final visualization--an interactive map--was produced using folium. Here, users can inspect the route for any unclear directions before their run.
 
![](https://github.com/mattguev/cool-runnings/blob/main/Project3/UBCroute_5k.JPG?raw=true)

