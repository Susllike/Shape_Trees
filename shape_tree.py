#!/usr/bin/python3

"""
Shape Trees
# By: Susllike
# October 2022
"""

import pygame
import math

pygame.init()

screen_width = 1000
screen_height = 1000
screen_center = (screen_width / 2, screen_height / 2)

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shape Trees")

# Clock
clock = pygame.time.Clock()

change_sides = True
rotate = False
# 1 for consistent change speed, 30 as base
clock_speed = 30

# Settings
start_sides = 5 # Sides for the starting polygon
start_small_radius = 100 # Size of the starting polygon
start_big_radius = 200 # Size of the "orbit" of smaller shapes
shift_angle = 0 # "Spin" of the shape
shift = 1
time_delta = 0

# Shape definition
def shape(sides, radius, center, angle):
	"""
	Definte the points of a polygon and its sides' midpoints.

	Technically this doesn't have to be done every loop
	since the shapes' points don't change over time.
	It works fine regardless, but might be a potential
	point for optimization.
	"""
	angles = [(360/sides)*i + angle for i in range(sides)]

	polygon_points = [
			(
				int(radius * math.cos(math.radians(angle))
					+ center[0]),
				int(radius * math.sin(math.radians(angle))
					+ center[1]),
			)

		for angle in angles
	]

	# Midpoints of each polygon side
	side_points = []
	for i in range(len(polygon_points) - 1):
		side_points.append(
			(
				(polygon_points[i][0] + polygon_points[i+1][0])/2, 
				(polygon_points[i][1] + polygon_points[i+1][1])/2
			)
		)
	
	# Using negative index "hack" to get the 
	# last tuple between last and first point
	side_points.append(
		(
			(polygon_points[-1][0] + polygon_points[0][0])/2, 
			(polygon_points[-1][1] + polygon_points[0][1])/2
		)
	)

	return angles, polygon_points, side_points

def draw_polygon_and_points(shape_points):
	"""Draw the polygon given its points."""

	# "Fill" the interior so the lines aren't shown inside
	# Only do that for actual polygons, not the line segments
	if len(shape_points) > 2:
		pygame.draw.polygon(
			screen, 
			(0, 0, 0), 
			shape_points,
		)

	pygame.draw.polygon(
		screen, 
		(255, 255, 255), 
		shape_points, 
		width = 1
	)

def make_tree(sides, s_radius, b_radius, center, rotation_angle, reduction_factor):
	"""Draw the tree recursively."""

	(angles, 
	 small_shape_points, 
	 small_side_points) = shape(sides, s_radius, center, rotation_angle)

	(_, 
	 big_shape_points, 
	 big_side_points) = shape(sides, b_radius, center, rotation_angle)

	# Draw the visible shape
	draw_polygon_and_points(small_shape_points)

	if sides > 2:
		for i in range(sides):
			# Draw a line from each midpoint of the shape the the outer "orbit"
			pygame.draw.line(
				screen,
				(255, 255, 255),
				small_side_points[i],
				big_side_points[i],
			)

			rotation_offset = 180 + angles[i] + (360 / sides) / 2

			# For the very end line segments to show up
			if sides == 3: rotation_offset += 90

			# Repeat the process on each point in the "orbit"
			make_tree(
				sides - 1, 
				s_radius / reduction_factor, 
				b_radius / reduction_factor, 
				big_side_points[i], 
				rotation_offset, 
				reduction_factor
			)

# Main loop
while True:
	screen.fill((0, 0, 0)) # Background color
	
	# Event check
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				pygame.quit()
				exit()

	# The meat - drawing the actual tree
	make_tree(
		start_sides, 
		start_small_radius, 
		start_big_radius, 
		screen_center, 
		shift_angle, 
		3 # 3 seems the best reduction-speed-wise.
	)

	# Make the shape rotate over time
	if rotate:
		shift_angle = shift_angle % 360 + 1
	
	# Change the number of sides of the starting polygon
	# Affects the rest of the tree
	if change_sides:
		cur_time = pygame.time.get_ticks()
		if abs(time_delta - cur_time) > 1000:
			time_delta = cur_time # might be a problem given enough time.
			start_sides += shift
			if start_sides >= 7 or start_sides <= 3:
				shift *= -1

	# Update everything
	pygame.display.update()
	clock.tick(clock_speed)