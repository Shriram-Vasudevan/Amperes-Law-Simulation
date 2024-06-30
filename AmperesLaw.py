Web VPython 3.2
import random 

scene = canvas(title='Ampere\'s Law Simulation: Current Carrying Wire', width=800, height=600, align = "left")

scene.userzoom = True
scene.userspin = False

# Constants
mu0 = 4 * pi * 1e-7  # Permeability of free space
I = 1  # Current in amperes

wire_length = 10
wire_start = vector(0, 0, -5)
wire_end = vector(0, 0, 5)
wire_radius = 0.005
num_wire_segments = 100


arrow_scale = 0.3


dl = vector(0, 0, 1) * wire_length / num_wire_segments

wire = cylinder(pos = wire_start, radius = wire_radius, axis = wire_end - wire_start, color = color.green)

#current_arrow = arrow(pos = vector(0, -1, 0), axis = vector(0, 0, 1), color = color.purple)

loop_points = []
loop_positions = []
loop_length_vectors = []
loop_completed = False  
arrows = []
lines = []


total_magnetic_circulation = 0.0

initial_camera_pos = scene.camera.pos
initial_userspin = scene.userspin
initial_userzoom = scene.userzoom

def calculate_field():
    total_magnetic_circulation = 0.0
    print("Angle (deg)"+"\t"+"Length (m)" +"\t"+ "Magnetic Field (T)")
    
    global total_magnetic_circulation, arrow_scale
    list_length = len(loop_positions)
    
    for i in range(list_length):
        mag_field_contribution = vector(0, 0, 0)
        
        for j in range(num_wire_segments):
            wire_piece = vector(0, 0, wire_start.z + (dl.z / 2) + (dl.z) * j)
            displacement_vector = loop_positions[i] - wire_piece
       
            dB = (mu0 * I * cross(dl, displacement_vector)) / (4 * pi * mag(displacement_vector) ** 3)
            mag_field_contribution += dB 
         
            mag_scale = arrow_scale / mag(dB)
            mag_arrow = arrow(pos = loop_positions[i], axis = mag_scale * dB, color=color.red)
            arrows.append(mag_arrow)
            
        angle = diff_angle(mag_field_contribution, loop_length_vectors[i]) * 180 / pi
        loop_length = mag(loop_length_vectors[i])
        mag_field_circulation = dot(mag_field_contribution, loop_length_vectors[i])
        
        print(f'{round(angle, 1)} \t\t\t {round(loop_length, 3)} \t\t {mag(mag_field_contribution)}')
        
        total_magnetic_circulation += mag_field_circulation
    
    print(f'The total magnetic circulation is: {total_magnetic_circulation} Tm')

def add_point_to_loop(pos):
    global loop_completed
    num_markers = len(loop_points)
    if (num_markers < 1):
        marker = sphere(pos = pos, radius = 0.05, color = color.cyan)
        loop_points.append(marker)
    else:
        difference_vector = pos - loop_points[0].pos
        #print(f"The distance is {sqrt(difference_vector.x **2 + difference_vector.y **2)}")
        if (sqrt(difference_vector.x **2 + difference_vector.y **2) < 0.1):
            line = curve(pos = [loop_points[num_markers - 1].pos, loop_points[0].pos], radius = 0.01)
            lines.append(line)
            loop_positions.append((loop_points[num_markers - 1].pos + loop_points[0].pos) / 2)
            loop_length_vectors.append(loop_points[0].pos - loop_points[num_markers - 1].pos)
            loop_completed = True
        else:
            marker = sphere(pos = pos, radius = 0.03, color = color.red)
            loop_points.append(marker)
            line = curve(pos = [loop_points[num_markers - 1].pos, loop_points[num_markers].pos], radius = 0.01)
            lines.append(line)
            loop_positions.append((loop_points[num_markers - 1].pos + loop_points[num_markers].pos) / 2)
            loop_length_vectors.append(loop_points[num_markers].pos - loop_points[num_markers - 1].pos)
        
        
def down(): 
    global loop_completed
    pick = scene.mouse.pick
    
    if (pick == wire):
        print("Don't Click on the Wire!")
    elif !loop_completed:
        pos = scene.mouse.pos
        pos.z = 0
        add_point_to_loop(pos)
    
def change_scale(scale):
    global arrow_scale
    arrow_scale = scale.value
    print(arrow_scale)
    
def change_cam_lock(active):
    scene.userspin = active.checked
    print(f"3D Mode: {active.checked}")
    
def clear_all():
    global loop_points, loop_positions, loop_length_vectors, arrows, loop_completed, total_magnetic_circulation, lines
    
    for marker in loop_points:
        marker.visible = False
    loop_points = []
    
    for arrow_obj in arrows:
        arrow_obj.visible = False    
    arrows = []
    
    for line in lines:
        line.visible = False
    lines = []
    
    loop_positions = []
    loop_length_vectors = []
    loop_completed = False
    total_magnetic_circulation = 0.0

def return_to_initial_position():
    scene.camera.pos = initial_camera_pos
    scene.userspin = initial_userspin
    scene.userzoom = initial_userzoom
    

scene.bind("mousedown", down)

wtext(text='\tAdjust Arrow Scale:')
scale_slider = slider(bind=change_scale, min=0.1, max=0.5, value=0.3)

scene.append_to_caption('\n\n\t')
button(text = "Calculate Circulation", bind = calculate_field)

scene.append_to_caption('\n\n\t')
button(text="Clear", bind=clear_all)

scene.append_to_caption('\n\n\t')
checkbox(text='Unlock Camera', bind=change_cam_lock, checked=False)


scene.append_to_caption('\n\n\t')
    