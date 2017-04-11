import math

def get_points(start, end, step, incline):
	points = list()

	if incline == -1:
		for point in range(start, end, step):
			points.append((point - start) / (end - start))

	if incline == 1:
		for point in range(start, end, step):
			points.append((end - point) / (end - start))

	if incline == 0:
		for point in range(start, end, step):
			points.append(1)

	return points

# получаем mu
def sensor(temperature):

	result = dict()

	if temperature <= 30:
		result['холодная'] = 1 if temperature <= 10 else (30 - temperature) / (30 - 10)

	if temperature >= 20 and temperature <= 50:
		result['прохладная'] = (temperature - 20) / (35 - 20) if temperature <= 35 else (50 - temperature) / (50 - 35)

	if temperature >= 40 and temperature <= 60:
		result['теплая'] = (temperature - 40) / (50 - 40) if temperature <= 50 else (60 - temperature) / (60 - 50)

	if temperature >= 50 and temperature <= 70:
		result['не очень горячая'] = (temperature - 50) / (60 - 50) if temperature <= 60 else (70 - temperature) / (70 - 60)

	if temperature >= 60:
		result['горячая'] = (temperature - 60) / (70 - 60) if temperature <= 70 else 1

	return result

# правила нечетких продукций(вывод)
def controller(water):

	action = list()

	if 'горячая' in water:
		action.append("намного уменьшить")

	if 'не очень горячая' in water:
		action.append("уменьшить")

	if 'теплая' in water:
		action.append("оставить")

	if 'прохладная' in water:
		action.append("увеличить")

	if 'холодная' in water:
		action.append("намного увеличить")

	return action


def max_disjunction(set_mu, max_mu):

	set_mu = [mu for mu in set_mu if mu <= max_mu]

	return max(set_mu)

# входные параметры(лингвистическая переменная): 
# температура воды
def start(temperature):
	# получаем mu
	set_temprature = sensor(temperature)
	# получаем нужные правила нечетких продукций
	# используются в текущем процессе нечеткого вывода
	action = controller([key for key in set_temprature.keys()])

	# отсекаем 0
	# блок агрегирования 
	# (вычисление степени истинности условий по каждому правилу продукций)
	set_temprature = [mu for mu in set_temprature.values() if mu > 0]

	# блок активизации (вычисление степени истинности каждого из подзаключений правил продукции и построение функции принадлежности каждого из подзаключений для рассматриваемых выходных лингвистических переменных)
	mu = min(set_temprature)
	
	set_mu = list()
	borders = list()

	# получаем точки нужных правил продукций
	if 'намного уменьшить' in action:
		set_mu.extend(get_points(30, 40, 2, 0))
		set_mu.extend(get_points(20, 30, 2, 1))
		# запоминаем граицы продукций
		borders.extend([20, 40])

	if 'уменьшить' in action:
		set_mu.extend(get_points(5, 15, 2, 1))
		set_mu.extend(get_points(15, 25, 2, -1))
		# запоминаем граицы продукций
		borders.extend([5, 25])

	if 'оставить' in action:
		set_mu.extend(get_points(-15, 0, 2, 1))
		set_mu.extend(get_points(0, 15, 2, -1))
		# запоминаем граицы продукций
		borders.extend([-15, 15])

	if 'увеличить' in action:
		set_mu.extend(get_points(-25, -15, 2, 1))
		set_mu.extend(get_points(-15, -5, 2, 0))
		# запоминаем граицы продукций
		borders.extend([-25, -5])

	if 'намного увеличить' in action:
		set_mu.extend(get_points(-30, -20, 2, -1))
		set_mu.extend(get_points(-40, -30, 2, 0))
		# запоминаем граицы продукций
		borders.extend([-40, -20])

	# блок аккумуляции 
	# (вычисление функции принадлежности для каждой из лингвистических переменных)
	mu = max_disjunction(set_mu, mu)
	# выбираем граицы продукций
	border_min = min(borders)
	border_max = max(borders)

	# блок дефаззификации (нахождение обычного (не нечеткого)
	# значения выходной переменной(ых))
	
	# находим точку
	# метод взвешенной точки
	x0 = (1/6) * border_min + (4/6) * (mu + mu)/2 + (1/6) * border_max

	return -1 * math.ceil(x0)


# используем алгоритм Мамдани
	
# в качестве входной 
# лингвистической переменной следует использовать температуру воды

# в качестве выходной лингвистической переменной 
# будем использовать угол поворота регулятора горячей воды
if __name__ == '__main__':
	# вода
	result = start(55)

	if result >= 0:
		print("Повернуть регулятор температуры на {0}* вправо".format(result))
	else:
		print("Повернуть регулятор температуры на {0}* влево".format(-1*result))

