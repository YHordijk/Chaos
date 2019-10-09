import pkg.funcs as fn 

ant = fn.Ant()

ant.start(iterations=15000000, rule='LR', FPS=60, draw_every_frame=False)