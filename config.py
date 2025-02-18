import numpy as np

EXAMPLES = {
    # Базовые фильтры
    "Повышение резкости": np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]),
    "Гауссово размытие": np.array([
        [0.0625, 0.125, 0.0625],
        [0.125, 0.25, 0.125],
        [0.0625, 0.125, 0.0625]
    ]),
    "Детектор краёв": np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ]),

    # Новые фильтры
    "Эффект тиснения": np.array([
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ]),
    "Контурная резкость": np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ]),
    "Точечное размытие": np.array([
        [0, 0.2, 0],
        [0.2, 0.2, 0.2],
        [0, 0.2, 0]
    ]),
    "Повышение контраста": np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ]),
    "Эффект рельефа": np.array([
        [1, 1, 0],
        [1, 0, -1],
        [0, -1, -1]
    ])
}