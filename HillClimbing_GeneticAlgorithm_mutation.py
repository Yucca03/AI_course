import csv
import math
import random

Population_Size = [50, 100, 500, 1000] # Population Size (Initial Population)
Generation_Number = [100, 1000, 10000] # Generation Number

# upper bound and lower bound of x1 and x2
x1_upper, x1_lower = 12.1, -3.0 
x2_upper, x2_lower = 5.8, 4.1

def get_objective_function_output(x1, x2):
	# Objective Function f(x1, x2) Here
	objective_function = round(21.5+x1*round(math.sin(4*math.pi*x1),6)+x2*round(math.sin(20*math.pi*x2),6),6)
	return objective_function

# def get_boundary_distance(x1, x2):
# 	a = (x1_upper, x2_upper)
# 	b = (x1_upper, x2_lower)
# 	c = (x1_lower, x2_upper)
# 	d = (x1_lower, x2_lower)
# 	temp_list = [a, b, c, d]
# 	maximum_distance = 0
# 	for point in temp_list:
# 		distance = math.sqrt(math.pow(point[0]-x1,2)+math.pow(point[1]-x2,2))
# 		if distance > maximum_distance:
# 			maximum_distance = distance
# 	return maximum_distance

# # Geometric Function for radius improving
# def Geometric_Function(x1, x2):
# 	r = 0.75
# 	Sn = get_boundary_distance(x1, x2)

# 	# Get variable a/(1-r) = Sn
# 	leading_element = Sn * (1 - r)
# 	# print(leading_element)
	
# 	# while True:

# Hill Climbing method
def Hill_Climbing(x1, x2):
	result = get_objective_function_output(x1, x2)
	# print('x1 is ' + str(x1) + ', x2 is ' + str(x2) + '  ', end = '')
	# print('The objective function is ' + str(result))
	
	# Circle_Function: (x - h)^2 + (y - k)^2 = r^2
	r = 0.001
	next_step = (x1, x2)
	next_value = result
	for angle in range(0, 360, 1):
		x = round(r * round(math.cos(round(angle/180,6)*math.pi),6) + x1, 6)
		y = round(r * round(math.sin(round(angle/180,6)*math.pi),6) + x2, 6)
		
		# To promise that the point is not out of bound.
		if x > x1_upper or x < x1_lower or x2 > x2_upper or x2 < x2_lower:
			continue

		temp_value = get_objective_function_output(x, y)
		if next_value < temp_value:
			next_value = temp_value
			next_step = (x, y)

	# Recursion of hill climbing
	if next_value == result:
		return (x1, x2, result)
	else:
		return Hill_Climbing(next_step[0], next_step[1])

# Simulated Annealing method
def Simulated_Annealing(x1, x2):
	# Section 1 - Hill Climbing
	hc_x, hc_y, hc_final_result = Hill_Climbing(x1, x2)

	# Section 2 - Simulated Annealing
	change_step = (x1, x2)
	change_value = hc_final_result

	distance_list = list()
	distance = 0.001
	while distance < 0.1:
		distance_list.append(round(distance,6))
		distance += 0.001

	# Change radius to imporove the result
	for radius in distance_list:
		for angle in range(0, 360, 1):
			x = round(radius * round(math.cos(round(angle/180,6)*math.pi),6) + hc_x, 6)
			y = round(radius * round(math.sin(round(angle/180,6)*math.pi),6) + hc_y, 6)	
		
			# To promise that the point is not out of bound.
			if x > x1_upper or x < x1_lower or x2 > x2_upper or x2 < x2_lower:
				continue

			temp_value = get_objective_function_output(x, y)
			if change_value < temp_value:
				change_value = temp_value
				change_step = (x, y)

	# Recursion of simulated annealing
	if hc_final_result == change_value:
		return (x1, x2, change_value)
	else:
		return Simulated_Annealing(change_step[0], change_step[1])

def generate_population(Population_Size):
	Chromosome_set = list()
	sum_of_fitness = 0
	for i in range(0, Population_Size, 1):
		x1 = round(random.uniform(x1_lower, x1_upper), 6)
		x2 = round(random.uniform(x2_lower, x2_upper), 6)
		y = get_objective_function_output(x1, x2)
		sum_of_fitness += y
		Chromosome_set.append((x1, x2, y, sum_of_fitness))
	return Chromosome_set, sum_of_fitness

