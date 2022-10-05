class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        pass

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: {toFixed(self.duration)} ч.; Дистанция: {toFixed(self.distance)} км; Ср. скорость: {toFixed(self.speed)} км/ч; Потрачено ккал: {toFixed(self.calories)}.')

    pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Определяет дефолтную длинну шага
    M_IN_KM: float = 1000.00
    TRINING_TYPE: str = ''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        result = InfoMessage(self.TRINING_TYPE, self.duration,
                             self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return result


class Running(Training):
    """Тренировка: бег."""
    TRINING_TYPE: str = 'Running'

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        pass

    def get_spent_calories(self) -> float:
        self.coeff_calorie_1 = 18
        self.coeff_calorie_2 = 20
        self.duration_in_minute = self.duration * 60
        self.spent_calories = (self.coeff_calorie_1
                               * self.get_mean_speed()
                               - self.coeff_calorie_2) * self.weight /\
            self.M_IN_KM * self.duration_in_minute
        return self.spent_calories

    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRINING_TYPE: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float, weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        pass

    def get_spent_calories(self) -> float:
        self.coeff_calorie_1 = 0.035
        self.coeff_calorie_2 = 0.029
        self.duration_in_minute = self.duration * 60
        self.spent_calories = (self.coeff_calorie_1 * self.weight
                               + (self.get_mean_speed()**2 // self.height)
                               * self.coeff_calorie_2
                               * self.weight) * self.duration_in_minute
        return self.spent_calories

    pass


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    TRINING_TYPE: str = 'Swimming'

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool
        pass

    def get_mean_speed(self) -> float:
        return self.lenght_pool * \
            self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        self.coeff_calorie_1 = 1.1
        self.coeff_calorie_2 = 2
        self.spent_calories = (self.get_mean_speed(
        ) + self.coeff_calorie_1) * self.coeff_calorie_2 * self.weight
        return self.spent_calories

    pass


def toFixed(numObj, digits=3):
    return f"{numObj:.{digits}f}"


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
    if workout_type == list(workout_type_dict.keys())[0]:
        training = workout_type_dict['SWM'](
            data[0], data[1], data[2], data[3], data[4])
    elif workout_type == list(workout_type_dict.keys())[1]:
        training = workout_type_dict['RUN'](data[0], data[1], data[2])
    else:
        training = workout_type_dict['WLK'](data[0], data[1], data[2], data[3])
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    string = info.get_message()
    print(string)
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
