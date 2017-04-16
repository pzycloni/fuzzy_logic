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

	def get_coordinate(self, x):
		if x < self.start or x > self.end:
			return False

		if self.incline == -1:
			return Coordinate(x, (self.end - x) / (self.end - self.start))

		if self.incline == 0:
			return Coordinate(x, 1)

		if self.incline == 1:
			return Coordinate(x, (x - self.start) / (self.end - self.start))

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

		self.start, self.end = 0, 0


	def __set_borders(self):
		borders = list()

		for tangent in self.tangents:
			borders.append(tangent.start)
			borders.append(tangent.end)

		self.start, self.end = min(borders), max(borders)


	# придаем фигуре форму незаконченой слева трапеции
	def create_form_middle_down(self, a, b, c):
		middle = Tangent(0, a, b)
		down = Tangent(-1, b, c)

		self.tangents = [middle, down]
		self.__set_borders()


	# придаем фигуре форму незаконченой справа трапеции
	def create_form_middle_up(self, a, b, c):
		up = Tangent(1, a, b)
		middle = Tangent(0, b, c)

		self.tangents = [up, middle]
		self.__set_borders()

	# придаем фигуре форму треугольника
	def create_form_up_down(self, a, b, c):
		up = Tangent(1, a, b)
		down = Tangent(-1, b, c)

		self.tangents = [up, down]
		self.__set_borders()

	def create_form_up_middle_down(self, a, b, c, d):
		up = Tangent(1, a, b)
		middle = Tangent(0, b, c)
		down = Tangent(-1, c, d)

		self.tangents = [up, middle, down]
		self.__set_borders()




# действия с нечеткими множествами
class Machine:

	def __init__(self):
		self.water_figures = self.__create_water_figures()
		self.weight_figures = self.__create_weight_figures()

	# создание фигур(нечетких множеств) температуры воды
	def __create_water_figures(self):
		cold = Figure('холодная')
		cold.create_form_middle_down(0, 10, 30)

		some_cold = Figure('прохладная')
		some_cold.create_form_up_down(20, 35, 50)

		warm = Figure('теплая')
		warm.create_form_up_down(40, 50, 60)

		some_warm = Figure('не очень горячая')
		some_warm.create_form_up_down(50, 60, 70)

		hot = Figure('горячая')
		hot.create_form_middle_up(60, 70, 90)

		return [cold, some_cold, warm, some_warm, hot]

	# создание фигур(нечетких множеств) кол-ва белья
	def __create_weight_figures(self):
		few = Figure('мало')
		few.create_form_middle_down(0, 1, 2)

		some = Figure('немного')
		some.create_form_up_middle_down(1, 2, 3, 4)

		many = Figure('много')
		many.create_form_middle_up(3, 4, 5)

		return [few, some, many]



	# по температуре воды определяет какая вода
	def sensor_water(self, temperature):

		result = dict()

		for figure in self.water_figures:

			if figure.start <= temperature and figure.end >= temperature:
				for tangent in figure.tangents:

					if tangent.start <= temperature and tangent.end >= temperature:
						result[figure.name] = tangent.get_coordinate(temperature).y

		return result

	# по весу белья определяет количество белья
	def sensor_weight(self, weight):

		result = dict()

		for figure in self.weight_figures:

			if figure.start <= weight and figure.end >= weight:
				for tangent in figure.tangents:

					if tangent.start <= weight and tangent.end >= weight:
						result[figure.name] = tangent.get_coordinate(weight).y

		return result

	# правило продукций для температуры воды
	def controller_water(self, feature):
		actions = dict()

		if 'холодная' in feature:
			actions['расход жидкости большой'] = 1

		if 'прохладная' in feature:
			actions['расход жидкости небольшой'] = 0.5

		if 'теплая' in feature or 'не очень горячая' in feature:
			actions['расход жидкости средний'] = 0.25

		if 'горячая' in feature:
			actions['расход жидкости малый'] = 0

		return actions

	# правило продукций для количество белья
	def controller_weight(self, feature):
		actions = dict()

		if 'мало' in feature:
			actions['уровень жидкости малый'] = 0.75

		if 'немного' in feature:
			actions['уровень жидкости средний'] = 0.25

		if 'много' in feature:
			actions['уровень жидкости большой'] = 0

		return actions

	# агрегирование подусловий правил нечеткой продукции 
	def aggregation(self, features):
		field = min(features, key=lambda field: features[field])

		return {field: features[field]}


	# активизация подусловий правил нечеткой продукции 
	def activisation(self, features):
		field = min(features, key=lambda field: features[field])

		return {field: features[field]}

	# аккумуляция подзаключений правил нечеткой продукции
	def accumulation(self, features):
		field = max(features, key=lambda field: features[field])

		return {field: features[field]}


	# проверка введеных параметров
	def verification_params(self, temperature, weight):
		if temperature > 90 or temperature < 0:
			print('Недопустимая температура!')
			return False

		if weight > 5:
			print('Превышен лимит количества белья!')
			return False

		if weight <= 0:
			print('Машинка пуста!')
			return False

		return True


	# запуск стиральной машинки
	def start(self, temperature, weight):
		
		if not self.verification_params(temperature, weight):
			return False

		# получаем все mu температуры воды
		feature_water = self.sensor_water(temperature)
		# получаем все mu веса белья
		feature_weight = self.sensor_weight(weight)

		# активизация
		mu_feature_water = self.activisation(feature_water)
		mu_feature_weight = self.activisation(feature_weight)

		degrees_truth_water = dict()
		# получаем степени истинности
		degrees_truth_water = self.controller_water(feature_water)
		# активизация подзаключений правил нечеткой продукции
		mu_degrees_water = self.aggregation(degrees_truth_water)

		degrees_truth_weight = dict()
		# получаем степени истинности
		degrees_truth_weight = self.controller_weight(feature_weight)
		# активизация подзаключений правил нечеткой продукции
		mu_degrees_weight = self.aggregation(degrees_truth_weight)

		mu_water = dict()
		# добавляем в словарь, для того чтобы сравнить
		mu_water.update(mu_degrees_water)
		mu_water.update(mu_feature_water)
		# аккумуляция подзаключений правил нечеткой продукции
		result_mu_water = self.accumulation(mu_water)
		# добавляем в словарь, для того чтобы сравнить
		mu_weight = dict()
		mu_weight.update(mu_degrees_weight)
		mu_weight.update(mu_feature_weight)
		# аккумуляция подзаключений правил нечеткой продукции
		result_mu_weight = self.accumulation(mu_weight)





if __name__ == '__main__':
	washine = Machine()
	washine.start(55, 2)

	#(figure.tangents[0].coordinates)