def reproduction(Chromosome_set, sum_of_fitness):
	New_Chromosome_set = list()
	new_sum_of_fitness = 0
	for num in range(0, len(Chromosome_set), 1):
		new_weight = random.uniform(0, sum_of_fitness)
		for Chromosome in Chromosome_set:
			if new_weight < Chromosome[3]:
				new_sum_of_fitness += Chromosome[2]
				New_Chromosome_set.append((Chromosome[0], Chromosome[1], Chromosome[2], new_sum_of_fitness))
				break
	return New_Chromosome_set, new_sum_of_fitness

def switch(strA, strB, target):
	item_a = strA[target]
	item_b = strB[target]
	strA = strA[:target] + strA[target].replace(item_a,item_b) + strA[target+1:]
	strB = strB[:target] + strB[target].replace(item_b,item_a) + strB[target+1:]
	return (strA, strB)

def string_to_float(input_string):
	output_flaot = ''
	flag = 0
	for s in input_string:
		if flag == 0 and s == '0':
			continue
		elif flag == 0 and s != '0':
			output_flaot += s
			flag = 1
		else:
			output_flaot += s
	return float(output_flaot)

def crossover(Chromosome_set):
	# print("{:.6f}".format(x1_upper))
	# print("{:0>3d}".format(int(x1_upper)))
	Mating_Pool = list()
	for item in Chromosome_set:
		# format: 9 digits and 6 digits after dot
		Mating_Pool.append((str('{:09.6f}'.format(item[0])),str('{:09.6f}'.format(item[1]))))
	
	Child_Chromosome_set = list()
	while len(Child_Chromosome_set) < 100:
		variable = random.randint(0,1)
		A_id = random.randint(0,len(Mating_Pool)-1)
		B_id = random.randint(0,len(Mating_Pool)-1)
		parent_A = Mating_Pool[A_id][variable]
		parent_B = Mating_Pool[B_id][variable]
		crossover_point = random.randint(0,len(parent_A)-1)
		child_a, child_b = switch(parent_A, parent_B, crossover_point)

		p_a = string_to_float(parent_A)
		p_b = string_to_float(parent_B)
		c_a = string_to_float(child_a)
		c_b = string_to_float(child_b)

		if variable == 0:
			if c_a > x1_upper or c_a < x1_lower or c_b > x1_upper or c_b < x1_lower:
				Child_Chromosome_set.append((p_a, string_to_float(Mating_Pool[A_id][1])))
				Child_Chromosome_set.append((p_a, string_to_float(Mating_Pool[B_id][1])))
			else:
				Child_Chromosome_set.append((c_a, string_to_float(Mating_Pool[A_id][1])))
				Child_Chromosome_set.append((c_b, string_to_float(Mating_Pool[B_id][1])))
		elif variable == 1:
			if c_a > x2_upper or c_a < x2_lower or c_b > x2_upper or c_b < x2_lower:
				Child_Chromosome_set.append((string_to_float(Mating_Pool[A_id][0]), p_a))
				Child_Chromosome_set.append((string_to_float(Mating_Pool[B_id][0]), p_b))
			else:
				Child_Chromosome_set.append((string_to_float(Mating_Pool[A_id][0]), c_a))
				Child_Chromosome_set.append((string_to_float(Mating_Pool[B_id][0]), c_b))
	return Child_Chromosome_set

def mutation(Child_Chromosome_set, probability):
	Chromosome_set = list()
	for Chromosome in Child_Chromosome_set:
		if random.uniform(0, 1)	< probability:
			variable = random.randint(0,1)

			origin = str('{:09.6f}'.format(Chromosome[variable]))
			length = len(origin)

			counter = 0
			while True:
				target = random.randint(0,length-1)
				number = random.randint(0,9)
				result = origin[:target] + origin[target].replace(origin[target],str(number)) + origin[target+1:]
				output = string_to_float(result)
				if variable == 0:
					if output < x1_upper and output > x1_lower:
						Chromosome_set.append((output, Chromosome[1]))
						break
				elif variable == 1:
					if output < x2_upper and output > x2_lower:
						Chromosome_set.append((Chromosome[0], output))
						break
				counter += 1
		else:
			Chromosome_set.append(Chromosome)

	next_Chromosome_set = list()
	sum_of_fitness = 0
	for i in range(0, len(Chromosome_set), 1):
		x1 = round(Chromosome_set[i][0],6)
		x2 = round(Chromosome_set[i][1],6)
		y = get_objective_function_output(x1, x2)
		sum_of_fitness += y
		next_Chromosome_set.append((x1, x2, y, sum_of_fitness))

	return (next_Chromosome_set, sum_of_fitness)

def get_best_Chromosome(Chromosome_set):
	temp_x1, temp_x2, temp_fitness = 0, 0, 0
	for item in Chromosome_set:
		if item[2] > temp_fitness:
			temp_fitness = item[2]
			temp_x1 = item[0]
			temp_x2 = item[1]
	return (temp_x1, temp_x2, temp_fitness)

