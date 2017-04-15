import math

# координаты точки
class Coordinate:

	def __init__(self, x, y):
		self.x, self.y = x, y

# касательная
class Tangent:

	def __init__(self, incline, start, end):
		self.incline = incline
		self.start = start
		self.end = end
		# все точки касательной
		self.coordinates = self.get_coordinates()

	# точки касательной
	def get_coordinates(self, step = 1):
		# все точки
		points = list()
		# отрицательный наклон касательной
		if self.incline == -1:
			for point in range(self.start, self.end, step):
				coordinate = Coordinate(point, (point - self.start) / (self.end - self.start))
				points.append(coordinate)
		# положительный наклон касательной
		if self.incline == 1:
			for point in range(self.start, self.end, step):
				coordinate = Coordinate(point, (self.end - point) / (self.end - self.start))
				points.append(coordinate)
		# касательная параллельна оси Х
		if self.incline == 0:
			for point in range(self.start, self.end, step):
				coordinate = Coordinate(point, 1)
				points.append(coordinate)

		return points


# фигура(множество), состоящая из касательных
class Figure:

	def __init__(self, name, tangents = []):
		self.tangents = tangents
		self.name = name

	# придаем фигуре форму незаконченой слева трапеции
	def create_form_middle_down(self, b, c, d):
		middle = Tangent(0, b, c)
		down = Tangent(-1, c, d)

		self.tangents = [middle, down]

	# придаем фигуре форму незаконченой справа трапеции
	def create_form_middle_up(self, a, b, c):
		up = Tangent(1, a, b)
		middle = Tangent(0, b, c)

		self.tangents = [up, middle]

	# придаем фигуре форму треугольника
	def create_form_up_down(self, a, b, c):
		up = Tangent(1, a, b)
		down = Tangent(-1, b, c)

		self.tangents = [up, down]

	def create_form_up_middle_down(self, a, b, c, d):
		up = Tangent(1, a, b)
		middle = Tangent(0, b, c)
		down = Tangent(-1, c, d)

		self.tangents = [up, middle, down]




# действия с нечеткими множествами
class Machine:

	def __init__(self):
		self.figures = list()

		figures = self.__create_figures()

	def __create_figures(self):
		cold = Figure('холодная')

		some_cold = Figure('прохладная')

		warm = Figure('теплая')

		some_wart = Figure('не очень горячая')
		
		hot = Figure('горячая')

	# по температуре воды определяет какая вода
	def sensor_water(self, temperature):

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

	# по весу белья определяет количество белья
	def sensor_weight(self, weight):

		result = dict()

		if weight <= 1:
			result['мало'] = 1 if weight <= 1 else (1 - weight) / (1 - 0)

		if weight >= 0.5 and weight <= 3:
			result['немного'] = (weight - 0.5) / (1.25 - 0.5) if weight <= 1.25 else (3 - weight) / (3 - 1.25)

		if weight >= 2.5:
			result['много'] = (weight - 2.5) / (4 - 2.5) if weight <= 4 else 1

		return result

	# правило продукций для температуры воды
	def controller_water(self, feature):
		actions = list()

		if 'холодная' in feature:
			actions.append('расход жидкости большой')

		if 'прохладная' in feature:
			actions.append('расход жидкости небольшой')

		if 'теплая' in feature or 'не очень горячая' in feature:
			actions.append('расход жидкости средний')

		if 'горячая' in feature:
			actions.append('расход жидкости большой')

		return actions

	# правило продукций для количество белья
	def controller_weight(self, feature):
		actions = list()

		if 'мало' in feature:
			actions.append('уровень жидкости малый')

		if 'немного' in feature:
			actions.append('уровень жидкости средний')

		if 'много' in feature:
			actions.append('уровень жидкости большой')

		return actions

	# степень истинности условий 
	def rules(self, feature_water, feature_weight):
		# с определением по Заде 
		return min(feature_water, feature_weight)



	# запуск стиральной машинки
	def start(self, temperature, weight):
		# получаем все mu температуры воды
		feature_water = self.sensor_water(temperature)
		# получаем все mu веса белья
		feature_weight = self.sensor_weight(weight)

		# применяем правила продукций для воды
		degrees_truth_water = list()
		# получаем степени истинности
		degrees_truth_water = self.controller_water(feature_water)

		# применяем правила продукций для белья
		degrees_truth_weight = list()
		# получаем степени истинности
		degrees_truth_weight = self.controller_weight(feature_weight)





if __name__ == '__main__':
	washine = Machine()

	tangents = [Tangent(-1, 15, 25), 
				Tangent(1, 5, 15)]

	washine.add_figure(tangents)

	figure = Figure('уменьшить', tangents)
	washine.start(55, 3)

	#(figure.tangents[0].coordinates)
