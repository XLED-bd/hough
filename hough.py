from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks, rotate
import numpy as np

def hough(gray): 
    """ На вход идет серое изображение в виде массива numpy произвольного размера
    и возвращает нормализированное/повернутое изображение в виде массива numpy"""
    edges = canny(gray) # находим границы объектов такие как номерных знаков или бамперов

    h, theta, d = hough_line(edges) # Выполнение преобразования Хафана основе границ объектов
                                    # Возвращаемые значения:
                                    # h - аккумуляторное пространство Хафа, является двумерной матрицей,
                                    # где каждый элемент матрицы соотвествует возможной линии на изображении
                                    # theta - массив углов
                                    # d - массив расстояний

    _, angles_peaks, _ = hough_line_peaks(h, theta, d, num_peaks=20) # находит пиковые значения
                                                                     # в аккумуляторном пространстве Хафа
                                                                     # используя theta, d
    angle = np.mean(np.rad2deg(angles_peaks)) # Вычисляет среднее значение углов пиковых линий

    if 0 <= angle <= 90:
        rot_angle = angle - 90
    elif -45 <= angle < 0:
        rot_angle = angle - 90
    elif -90 <= angle < -45:
        rot_angle = angle + 90

    if abs(rot_angle) > 90: # Если получившийся угл больше 90 градусов не преобразоовать его
                            # Чтобы избежать отзеркаливания изображения
        rot_angle = 0

    rotated = rotate(gray, rot_angle, resize=False) # Поворачиваем изображение сохраняя пропорции
    return rotated