def Genetic_Algorithm(Population_Size, Generation_Number):
	Chromosome_set, sum_of_fitness = generate_population(Population_Size)
	mutation_probability = 0.001
	best_fitness, best_x1, best_x2 = 0, 0, 0
	i = 1
	with open('GA_P' + str(Population_Size) + '_G' + str(Generation_Number) + '.csv', 'w') as csvfile:
		fieldnames = ['Generation', 'x1', 'x2', 'fitness', 'best_x1', 'best_x2', 'best_fitness','avg_fitness']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		fitness_sum = 0
		# Loop start
		while i <= Generation_Number:
			result_after_reproduction, sum_of_fitness = reproduction(Chromosome_set, sum_of_fitness)
			result_after_crossover = crossover(result_after_reproduction)
			result_after_mutation, sum_of_fitness = mutation(result_after_crossover, mutation_probability)
			Chromosome_set = result_after_mutation
			x1, x2, fitness = get_best_Chromosome(Chromosome_set)
			if best_fitness < fitness:
				best_fitness = fitness
				best_x1 = x1
				best_x2 = x2
			fitness_sum += fitness
			# print('Generation ' + str(i) + ' : x1 = ' + str(x1) + ' x2 = ' + str(x2) + ' fitness = ' + str(fitness))
			# print('Best-so-far : ' + str(best_fitness))
			writer.writerow({'Generation': i, 'x1': x1, 'x2': x2, 'fitness':fitness, 'best_x1':fitness, 'best_x1':best_x1, 'best_x2':best_x2, 'best_fitness':best_fitness, 'avg_fitness':round((fitness_sum/i),6)})
			i += 1
		# Loop end
	return (best_x1, best_x2, best_fitness)

def main():
	# Result comparison for three optimization methods
	# with open('Comparison_HC_SA_GA(P=1000,G=100).csv', 'w') as csvfile:
	# 	fieldnames = ['Iteration', 'Hill_Climbing', 'Simulated_Annealing', 'Genetic_Algorithm(P=1000,G=100)']
	# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	# 	writer.writeheader()
	# 	for i in range(1, 101, 1):
	# 		# Range: -3.0 ≦ x1 ≦ 12.1 and 4.1 ≦ x2 ≦ 5.8
	# 		x1, x2 = round(random.uniform(x1_lower, x1_upper), 6), round(random.uniform(x2_lower, x2_upper), 6)
	# 		print('Start: x1 is ' + str(x1) + ', x2 is ' + str(x2))
	# 		print('-----')
	# 		# Hill Climbing method
	# 		hc_x, hc_y, hc_final_result = Hill_Climbing(x1, x2)
	# 		print('The final result of Hill Climbing is \nx1 = ' + str(hc_x) + ', x2 = ' + str(hc_y) + '\nf(x1, x2) is ' + str(hc_final_result))
	# 		print('-----')
	# 		# Simulated Annealing method
	# 		sa_x, sa_y, sa_final_result = Simulated_Annealing(x1, x2)
	# 		print('The final result of Simulated Annealing is \nx1 = ' + str(sa_x) + ', x2 = ' + str(sa_y) + '\nf(x1, x2) is ' + str(sa_final_result))
	# 		print('-----')
	# 		# Genetic Algorithm method
	# 		ga_x, ga_y, ga_final_result = Genetic_Algorithm(1000, 100)
	# 		print('The final result of Genetic Algorithm is \nx1 = ' + str(ga_x) + ', x2 = ' + str(ga_y) + '\nf(x1, x2) is ' + str(ga_final_result))
	# 		print('-----')
	# 		writer.writerow({'Iteration': i, 'Hill_Climbing': hc_final_result, 'Simulated_Annealing': sa_final_result, 'Genetic_Algorithm(P=1000,G=100)':ga_final_result})
	# 		print()

	# Genetic Algorithm method
	for Population in Population_Size:
		for Generation in Generation_Number:
			ga_x, ga_y, ga_final_result = Genetic_Algorithm(Population, Generation)
			print('The result of Genetic Algorithm (P = ' + str(Population) + ' ,G = ' + str(Generation) + ') is \nx1 = ' + str(ga_x) + ', x2 = ' + str(ga_y) + '\nf(x1, x2) is ' + str(ga_final_result))
	
	# # Comparison
	# if hc_final_result < sa_final_result:
	# 	print('Simulated Annealing method is better than Hill Climbing method.')
	# else:
	# 	print('Hill Climbing method is better than Simulated Annealing method.')

if __name__=="__main__":
	main()
