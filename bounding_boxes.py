from pascal_voc_writer import Writer

import carla
import math
import random
import time
import queue
import numpy as np
import cv2

client = carla.Client('localhost', 2000)
client.reload_world()
world  = client.get_world()
bp_lib = world.get_blueprint_library()

spawn_points = world.get_map().get_spawn_points()

vehicle_bp =bp_lib.find('vehicle.lincoln.mkz_2020')
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

camera_bp = bp_lib.find('sensor.camera.rgb')
camera_init_trans = carla.Transform(carla.Location(z=2))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
vehicle.set_autopilot(True)

settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

image_queue = queue.Queue()
camera.listen(image_queue.put)

def build_projection_matrix(w, h, fov):
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K


def get_image_point(loc, K, w2c):
        point = np.array([loc.x, loc.y, loc.z, 1])
        point_camera = np.dot(w2c, point)

        point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

        point_img = np.dot(K, point_camera)
        point_img[0] /= point_img[2]
        point_img[1] /= point_img[2]

        return point_img[0:2]

world_2_camera = np.array(camera.get_transform().get_inverse_matrix())

# Get the attributes from the camera
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
fov = camera_bp.get_attribute("fov").as_float()

K = build_projection_matrix(image_w, image_h, fov)

for i in range(50):
    vehicle_bp = random.choice(bp_lib.filter('vehicle'))
    npc = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
    if npc:
        npc.set_autopilot(True)

bounding_box_set = world.get_level_bbs(carla.CityObjectLabel.TrafficLight)
bounding_box_set.extend(world.get_level_bbs(carla.CityObjectLabel.TrafficSigns))

edges = [[0,1], [1,3], [3,2], [2,0], [0,4], [4,5], [5,1], [5,7], [7,6], [6,4], [6,2], [7,3]]

while True:
    world.tick()
    image = image_queue.get()

    img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))

    world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
    
    # frame_path = 'output/%06d' % image.frame

    # # Save the image
    # image.save_to_disk(frame_path + '.png')

    # # Initialize the exporter
    # writer = Writer(frame_path + '.png', image_w, image_h)

    for bb in bounding_box_set:

        if bb.location.distance(vehicle.get_transform().location) < 50:

            forward_vec = vehicle.get_transform().get_forward_vector()
            ray = bb.location - vehicle.get_transform().location

            if forward_vec.dot(ray) > 1:
                verts = [v for v in bb.get_world_vertices(carla.Transform())]
                for edge in edges:
                    p1 = get_image_point(verts[edge[0]], K, world_2_camera)
                    p2 = get_image_point(verts[edge[1]],  K, world_2_camera)
                    cv2.line(img, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), (0,0,255, 255), 1)
    
    for npc in world.get_actors().filter('*vehicle*'):
        if npc.id != vehicle.id:

            bb = npc.bounding_box
            dist = npc.get_transform().location.distance(vehicle.get_transform().location)

            if dist < 50:
                forward_vec = vehicle.get_transform().get_forward_vector()
                ray = npc.get_transform().location - vehicle.get_transform().location

                if forward_vec.dot(ray) > 4:
                    p1 = get_image_point(bb.location, K, world_2_camera)
                    verts = [v for v in bb.get_world_vertices(npc.get_transform())]
                    
                    #######################
                    # Draw 3D bbox
                    #######################
                    for edge in edges:
                        p1 = get_image_point(verts[edge[0]], K, world_2_camera)
                        p2 = get_image_point(verts[edge[1]],  K, world_2_camera)
                        cv2.line(img, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), (255,0,0, 255), 1)

                    #######################
                    # Draw 2D bbox and write to PASCOL VOC format
                    #######################

                    # p1 = get_image_point(bb.location, K, world_2_camera)
                    # verts = [v for v in bb.get_world_vertices(npc.get_transform())]
                    # x_max = -10000
                    # x_min = 10000
                    # y_max = -10000
                    # y_min = 10000

                    # for vert in verts:
                    #     p = get_image_point(vert, K, world_2_camera)
                    #     # Find the rightmost vertex
                    #     if p[0] > x_max:
                    #         x_max = p[0]
                    #     # Find the leftmost vertex
                    #     if p[0] < x_min:
                    #         x_min = p[0]
                    #     # Find the highest vertex
                    #     if p[1] > y_max:
                    #         y_max = p[1]
                    #     # Find the lowest  vertex
                    #     if p[1] < y_min:
                    #         y_min = p[1]

                    # cv2.line(img, (int(x_min),int(y_min)), (int(x_max),int(y_min)), (0,0,255, 255), 1)
                    # cv2.line(img, (int(x_min),int(y_max)), (int(x_max),int(y_max)), (0,0,255, 255), 1)
                    # cv2.line(img, (int(x_min),int(y_min)), (int(x_min),int(y_max)), (0,0,255, 255), 1)
                    # cv2.line(img, (int(x_max),int(y_min)), (int(x_max),int(y_max)), (0,0,255, 255), 1)
                
                # Add the object to the frame (ensure it is inside the image)
                # if x_min > 0 and x_max < image_w and y_min > 0 and y_max < image_h: 
                #     writer.addObject('vehicle', x_min, y_min, x_max, y_max)

    cv2.imshow('ImageWindowName',img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
# writer.save(frame_path + ".xml")