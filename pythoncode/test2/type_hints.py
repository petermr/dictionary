# cfrom Rajarshi Guha
from typing import List, Union


class Unit:
    def __init__(self):
        pass


class Result:
    def __init__(self, value: float, unit: Unit):
        self._value = value
        self._unit = unit


Smiles = str


def predict_activity(smi: Smiles, values: List[Result] = None) -> List[float]:
    return "hello"


if __name__ == '__main__':
    print("main")
    print(predict_activity(123.34, None))
    print(predict_activity("CCCC", [1, 2, 3]))
    print(predict_activity("CCCC", [Result(12.0, Unit())]))

