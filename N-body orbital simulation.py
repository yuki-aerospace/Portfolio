from numpy import *
from matplotlib.pyplot import *
from vpython import *
import time


'''
Noah, Kayla, and Yuki developed the charge class and its methods
'''
mass_of_electron = 9.1093837015e-31 #kg
charge_of_electron = -1.602176634e-19 #C
mass_of_proton = 1.672621898e-27 #kg
charge_of_proton = 1.602176634e-19 #C


class Charge:
   def __init__(self,label, mass_input, q_input, x_input, y_input, z_input, vx_input, vy_input, vz_input):
       self.label = label
       self.mass = mass_input #mass (kg)
       self.pos = array([x_input,y_input,z_input])#position (m)
       self.v = array([vx_input,vy_input,vz_input]) #velocity (m/s)
       self.q = q_input #magnitude(and sign) of charge (C)
   def distance_from_origin(self):
       return linalg.norm(self.pos)
   def distance_from_self_to_other(self,other):
       return linalg.norm(self.pos-other.pos)
   def force_on_self_from_other(self,other):
       ke = 8.99e9
       force = zeros(3, float)
       if self.label == other.label:
           return force
       else:
           if self.pos[0] != other.pos[0] or self.pos[1] != other.pos[1] or self.pos[2] != other.pos[2]:
               force = ((ke*self.q*other.q*(self.pos-other.pos))/(self.distance_from_self_to_other(other))**3)
               return force
           else:
               force = zeros(3, float)
               return force
   def sum_of_forces_on_self_from_others(self,list_of_others):
       force = zeros(3, float)
       for other in list_of_others:
           force += self.force_on_self_from_other(other)
       return force


def charges_to_r_vec(list_of_charges): #creates an r vector that records positions and velocities of each particle
       r_vec = zeros([len(list_of_charges)*6],float)
       for j in range(len(list_of_charges)):
           charge_j = list_of_charges[j]
           r_vec[6*j]   = charge_j.pos[0]
           r_vec[6*j+1] = charge_j.pos[1]
           r_vec[6*j+2] = charge_j.pos[2]
           r_vec[6*j+3] = charge_j.v[0]
           r_vec[6*j+4] = charge_j.v[1]
           r_vec[6*j+5] = charge_j.v[2]
       return r_vec
#print(charges_to_r_vec(charge_list))


def f_vec(list_of_charges,r_vec,t): #creates an f vector that returns the component derivatves of the r vector
   derivs = zeros([len(r_vec)],float) #numpy array the same length as r_vec
   for j in range (len(list_of_charges)):
       charge_j = list_of_charges[j]
       derivs[6*j]   = r_vec[6*j+3]
       derivs[6*j+1] = r_vec[6*j+4]
       derivs[6*j+2] = r_vec[6*j+5]
       acceleration  = charge_j.sum_of_forces_on_self_from_others(list_of_charges)\
                       /charge_j.mass
       derivs[6*j+3] = acceleration[0]
       derivs[6*j+4] = acceleration[1]
       derivs[6*j+5] = acceleration[2]
   return derivs
#print(f_vec(charge_list,1))


def find_r0_vec(list_of_charges): #finds the initial state of the system before any differential approximation has happened
   r0_vec = zeros([len(list_of_charges)*6],float)
   for j in range(len(list_of_charges)):
       charge_j = list_of_charges[j]
       r0_vec[6*j]   = charge_j.pos[0]
       r0_vec[6*j+1] = charge_j.pos[1]
       r0_vec[6*j+2] = charge_j.pos[2]
       r0_vec[6*j+3] = charge_j.v[0]
       r0_vec[6*j+4] = charge_j.v[1]
       r0_vec[6*j+5] = charge_j.v[2]
   return r0_vec


#'find trajectories' functions create a list of r vectors that track the positions and velocities of
#  all particles through time using a particular numerical integration method


def find_trajectories_Euler(list_of_charges):
   r0_vec = find_r0_vec(list_of_charges)
   list_of_r_vecs = [r0_vec]
   for j in range(N):
       rj_vec = list_of_r_vecs[-1]
       rjplus1_vec = rj_vec + h*f_vec(list_of_charges, rj_vec, j*h)
       list_of_r_vecs.append(rjplus1_vec)
      
       for k in range(len(list_of_charges)):
           charge_k = list_of_charges[k]
           charge_k.pos[0] = rjplus1_vec[6*k]
           charge_k.pos[1] = rjplus1_vec[6*k+1]
           charge_k.pos[2] = rjplus1_vec[6*k+2]
           charge_k.v[0] = rjplus1_vec[6*k+3]
           charge_k.v[1] = rjplus1_vec[6*k+4]
           charge_k.v[2] = rjplus1_vec[6*k+5]
         
   return list_of_r_vecs


