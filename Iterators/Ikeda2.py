import mypackage.rule as rule
import mypackage.drawer as draw
import random
from datetime import datetime
import math

rangex = (-10, 10)
rangey = (-10, 10)
screen = draw.Screen((1600, 900), rangex, rangey, draw_opacity_steps=15)
rule = rule.Ikeda()
# rule.u = int(1000*(0.5*random.random()+0.5))/1000
# rule.u = 1.001

# iters = 100
# steps = 500
# for i in range(iters):
# 	# start_pos = (20*random.random()-10, 20*random.random()-10)
# 	start_pos = (random.randrange(rangex[0]*100,rangex[1]*100)/100, random.randrange(rangey[0]*100,rangey[1]*100)/100)
# 	pos = rule.iterate(start_pos, steps)
# 	screen.draw_pixels(pos[:-50])
# 	if i%int(iters/100)==0:
# 		print(f'Current progress: {int(100*i/iters)}%', end="\r")
# # screen.show()
# print(f"C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\Iterators\\ikeda frames\\{iters}_{steps}_{int(rule.u*10000)}.png")
# screen.save(f"C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\Iterators\\ikeda frames\\{iters}_{steps}_{int(rule.u*10000)}.png")



iters = 5000
steps = 500
u_range = range(1040,1080,1)
# u_range = [1002, 1004, 1006]
max_iters = iters * len(u_range)

for j, k in enumerate(u_range):
	rule.u = round(k/1000,3)

	screen.clear()

	for i in range(iters):
		if i%math.ceil(iters/100)==1:
			start = datetime.now()

		start_pos = (random.randrange(rangex[0]*100,rangex[1]*100)/100, random.randrange(rangey[0]*100,rangey[1]*100)/100)
		pos = rule.iterate(start_pos, steps)
		screen.draw_pixels(pos[:-50])
		
		if i%math.ceil(iters/100)==1:
			curr_iter = i + j*iters
			delta_time = datetime.now() - start
			average_time = delta_time.microseconds/60/1000000
			print(f'Generating Ikeda map with u={rule.u}. Current progress: {round(curr_iter/max_iters*100, 1)}%. Estimated time remaining: {int((max_iters - curr_iter) * average_time)} minutes.', end="\r")

	# print(round(rule.u*1000), rule.u*1000, f"C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\Iterators\\ikeda frames\\test\\{iters}_{steps}_{round(rule.u*1000)}.png")
	screen.save(f"C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\Iterators\\ikeda frames\\test\\{iters}_{steps}_{round(rule.u*1000)}.png")

print('Finished.')