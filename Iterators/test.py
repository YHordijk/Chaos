import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os



def test():
	for i in range(100):
		if i%10 == 0:
			print(i)
			yield i
	return True


a = test()
for progress in a: pass