def find_trajectories_RungeKutta4(list_of_charges): #4th Order Runge-Kutta Method
   r0_vec = find_r0_vec(list_of_charges)
   list_of_r_vecs = [r0_vec]
   for j in range(N):
       rj_vec = list_of_r_vecs[-1]
       k1 = h*f_vec(list_of_charges,rj_vec,j)
       k2 = h*f_vec(list_of_charges,rj_vec + (1/2)*k1, j + (1/2)*h)
       k3 = h*f_vec(list_of_charges,rj_vec + (1/2)*k2, j + (1/2)*h)
       k4 = h*f_vec(list_of_charges,rj_vec + k3, j + h)
       rjplus1_vec = rj_vec + (1/6)*(k1 + 2*k2 + 2*k3 + k4)
       list_of_r_vecs.append(rjplus1_vec)
      
       for k in range(len(list_of_charges)):
           charge_k = list_of_charges[k]
           charge_k.pos[0] = rjplus1_vec[6*k]
           charge_k.pos[1] = rjplus1_vec[6*k+1]
           charge_k.pos[2] = rjplus1_vec[6*k+2]
           charge_k.v[0] = rjplus1_vec[6*k+3]
           charge_k.v[1] = rjplus1_vec[6*k+4]
           charge_k.v[2] = rjplus1_vec[6*k+5]
          
   return list_of_r_vecs


def find_trajectories_RungeKutta2(list_of_charges): #2th Order Runge-Kutta Method
   r0_vec = find_r0_vec(list_of_charges)
   list_of_r_vecs = [r0_vec]
   for j in range(N):
       rj_vec = list_of_r_vecs[-1]
       k1 = h*f_vec(list_of_charges,rj_vec,j)
       k2 = h*f_vec(list_of_charges,rj_vec + (1/2)*k1, j + (1/2)*h)
       rjplus1_vec = rj_vec + k2
       list_of_r_vecs.append(rjplus1_vec)
      
       for k in range(len(list_of_charges)):
           charge_k = list_of_charges[k]
           charge_k.pos[0] = rjplus1_vec[6*k]
           charge_k.pos[1] = rjplus1_vec[6*k+1]
           charge_k.pos[2] = rjplus1_vec[6*k+2]
           charge_k.v[0] = rjplus1_vec[6*k+3]
           charge_k.v[1] = rjplus1_vec[6*k+4]
           charge_k.v[2] = rjplus1_vec[6*k+5]
          
   return list_of_r_vecs


#The following code creates a user interface in order to customize the system


print('Welcome to Kayla, Yuki, and Noah*s Charged Particle Modeling System')
time.sleep(1.3)
print('Do you want to use a preset list of charges ?')
time.sleep(1.3)
options = ['1.) Six Equidistant Electrons','2.)Six Equidistant Protons','3.) Four Curving Electrons']
print('Available Options Are')
time.sleep(1.3)
print(options)
time.sleep(1.3)
Q = str(input('enter y or n:'))
if Q == 'n': #this path allows user to completely customize a list of charges
       print('You may now create your own list of charges')
       num = int(input('Number of Charges ='))
       charge_list = []
       for j in range(num):
           Q = input('Do you want a preset charged particle? (enter y or n):')
           if Q == 'y': #this path allows user to pick a proton or electron for a particle
               Q = input('Proton or Electron ? (enter p or e):')
               if Q == 'p':
                   mass = mass_of_proton
                   charge = charge_of_proton
                   #print('mass = ', mass, 'kg')
                   #print('charge = ', charge, 'C')
               if Q == 'e':
                   mass = mass_of_electron
                   charge = charge_of_electron
                   #print('mass = ', mass, 'kg')
                   #print('charge = ', charge, 'C')
           else:
               mass = float(input('mass of particle (kg) ='))
               charge = float(input('charge of particle (C) ='))


           position_list = [float(input('x-position of particle (m) =')),\
                            float(input('y-position of particle (m) =')),\
                            float(input('z-position of particle (m) ='))]
           position_vec = array(position_list)
           velocity_list = [float(input('x-velocity of particle (m/s) =')),\
                            float(input('y-velocity of particle (m/s) =')),\
                            float(input('z-velocity of particle (m/s) ='))]
           velocity_vec = array(velocity_list)
          
           charge_list.append(Charge(str(j),mass,charge,position_list[0],position_list[1],position_list[2],\
                                   velocity_list[0],velocity_list[1],velocity_list[2]))   
