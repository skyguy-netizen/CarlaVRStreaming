import carla
import random


client = carla.Client("127.0.0.1", 2000)
client.reload_world()
world = client.get_world()

settings = world.get_settings()
settings.syncrhonous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

traffic_manager.set_random_device_seed(0)
random.seed(0)

spectator = world.get_spectator()

spawn_points = world.get_map().get_spawn_points()

# Route 1
spawn_point_1 = spawn_points[32]
route_1_indices = [129, 28, 124, 33, 97, 119, 58, 154, 147 ]
route_1 = []
for ind in route_1_indices:
    route_1.append(spawn_points[ind].location)

# Route 2
spawn_point_2 = spawn_points[149]
route_2_indices = [21, 76, 38, 34, 90, 3]
route_2 = []
for ind in route_2_indices:
    route_2.append(spawn_points[ind].location)

world.debug.draw_string(spawn_point_1.location, 'Spawn point 1', life_time=30, color=carla.Color(255,0,0))
world.debug.draw_string(spawn_point_2.location, 'Spawn point 2', life_time=30, color=carla.Color(0,0,255))

for ind in route_1_indices:
    spawn_points[ind].location
    world.debug.draw_string(spawn_points[ind].location, str(ind), life_time=60, color=carla.Color(255,0,0))

for ind in route_2_indices:
    spawn_points[ind].location
    world.debug.draw_string(spawn_points[ind].location, str(ind), life_time=60, color=carla.Color(0,0,255))

models = ["dodge", "audi", "model3", "mini", "mustang", "lincoln", "prius", "nissan", "crown", "impala"]
blueprints = []
for vehicle in world.get_blueprint_library().filter("vehicle"):
    if any(model in vehicle.id for model in models):
        blueprints.append(vehicle)

##################
# Code to spawn vehicles on autopilot
##################

# max_vehicles = 50
# max_vehicles = min([max_vehicles, len(spawn_points)])
# vehicles = []

# for i, spawn_point in enumerate(spawn_points):
#     # world.debug.draw_string(spawn_point.location, str(i), life_time=10)

#     temp = world.try_spawn_actor(random.choice(blueprints), spawn_point)
#     if temp is not None:
#         vehicles.append(temp)

# for vehicle in vehicles:
#     vehicle.set_autopilot(True)
#     traffic_manager.ignore_lights_percentage(vehicle, random.randint(0, 50))

# while True:
#     try:
#         world.tick()
#     except KeyboardInterrupt:
#         break

##################
# Code to spawn vehicles that follow a route 
##################
spawn_delay = 20
counter = spawn_delay

max_vehicles = 200
alt = False

spawn_points = world.get_map().get_spawn_points()
while True:
    try:
        world.tick()
        n_vehicles = len(world.get_actors().filter("vehicle.*"))
        vehicle_bp = random.choice(blueprints)

        if counter == spawn_delay and n_vehicles < max_vehicles:
            if alt:
                vehicle = world.try_spawn_actor(vehicle_bp, spawn_point_1)
            else:
                vehicle = world.try_spawn_actor(vehicle_bp, spawn_point_2)
            
            if vehicle:
                vehicle.set_autopilot(True)

                traffic_manager.update_vehicle_lights(vehicle, True)
                traffic_manager.random_left_lanechange_percentage(vehicle, 0)
                traffic_manager.random_right_lanechange_percentage(vehicle, 0)
                traffic_manager.auto_lane_change(vehicle, False)

                if alt:
                    traffic_manager.set_path(vehicle, route_1)
                    alt = False
                else:
                    traffic_manager.set_path(vehicle, route_2)
                    alt = True

                vehicle = None

            counter -= 1
        elif counter > 0:
            counter -= 1
        elif counter == 0:
            counter = spawn_delay   
    except KeyboardInterrupt:
        break