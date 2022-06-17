# Beginner Runner’s Route Generator

## Motivation
Idea: Build a program that would help beginner road runners achieve better outdoor training sessions--the 3 most common types being:

1. Fartlek: unstructured runs where periods of faster running are mixed with periods of easy-paced or moderate-paced running.

2. Tempo: sustained effort run that builds up the body’s ability to run faster for longer periods of time.

3. Interval: alternating short bursts of intense activity with longer periods of less intense activity or even rest.

These methods improve performance by polishing a runners' mechanics and sense of pace. All three require a level of 'flow', which is best achieved by access to a track or treadmill. 

Conflict: Beginners often find themselves training outdoors without convenient access to such tools. As such, they risk spending their entire workout preoccupied with the navigation of unfamiliar terrain. 

## Audience and Features
Solution: Build a route generator which would solve these challenges and improve beginner race performance by offering three features:

1. Ability to specify any land-based start point in the world.

2. Ability to specify a general direction and goal distance, (including the 4 most common World Athletics categories: 5K, 10K, 21K, 42K).

3. Generating the straightest possible route to avoid overwhelming runners with constant directional changes.

## Datasets and Engineering
Building these features required the use of map data in Python via the OpenStreetMaps API, in addition to the NetworkX and OSMnx libraries to represent that data as a graph. This graph of UBC (my chosen location) has a circle for each location marker (vertex) and a line for each path (node). 

![](https://github.com/mattguev/cool-runnings/blob/main/ubc_map_elevation.png?raw=true)

Only then was it possible to run the computations and algorithms that would enable each feature. For example:
- Feature 1: OSMnx contains a function which allows users to specify a point anywhere in the loaded graph using vertex longitude and latitude markers.
- Feature 2: NetworkX and OSMnx can compute the total length represented by a set of connected vertices (i.e. a route)
- Feature 3: built by applying a Depth-First Search algorithm to the map data, constrained by the parameters above in addition to a bias toward minimizing the bearing difference (amount of turning) along the way.

## Results and Visualization
The final visualizations--an interactive map stored as an html file--were produced using the Folium library in Python. Here, users can inspect the route for any unclear directions before their run. It also contains the total elevation gain for the route. Two versions of the interactive map are presented below:

Route Ver. 1 (naive): No other specifications aside from the start location, goal distance, and initial direction. In essence, this represents the typical route that a beginner might find themselves on when they first attempt a 5k. It is full of inefficient twists and turns that make it hard to remember the trail for future training attempts.

![](https://github.com/mattguev/cool-runnings/blob/main/UBCnaive_5k.JPG?raw=true)

Route Ver. 2 (sophisticated): Contains an additional specification to minimize the number of sharp turns on the path. It is visibly straighter, and therefore easier to reproduce for more consistent training sessions. 

![](https://github.com/mattguev/cool-runnings/blob/main/UBCroute_5k.JPG?raw=true)