if Q == 'y': #This path allows user to pick a preset list of charges
       e1 = Charge('1',mass_of_electron,charge_of_electron,1,0,0,0,0,0)
       e2 = Charge('2',mass_of_electron,charge_of_electron,0,1,0,0,0,0)
       e3 = Charge('3',mass_of_electron,charge_of_electron,0,0,1,0,0,0)
       e4 = Charge('4',mass_of_electron,charge_of_electron,-1,0,0,0,0,0)
       e5 = Charge('5',mass_of_electron,charge_of_electron,0,-1,0,0,0,0)
       e6 = Charge('6',mass_of_electron,charge_of_electron,0,0,-1,0,0,0)
       list1 = [e1,e2,e3,e4,e5,e6]
       p1 = Charge('1',mass_of_proton,charge_of_proton,1,0,0,0,0,0)
       p2 = Charge('2',mass_of_proton,charge_of_proton,0,1,0,0,0,0)
       p3 = Charge('3',mass_of_proton,charge_of_proton,0,0,1,0,0,0)
       p4 = Charge('4',mass_of_proton,charge_of_proton,-1,0,0,0,0,0)
       p5 = Charge('5',mass_of_proton,charge_of_proton,0,-1,0,0,0,0)
       p6 = Charge('6',mass_of_proton,charge_of_proton,0,0,-1,0,0,0)
       list2 = [p1,p2,p3,p4,p5,p6]
       c1 = Charge('one', mass_of_electron, 2*charge_of_electron, -1.2,-1.1,0,8,2,0)
       c2 = Charge('two', mass_of_electron, 2*charge_of_electron, 1.1,1.2,0,0,-7,0)
       c3 = Charge('three', mass_of_electron, 2*charge_of_electron, 1.3,-1.4,0,13,14,0)
       c4 = Charge('four', mass_of_electron, 2*charge_of_electron, -.5,1.2,0,10,0.9,0)
       list3 = [c1,c2,c3,c4]
       preset_charge_lists = [list1, list2, list3]
       choice = int(input('enter 1 / 2 / 3 :'))
       charge_list = preset_charge_lists[choice-1]
diff_options_list = ['Euler*s method','2nd Order Runge-Kutta','4th Order Runge-Kutta']


dimension_choice = str(input('2-Dimensional or 3-Dimensional model ? (enter 2D or 3D):'))
if dimension_choice == '2D': #this path outputs a 2D x-y plot of the trajectories for an arbitrary number of particles
   print('What Numerical Differentiation Method will be used ?')
   time.sleep(1.3)
   print('Available Options Are')
   time.sleep(1.3)
   print(diff_options_list)
   time.sleep(1.3)
   diff_choice = str(input('enter E / RK2 / RK4 :'))
   print('Use Default Step Size and Number of Steps ?')
   time.sleep(1.3)
   print('defaults are, h = 0.1 sec N = 10')
   time.sleep(1.3)
   step_choice = str(input('enter y/n :'))
   if step_choice == 'y':
       h = 0.1 #sec
       N = 10 #steps
   if step_choice == 'n':
       h = float(input('Differentiation Step Size (s) =')) #seconds
       N = int(input('Number of Differentiation Steps =')) #number of steps  
   if diff_choice == 'E':
       list_of_r_vecs = find_trajectories_Euler(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)
   if diff_choice == 'RK2':
       list_of_r_vecs = find_trajectories_RungeKutta2(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)
   if diff_choice == 'RK4':
       list_of_r_vecs = find_trajectories_RungeKutta4(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)


   color_list = ['ko', 'ro', 'yo', 'go', 'co', 'bo', 'mo']
   if len(charge_list) > len(color_list):
       for j in range (len(charge_list)-len(color_list)):
           color_list.append(color_list[j])
          
   for j in range(len(charge_list)):
       plot(array_of_r_vecs[:,6*j],array_of_r_vecs[:,6*j+1],color_list[j])
  
   title('Trajectories of Charged Particles')
   xlabel('x-position (meters)')
   ylabel('y-position (meters)')
   axis("square")
   show()
  
