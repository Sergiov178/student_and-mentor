class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []  # Список завершённых курсов
        self.courses_in_progress = []  # Список курсов в процессе изучения
        self.grades = {}  # Словарь оценок за домашние задания

    # Метод оценки лектора студентом
    def rate_lecture(self, lecturer, course, grade):

        # Проверяем:
        # 1. lecturer является объектом Lecturer
        # 2. курс закреплён за лектором
        # 3. студент изучает этот курс
        # 4. оценка находится в диапазоне от 1 до 10
        if (
            isinstance(lecturer, Lecturer)
            and course in lecturer.courses_attached
            and course in self.courses_in_progress
            and isinstance(grade, int)
            and 1 <= grade <= 10
        ):

            # Если курс уже есть в словаре оценок лектора —
            # добавляем новую оценку
            lecturer.grades.setdefault(course, []).append(grade)
            return 'Оценка добавлена'

        return 'Ошибка'

    def average_grade(self):

        # Создаём список для хранения всех оценок
        grades_list = []

        for grades in self.grades.values():
            grades_list += grades

        # Возвращаем среднее значение
        # Если оценок нет — возвращаем 0
        return sum(grades_list) / len(grades_list) if grades_list else 0

    # Магический метод строкового представления объекта
    def __str__(self):

        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.average_grade():.1f}\n'
            f'Курсы в процессе изучения: '
            f'{", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: '
            f'{", ".join(self.finished_courses)}'
        )

    # Магический метод сравнения "меньше"
    def __lt__(self, other):

        # Сравниваем студентов по средней оценке
        if isinstance(other, Student):
            return self.average_grade() < other.average_grade()

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Student):
            return self.average_grade() > other.average_grade()

        return NotImplemented

    # Магический метод сравнения "равно"
    def __eq__(self, other):

        # Проверяем равенство средних оценок
        if isinstance(other, Student):
            return self.average_grade() == other.average_grade()

        return NotImplemented


class Mentor:

    # Базовый класс Mentor
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Закреплённые курсы


class Lecturer(Mentor):

    def __init__(self, name, surname):

        # Вызываем конструктор родительского класса
        super().__init__(name, surname)

        self.grades = {}  # Оценки за лекции

    # Метод вычисления средней оценки лектора
    def average_grade(self):

        grades_list = []

        # Собираем все оценки лектора
        for grades in self.grades.values():
            grades_list += grades

        # Возвращаем среднюю оценку
        return sum(grades_list) / len(grades_list) if grades_list else 0

    # Строковое представление объекта Lecturer
    def __str__(self):

        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: '
            f'{self.average_grade():.1f}'
        )

    # Сравнение лекторов по средней оценке
    def __lt__(self, other):

        if isinstance(other, Lecturer):
            return self.average_grade() < other.average_grade()

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Lecturer):
            return self.average_grade() > other.average_grade()
        return NotImplemented

    # Проверка равенства лекторов
    def __eq__(self, other):

        if isinstance(other, Lecturer):
            return self.average_grade() == other.average_grade()

        return NotImplemented


# Класс Reviewer
class Reviewer(Mentor):

    # Конструктор Reviewer
    def __init__(self, name, surname):

        # Вызываем конструктор родительского класса
        super().__init__(name, surname)

    # Метод выставления оценки студенту
    def rate_hw(self, student, course, grade):

        # Проверяем:
        # 1. student является объектом Student
        # 2. курс закреплён за проверяющим
        # 3. студент изучает этот курс
        # 4. оценка от 1 до 10
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
            and isinstance(grade, int)
            and 1 <= grade <= 10
        ):

            # Добавляем оценку студенту
            student.grades.setdefault(course, []).append(grade)
            return 'Оценка добавлена'

        return 'Ошибка'

    # Строковое представление Reviewer
    def __str__(self):

        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}'
        )


# Функция подсчета средней оценки студентов
# по конкретному курсу

def average_hw_grade_by_course(students, course):
    # Список всех оценок по курсу
    grades_list = []

    for student in students:

        # Если курс есть у студента —
        # добавляем оценки в общий список
        if course in student.grades:
            grades_list += student.grades[course]

    return sum(grades_list) / len(grades_list) if grades_list else 0


# Функция подсчета средней оценки лекторов
# по конкретному курсу

def average_lecture_grade_by_course(lecturers, course):
    # Список всех оценок лекторов
    grades_list = []

    for lecturer in lecturers:

        # Если курс есть у лектора —
        # добавляем оценки
        if course in lecturer.grades:
            grades_list += lecturer.grades[course]

    return sum(grades_list) / len(grades_list) if grades_list else 0


# Создание объектов класса Student

student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_2 = Student('Иван', 'Сидоров', 'М')

# Создание объектов класса Lecturer

lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_2 = Lecturer('Анна', 'Смирнова')

# Создание объектов класса Reviewer

reviewer_1 = Reviewer('Пётр', 'Петров')
reviewer_2 = Reviewer('Мария', 'Кузнецова')

# Добавление курсов студентам

student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Введение в программирование']

student_2.courses_in_progress += ['Python', 'Java']
student_2.finished_courses += ['Git']

# Добавление курсов лекторам

lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2.courses_attached += ['Python', 'Java']

# Добавление курсов Reviewer

reviewer_1.courses_attached += ['Python', 'Git']
reviewer_2.courses_attached += ['Python', 'Java']

# Reviewer ставят оценки студентам

reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Git', 8)

reviewer_2.rate_hw(student_2, 'Python', 7)
reviewer_2.rate_hw(student_2, 'Java', 9)

# Студенты ставят оценки лекторам

student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)

student_2.rate_lecture(lecturer_1, 'Python', 8)
student_2.rate_lecture(lecturer_2, 'Python', 7)
student_2.rate_lecture(lecturer_2, 'Java', 10)

# Демонстрация отказов при некорректном оценивании
print(reviewer_1.rate_hw(lecturer_1, 'Python', 9)) # Попытка поставить оценку за ДЗ не студенту
print()

print(reviewer_1.rate_hw(student_2, 'Git', 8)) # Попытка поставить оценку за курс, который студент не изучает
print()

print(student_1.rate_lecture(lecturer_2, 'Git', 8)) # Попытка оценить лектора за курс, который он не ведет
print()

# Вывод информации об объектах

print(student_1)
print()

print(student_2)
print()

print(lecturer_1)
print()

print(lecturer_2)
print()

print(reviewer_1)
print()

print(reviewer_2)

# Сравнение объектов

# Проверка сравнения студентов
print(student_1 < student_2)
print(student_1 > student_2)
print(student_1 == student_2)

# Проверка сравнения лекторов
print(lecturer_1 < lecturer_2)
print(lecturer_1 > lecturer_2)
print(lecturer_1 == lecturer_2)

# Вызов функций подсчета средних оценок

print()
print(
    average_hw_grade_by_course(
        [student_1, student_2],
        'Python'
    )
)

print(
    average_lecture_grade_by_course(
        [lecturer_1, lecturer_2],
        'Python'
    )
)

print(student_1.average_grade())
print(student_2.average_grade())

print(lecturer_1.average_grade())
print(lecturer_2.average_grade())