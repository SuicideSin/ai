#Aidan San
#muakasan@gmail.com
#https://github.com/Muakasan/Functional-Programming

from itertools import *

def myMap(f, l):
	#return [f(i) for i in l]
	return reduce(lambda a, x: a + [f(x)], l, [])

def myFilter(f, l):
	#return [i for i in l if f(i)]
	#return reduce(lambda a, x: a + [x] if f(x) else a, l, [])
	return reduce(lambda a, x: a + ([x] if f(x) else []), l, [])

def isPrime(n):
	return n!=1 and reduce(lambda a, x: a and x, map(lambda x: n%x != 0, range(2, n)), True)

def main():
	l = [60, 36, 20, 8, 43, 75, 15, 42, 87, 48, 68, 4, 82, 41, 44]

	print("The list where each element is multiplied by 2:")
	print(map(lambda x: 2*x, l))
	
	print("The list where each element has 1 added to it:")
	print(map(lambda x:x+1, l))

	print("The list with only elements greater than 40:")
	print(filter(lambda x: x > 40, l))
	
	print("The list with only even elements:")
	print(filter(lambda x: x%2 == 0, l))
	
	print("The sum of the list:")
	print(reduce(lambda a, x: a + x, l))
	
	print("The max of the list:")
	print(reduce(lambda a, x: x if x > a else a, l))

	print("The list where each element is multiplied by 2 using YOUR map:")
	print(myMap(lambda x: 2*x, l))

	print("The list with only elements greater than 40 using YOUR filter:")
	print(myFilter(lambda x: x > 40, l))

	print("The first 20 prime numbers:")
	print(list(islice(ifilter(isPrime, count(1)), 100)))

if __name__ == "__main__":
	main()	