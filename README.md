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
Building these features required the use of map data in Python via the OpenStreetMaps API, as well as the NetworkX and OSMnx libraries to represent that data as a graph. In this representation of the UBC map data I chose, each circle was a location marker (vertex) and each line was a path (node). 

![](https://github.com/mattguev/cool-runnings/blob/main/ubc_map.png?raw=true)

Only then was it possible to run the computations and algorithms required to enable each feature. For example:
- Feature 1 was realized because OSMnx contains a function which allows users to specify a point anywhere in the loaded graph using vertex longitude and latitude markers.
- Feature 2 was realized because NetworkX and OSMnx can compute the total length represented by a set of connected vertices (i.e. a route)
- Feature 3 was built by applying a Depth-First Search algorithm to the map data, constrained by the parameters of Features 1 and 2, in addition to a bias toward minimizing the bearing difference (amount of turning) to be done at each vertex.

## Results and Visualization
The final visualization--an interactive map--was produced using the Folium library in Python. Here, users can inspect the route for any unclear directions before their run. It also contains the total elevation gain for the route. A screenshot of the final interactive page is provided below.
 
![](https://github.com/mattguev/cool-runnings/blob/main/UBCroute_5k.JPG?raw=true)

