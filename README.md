# Boids

This is a program I wrote because I thought it would be an interesting project. It was and I highly recommend everyone to try this out themself.

I used 3 rules and some optimizations to create this simulation and feel free to use my code as you like.


## Rules

### Alignment
Boids will align with other boids closeby that are of the same type.
### Cohesion
Boids will go the center of mass of other boids closeby that are also of the same type.
### Seperation
Boids will avoid other boids closeby of all types as to not collide.


## Optimizations

### Spatial Hash Grid
This is a grid that divides the entire world up into cells, each cell contains boids.
Now we can get all boids close to a boid by looking at the cell it is in or/and the cells adjacent to that cell.

### Getting the boids only once
Some implementations I have seen get the boids for each rule, however I thought it would be better to just get close boids once per boid.


## Flock
This is an object I created that handles most of the boid behaviour.

### num_boids
The number of Boids to create when the flock is intantiated.

### num_types
The number of different types of boids.

### world_size
The size of the world (width, height).

### cell_size
The size of the Spatial Hash Grid cells.

### max_speed
The maximum speed a boid is permitted to go.

### perception
How many cells around itself a boid may get all close boids.

### field_of_view
The field of view for the boid.

### avoid_dist
The minimum distance to keep from all other boids, if inside this distance the boids move away.


## Credits
Credits to [Sebastian Legue](https://www.youtube.com/channel/UCmtyQOKKmrMVaKuRXz02jbQ) and his [Coding Adventure on Boids](https://www.youtube.com/watch?v=bqtqltqcQhw).

Also credits to [Ben Eater](https://eater.net/) for his [code](https://github.com/beneater/boids) and his [explanation](https://eater.net/boids) about boids.