if dimension_choice == '3D':
   print('What Numerical Differentiation Method will be used ?')
   time.sleep(1.3)
   print('Available Options Are')
   time.sleep(1.3)
   print(diff_options_list)
   time.sleep(1.3)
   diff_choice = str(input('enter E / RK2 / RK4 :'))
   print('Use Default Step Size and Number of Steps ?')
   time.sleep(1.3)
   print('defaults are, h = 0.1 sec N = 100')
   time.sleep(1.3)
   step_choice = str(input('enter y/n :'))
   if step_choice == 'y':
       h = 0.1 #sec
       N = 100 #steps
   if step_choice == 'n':
       h = float(input('Differentiation Step Size (s) =')) #seconds
       N = int(input('Number of Differentiation Steps =')) #number of steps  
   if diff_choice == 'E':
       list_of_r_vecs = find_trajectories_Euler(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)
   if diff_choice == 'RK2':
       list_of_r_vecs = find_trajectories_RungeKutta2(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)
   if diff_choice == 'RK4':
       list_of_r_vecs = find_trajectories_RungeKutta4(charge_list)
       array_of_r_vecs = array(list_of_r_vecs)
    
  
   scene.title = "Interaction of Charged Masses"
   number_of_charges = len(charge_list)


   # form box in simulation for reference frame; use max position in any direction to scale the box
   max_list = []
   for k in range(0, number_of_charges):
       x_max = abs(list_of_r_vecs[-1][6*k])
       y_max = abs(list_of_r_vecs[-1][6*k+1])
       z_max = abs(list_of_r_vecs[-1][6*k+2])
       max_list.append(x_max)
       max_list.append(y_max)
       max_list.append(z_max)
   max_list.sort()
   max_pos = max_list[-1]


   x_length, y_length , z_length = 2*max_pos, 2*max_pos, 2*max_pos
   boundaries = [
      box(pos = vector(0,-y_length/2,0), size = vector(x_length, .2, z_length), opacity = 0.5),
      box(pos = vector(0,y_length/2,0), size = vector(x_length, .2, z_length), opacity = 0.5),
      box(pos = vector(-x_length/2,0,0), size = vector(.2, y_length, z_length), opacity = 0.5),
      box(pos = vector(x_length/2,0,0), size = vector(.2, y_length, z_length), opacity = 0.5),
      box(pos = vector(0,0,-z_length/2), size = vector(x_length, y_length, .2), opacity = 0.5)
      ]


   # initialize charges as spheres in initial position; size radius in reference to final frame
   origin = sphere(pos=vector(0,0,0), radius=max_pos/100, color=color.black)


   # create a list of colors in ROY G BIV order so that the charges can be distinguished consecutively
   color_list = [color.red, color.orange, color.yellow, color.green, color.cyan, color.blue, color.magenta, color.white]
   if len(charge_list) > len(color_list):
       for j in range (len(charge_list)-len(color_list)):
           color_list.append(color_list[j])


   sphere_list = []
   for k in range(0, number_of_charges): # algebraic representation works for charge labeled 1 to be first element (0)
       new_sphere = sphere(pos = vector(list_of_r_vecs[0][6*k], list_of_r_vecs[0][6*k+1], list_of_r_vecs[0][6*k+2]), radius=max_pos/25,color=color_list[k])
       sphere_list.append(new_sphere)


   start_time = time.time() # relative start time of simulation set
   for j in range(0, N):
       rate(5) # so that # of calc. is reasonable to time per second


       for k in range(0, number_of_charges):
          sphere_list[k].pos = vector(list_of_r_vecs[j][6*k], list_of_r_vecs[j][6*k+1], list_of_r_vecs[j][6*k+2])


   # calculate elapsed time
       elapsed_time = int(time.time() - start_time)


       # convert second to hour, minute and seconds
       elapsed_hour = elapsed_time // 3600
       elapsed_minute = (elapsed_time % 3600) // 60
       elapsed_second = (elapsed_time % 3600 % 60)


       # print as 00:00:00 in vpython
       elapsed_time = (str(elapsed_hour).zfill(2) + ":" + str(elapsed_minute).zfill(2) + ":" + str(elapsed_second).zfill(2))


       time_label = label( pos= vector(0, y_length/2, z_length/2), text = '')
   
       time_label.text = 'Elapsed Time: ' + elapsed_time   



