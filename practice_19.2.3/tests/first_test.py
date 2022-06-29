import pytest
from app.calculator import Calculator

class TestCals:  # название класса и методов начинается со слова Test
    def setup(self):               # подготовительный метод
         self.calc = Calculator     # создаём объект из импортируемого класса #

    def test_multiply_calculate_correctly(self): # в названии пишим функцию, которую проверяем
        assert self.calc.multiply(self, 2, 2) == 4  #и результат,который ожидаем. Сравниваем

    def test_multyply_calculation_failed(self):
        assert self.calc.multiply(self, 2, 2) == 5

    def test_division_calculate_correctly(self):
        assert self.calc.division(self, 10, 5) == 2

    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(self, -3, 2) == -5

    def test_adding_calculate_correctly(self):
        assert self.calc.adding(self, 1, 2) == 3



