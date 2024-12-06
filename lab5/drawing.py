import numpy as np


def lagrange_surface(x_points, y_points, num_samples=100, num_layers=50):
    x_min, x_max = min(x_points), max(x_points)
    n = len(x_points)

    # Генерируем значения x для сетки
    x_vals = np.linspace(x_min, x_max, num_samples)
    # Генерируем значения z для сетки (ось Z будет глубиной)
    z_layers = np.linspace(-5, 5, num_layers)

    # Вычисляем значения полинома Лагранжа для каждого x
    y_vals = np.zeros_like(x_vals)
    for i in range(n):
        l_i = np.ones_like(x_vals)
        for j in range(n):
            if i != j:
                l_i *= (x_vals - x_points[j]) / (x_points[i] - x_points[j])
        y_vals += y_points[i] * l_i

    # Создаем сетку координат
    vertices = []
    for z in z_layers:
        for x, y in zip(x_vals, y_vals):
            vertices.extend([x, y, z])

    # Создаем индексы для треугольников
    indices = []
    num_vertices_per_layer = num_samples
    for i in range(num_layers - 1):
        for j in range(num_samples - 1):
            idx = i * num_vertices_per_layer + j
            indices.extend([
                idx, idx + num_vertices_per_layer, idx + num_vertices_per_layer + 1,
                idx, idx + num_vertices_per_layer + 1, idx + 1
            ])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)
