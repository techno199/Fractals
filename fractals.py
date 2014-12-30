import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

max_levels = 3                              # Максимальный уровень для спуска рекурсии
LABEL_TEXT = "Текущее число уровней : "     # Текст для интерфейса

SIZE = 3 ** 5 * 2                           # Размер холста

def gradient(first, last, alpha):
    """
    Вычисляет значение лежащее между first и last на относительном расстоянии alpha.
    """
    return int(first + alpha * (last - first))

def angle_to_vector(ang, length):
    """
    Преобразует угол в вектор заданой длины.
    :param ang: угол в радианах
    :param length: длина вектора
    """
    return [length * math.cos(ang), length * math.sin(ang)]

class Fractal:
    """
    Суперкласс для рисования фракталов
    """
    def __init__(self, first_color, last_color):
        """
        :param first_color: цвет компонентов первого уровня
        :param last_color: цвет компонентов последнего уровня
        """
        self._level = 0                     # текущий уровень рекурсии
        self._first_color = first_color
        self._last_color = last_color

    def current_color(self):
        """
        Возвращает цвет для компонентов текущего уровня рекурсии
        """
        a = [str(gradient(self._first_color[i],self._last_color[i], self._level/max_levels)) for i in range(3)]
        return "rgb("+a[0]+","+a[1]+","+a[2]+")"
    

    def recursive(self, canvas, position, length, angle):
        """
        Вычисляет текущий уровень рекурсии.
        На последнем уровне вызывает base(), на остальных - iteration().
        """
        self._level+=1
        if self._level <= max_levels:
            self.iteration(canvas, position, length, angle)
        else:
            self.base(canvas, position, length, angle)
        self._level-=1

    def draw(self, canvas):
        """
        Рисует фрактал
        """
        self._level=0
        self.start(canvas)

class CantorSet(Fractal):
    def __init__(self, first_color, last_color):
        Fractal.__init__(self, first_color, last_color)

    def start(self, canvas):
        """
        Запускает процесс построения фрактала
        :param canvas: холст для рисования
        """
        self.recursive(canvas, (0, SIZE / 3), SIZE, 0)

    def base(self, canvas, position, length, angle):
        """
        Рисует на холсте canvas базовый элемент фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        canvas.draw_line(position, (position[0] + length, position[1]), 5, self.current_color())

    def iteration(self, canvas, position, length, angle):
        """
        Cтроит на холсте canvas одну итерацию фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        self.base(canvas, position, length, angle)
        self.recursive(canvas, (position[0], position[1] + 10), length / 3, 0)
        self.recursive(canvas, (position[0] + 2 * length / 3, position[1] + 10), length / 3, 0)


