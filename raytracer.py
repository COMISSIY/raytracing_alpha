import pygame, math, numba
pygame.init()

w, h = 600, 400
sc = pygame.display.set_mode((w, h))
x_a = 0
y_a = 0
z_a = 0
def intersect(ro, rd, ce, ra):
	oc = ro - ce
	b = oc.dot(rd)
	c = oc.dot(oc) - ra ** 2
	h = b ** 2 - c
	
	if h < 0:
		return pygame.Vector2(-1)
	h = math.sqrt(h)
	return pygame.Vector2(-b - h, -b+h)

def rotated_y(p, a):
	x = p[0]*math.cos(a)+p[2]*math.sin(a)
	y = p[1]
	z = -p[0]*math.sin(a)+p[2]*math.cos(a)
	return pygame.Vector3((x, y, z))

def rotated_x(p, a):
	x = p[0]
	y = p[1]*math.cos(a)+p[2]*math.sin(a)
	z = -p[1]*math.sin(a)+p[2]*math.cos(a)
	return pygame.Vector3((x, y, z))

def rotated_z(p, a):
	x = p[0]*math.cos(a)-p[1]*math.sin(a)
	y = p[0]*math.sin(a)+p[1]*math.cos(a)
	z = p[2]
	return pygame.Vector3((x, y, z))

def plaIntersect(ro, rd, p):
	a = rd.dot(p.xyz)
	if a == 0:
		a = 0.001
	return -(ro.dot(p.xyz) + 1) / a

# def distance(a, b):
# 	return math.sqrt(a.x**2-b.x**2+a.y**2-b.y**2+a.z**2-b.z**2)

point = pygame.Vector3((50, -10, 0))
x_d, y_d = 300, 200
c_pos = pygame.Vector3((50, 0, -50))
a = 0
ratio = w/h

sun = pygame.Vector3((0, -1000, 0))

def raycast():
	for x in range(-300, 300, res):
		# z += 0.1
		for y in range(-200, 200, res):
			ray = pygame.Vector3((x*ratio, y*ratio, 1000))
			ray = rotated_x(ray, x_a+math.cos(z/5)/100)
			ray = rotated_y(ray, y_a+math.cos(z/5)/100)
			rd = (c_pos + ray).normalize()
			bright = rd.dot(sun.normalize())
			if bright > 0:
				bright = bright*4
				bright = min(1, bright)
				pygame.draw.rect(sc, [bright*100, bright*125, bright*255], [x_d+x, y_d+y, res, res])

			dist = pygame.Vector2(plaIntersect(c_pos, rd, pygame.Vector3((0, -100, 0)).normalize()))
			if dist.y > 0:
				ray_point = c_pos + rd * dist.x

				sd = (ray_point + (sun)).normalize()
				
				is_inter = intersect(ray_point, sd, point, 10)
				color = -sd.dot(sun.normalize())
				if is_inter.x < 0:
					color = sun.normalize().dot(pygame.Vector3((0, -1, 0)))
					
				pygame.draw.rect(sc, [max(color, 0.05)*255]*3, [x_d+x, y_d+y, res, res])
			
			dist = intersect(c_pos, rd, point, 10)
			if dist.x > 0:
				ray_point = c_pos + rd * dist.x
				normal = ray_point - point 
				if ray_point.y < 0 and c_pos.y <= 0:
					color = sun.normalize().dot(ray_point.normalize())
					if color < 0:
						color = 0
					
					pygame.draw.rect(sc, [color*255, color*100, color*10], [x_d+x, y_d+y, res, res])



res = 10
z = 0
while True:
	sc.fill((0, 0, 0))
	# sun = rotated_x(sun, 0.05)
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()
		
	raycast()



	keys = pygame.key.get_pressed()

	if keys[pygame.K_UP]:
		x_a -= 0.1
	if keys[pygame.K_DOWN]:
		x_a += 0.1
	if keys[pygame.K_LEFT]:
		y_a -= 0.1
	if keys[pygame.K_RIGHT]:
		y_a += 0.1
	if keys[pygame.K_a]:
		c_pos.x -= 10/res
	if keys[pygame.K_d]:
		c_pos.x += 10/res
	if keys[pygame.K_w]:
		c_pos.z += 10/res
	if keys[pygame.K_s]:
		c_pos.z -= 10/res
	if keys[pygame.K_LSHIFT]:
		c_pos.y -= 1
	if keys[pygame.K_LCTRL]:
		c_pos.y += 1
	if keys[pygame.K_1]:
		res = 1
	if keys[pygame.K_2]:
		res = 10

	pygame.display.update()
	