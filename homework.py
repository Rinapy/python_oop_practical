from dataclasses import dataclass, asdict
from msilib.schema import Error
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    PHRASE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает результаты и ти тренировки"""
        return self.PHRASE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Определяет дефолтную длинну шага
    M_IN_KM: float = 1000.00
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIE_BURN_RATE_1: float = 18.0
    CALORIE_BURN_RATE_2: float = 20.0

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIE_BURN_RATE_1
             * self.get_mean_speed()
             - self.CALORIE_BURN_RATE_2) * self.weight_kg
            / self.M_IN_KM * self.duration_h * self.H_IN_M
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_BURN_RATE_1: float = 0.035
    CALORIE_BURN_RATE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float, weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height_ce = height

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIE_BURN_RATE_1 * self.weight_kg
             + (self.get_mean_speed()**2 // self.height_ce)
             * self.CALORIE_BURN_RATE_2
             * self.weight_kg)
            * self.duration_h * self.H_IN_M
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIE_BURN_RATE_1: float = 1.1
    CALORIE_BURN_RATE_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool_me = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            (self.lenght_pool_me
             * self.count_pool / self.M_IN_KM
             / self.duration_h)
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed()
             + self.CALORIE_BURN_RATE_1)
            * self.CALORIE_BURN_RATE_2 * self.weight_kg
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        training: Type[Training] = workout_type_dict[workout_type](*data)
    except KeyError:
        raise KeyError(
            f'Invalid workout code "{workout_type}".'
            f'Available codes {workout_type_dict.keys()}')
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    string = info.get_message()
    print(string)


if __name__ == '__main__':
    packages = [
        ('SWs', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
