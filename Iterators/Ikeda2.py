import mypackage.rule as rule
import mypackage.drawer as draw
import random

rangex = (-10, 10)
rangey = (-10, 10)
screen = draw.Screen((1600, 900), rangex, rangey, draw_opacity_steps=15)
rule = rule.Ikeda()
rule.u = 0.6

iters = 5000
steps = 500
for i in range(iters):
	# start_pos = (20*random.random()-10, 20*random.random()-10)
	start_pos = (random.randrange(rangex[0]*100,rangex[1]*100)/100, random.randrange(rangey[0]*100,rangey[1]*100)/100)
	pos = rule.iterate(start_pos, steps)
	screen.draw_pixels(pos)
	if i%int(iters/100)==0:
		print(f'Current progress: {int(100*i/iters)}%', end="\r")
screen.show()
screen.save(f"C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\ikeda frames\\{iters}_{steps}_{rule.u*1000}_{rangex[0]}_{rangex[1]}_{rangey[0]}_{rangey[1]}.png")





# screen = draw.Screen((1600, 900), (-2, 7), (-6, 6), draw_opacity_steps=5)
# rule = rule.Ikeda()

# iters = 200
# for j in range(600, 1150, 5):
# 	u = j/1000
# 	for i in range(iters):
# 		start_pos = (20*random.random()-10, 20*random.random()-10)
# 		pos = rule.iterate(start_pos, 200)
# 		screen.draw_pixels(pos)
# 		if i%int(iters/100)==0:
# 			print(f'Current progress: {int(100*i/iters)}%', end="\r")

# 	screen.save(pygame.image.save(disp, "C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\ikeda frames\\hires2-{}.png".format(k)))