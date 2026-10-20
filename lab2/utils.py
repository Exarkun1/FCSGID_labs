"""Диапазон температуры и преобразования между температурными шкалами"""

MIN_CELSIUS = -90.0
MAX_CELSIUS = 60.0


def celsius_to_fahrenheit(degree: float) -> float:
    """Перевести градусы Цельсия в градусы Фаренгейта без округления"""
    return degree * 9 / 5 + 32


def fahrenheit_to_celsius(degree: float) -> float:
    """Перевести градусы Фаренгейта в градусы Цельсия без округления"""
    return (degree - 32) * 5 / 9


def celsius_to_kelvin(degree: float) -> float:
    """Перевести градусы Цельсия в кельвины без округления"""
    return degree + 273.15


def kelvin_to_celsius(degree: float) -> float:
    """Перевести кельвины в градусы Цельсия без округления"""
    return degree - 273.15