class FractalTree(Fractal):
    def __init__(self, first_color, last_color):
        super().__init__(first_color, last_color)

    def start(self, canvas):
        """
        Запускает процесс построения фрактала
        :param canvas: холст для рисования
        """
        self.recursive(canvas, (SIZE//2, SIZE-1), SIZE//2, -math.pi/2)

    def base(self, canvas, position, length, angle):
        """
        Рисует на холсте canvas базовый элемент фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        atv = angle_to_vector(angle, length)
        canvas.draw_line(position, [position[0]+atv[0], position[1]+atv[1]], 5, self.current_color())

    def iteration(self, canvas, position, length, angle):
        """
        Cтроит на холсте canvas одну итерацию фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        atv = angle_to_vector(angle, length)
        pos_new = (position[0]+atv[0], position[1]+atv[1])
        self.base(canvas, position, length, angle)
        self.recursive(canvas, pos_new, length//2, angle+math.pi/4)
        self.recursive(canvas, pos_new, length//2, angle-math.pi/4)

class KochLine(Fractal):
    def __init__(self, first_color, last_color):
        super().__init__(first_color, last_color)

    def start(self, canvas):
        """
        Запускает процесс построения фрактала
        :param canvas: холст для рисования
        """
        self.recursive(canvas, (0,SIZE-10), SIZE, 0)

    def base(self, canvas, position, length, angle):
        """
        Рисует на холсте canvas базовый элемент фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        atv = angle_to_vector(angle, length
                              /3)
        canvas.draw_line(position, [position[0]+atv[0], position[1]+atv[1]], 2, self.current_color())
        new_pos = position[0]+atv[0]*2, position[1]+atv[1]*2
        canvas.draw_line(new_pos, (new_pos[0]+atv[0], new_pos[1]+atv[1]), 2, self.current_color())

    def iteration(self, canvas, position, length, angle):
        """
        Cтроит на холсте canvas одну итерацию фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        self.base(canvas, position, length, angle)
        atv = angle_to_vector(angle, length/3)
        pos_new1 = (position[0]+atv[0], position[1]+atv[1])
        atv = angle_to_vector(angle-math.pi/3, length/3)
        pos_new2 = (pos_new1[0]+atv[0], pos_new1[1]+atv[1])
        atv = angle_to_vector(angle, 2*length/3)
        pos_new3 = (position[0]+atv[0], position[1]+atv[1])
        self.recursive(canvas, pos_new1, length//3, angle-math.pi/3)
        self.recursive(canvas, pos_new2, length//3, angle+math.pi/3)
        self.recursive(canvas, pos_new3, length//3, angle)
        self.recursive(canvas, position, length//3, angle)
        


class KochSnowflake(KochLine):
    def __init__(self, first_color, last_color):
        super().__init__(first_color, last_color)
    def start(self, canvas):
        """
        Запускает процесс построения фрактала
        :param canvas: холст для рисования
        """
        temp = angle_to_vector(-math.pi/3, 2/3*SIZE)
        self.recursive(canvas, (5/6*SIZE, 5/6*SIZE), 2/3*SIZE, -math.pi)
        self.recursive(canvas, (1/6*SIZE, 5/6*SIZE), 2/3*SIZE, -math.pi/3)
        self.recursive(canvas, (1/6*SIZE+temp[0], 5/6*SIZE+temp[1]), 2/3*SIZE, math.pi/3)


class SerpinskyCarpet(Fractal):
    def __init__(self, first_color, last_color):
        super().__init__(first_color, last_color)

    def start(self, canvas):
        """
        Запускает процесс построения фрактала
        :param canvas: холст для рисования
        """
        self.recursive(canvas, (0,0), SIZE, 0)

    def base(self, canvas, position, length, angle):
        """
        Рисует на холсте canvas базовый элемент фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        one_third = 1/3*length
        color = self.current_color()
        p1 = (position[0]+one_third, position[1]+one_third)
        p2 = (position[0]+2*one_third, position[1]+one_third)
        p3 = (position[0]+2*one_third, position[1]+2*one_third)
        p4 = (position[0]+one_third, position[1]+2*one_third)
        position = (p1,p2,p3,p4)
        canvas.draw_polygon(position, 1, color, color)

    def iteration(self, canvas, position, length, angle):
        """
        Cтроит на холсте canvas одну итерацию фрактала,
        начиная с точки position, размером length и ориентацией angle.
        """
        self.base(canvas, position, length, angle)
        one_third = 1/3*length
        self.recursive(canvas, position, length/3, angle)
        self.recursive(canvas, (position[0]+one_third, position[1]), length/3, angle)
        self.recursive(canvas, (position[0]+2*one_third, position[1]), length/3, angle)
        self.recursive(canvas, (position[0], position[1]+one_third), length/3, angle)
        self.recursive(canvas, (position[0]+2*one_third, position[1]+one_third), length/3, angle)
        self.recursive(canvas, (position[0], position[1]+2*one_third), length/3, angle)
        self.recursive(canvas, (position[0]+one_third, position[1]+2*one_third), length/3, angle)
        self.recursive(canvas, (position[0]+2*one_third, position[1]+2*one_third), length/3, angle)


def draw(canvas):
    """
    Обработчик рисования.
    :param canvas:  холст
    """
    f.draw(canvas)


def set_levels(text):
    """
    Обработчик текствого поля.
    Устанавливает значение максимального уровня (переменная max_levels).
    """
    global max_levels
    max_levels = int(text)
    level_label.set_text(LABEL_TEXT + str(max_levels))


def cantor_set():
    """
    Обработчик кнопки "Множество Кантора"
    """
    global f
    f = CantorSet((255, 0, 0), (0, 255, 0))


def fractal_tree():
    """
    Обработчик кнопки "Фрактальное дерево"
    """
    global f
    f = FractalTree((204, 153, 0), (153, 204, 0))


def koch_line():
    """
    Обработчик кнопки "Кривая Коха"
    """
    global f
    f = KochLine((0, 0, 0), (0, 0, 0))


def koch_snowflake():
    """
    Обработчик кнопки "Снежинка Коха"
    """

    global f
    f = KochSnowflake((0, 0, 0), (0, 0, 0))


def serpinsky_carpet():
    """
    Обработчик кнопки "Ковёр Серпинского"
    """
    global f
    f = SerpinskyCarpet((0, 0, 255), (0, 255, 0))


# По умолчанию создаём множество Кантора
cantor_set()

# Создание окна и настройка обработчиков
frame = simplegui.create_frame("Фракталы", SIZE, SIZE)
frame.set_canvas_background("White")
frame.set_draw_handler(draw)
frame.add_input("Число уровней", set_levels, 50)
level_label = frame.add_label(LABEL_TEXT + str(max_levels), 150)
frame.add_button("Множество Кантора", cantor_set, 150)
frame.add_button("Дерево", fractal_tree, 150)
frame.add_button("Кривая Коха", koch_line, 150)
frame.add_button("Снежинка Коха", koch_snowflake, 150)
frame.add_button("Ковёр Серпинского", serpinsky_carpet, 150)

# Запуск окна
frame.start()

# Всегда проверяйте, полностью ли выполнено задание,
# сверив работу программы с описанием задания и разделом "Оценка задания".
