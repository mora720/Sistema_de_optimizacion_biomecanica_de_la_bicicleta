import cv2
import numpy as np
from AngleCalculator import AngleCalculator  # Importa la clase de cálculo de ángulos

class PointAnalyzer:
    def __init__(self, lower_color, upper_color, min_contour_area=10):
        self.lower_color = np.array(lower_color)
        self.upper_color = np.array(upper_color)
        self.min_contour_area = min_contour_area
        self.kernel1 = np.ones((9, 9), np.uint8)
        self.kernel2 = np.ones((7, 7), np.uint8)
        self.angle_calculator = AngleCalculator()  # Instancia de la clase de cálculo de ángulos

    def analyze_points(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: No se puede abrir la cámara")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se puede recibir el fotograma")
                break

            frame = cv2.flip(frame, 1)
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, self.lower_color, self.upper_color)
            mask = cv2.dilate(cv2.erode(mask, self.kernel2, iterations=1), self.kernel1, iterations=1)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            centers = [
                (x + w // 2, y + h // 2)
                for contour in contours if cv2.contourArea(contour) >= self.min_contour_area
                for x, y, w, h in [cv2.boundingRect(contour)]
            ]

            if len(centers) != 6:
                cv2.putText(frame, "No se encontraron 6 puntos", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Puntos Detectados y Conectados con Ángulos', frame)
                if cv2.waitKey(1) == 13:  # Enter key
                    break
                continue  # Saltar al siguiente fotograma

            centers.sort(key=lambda p: p[0])
            point_3, point_5, point_6 = centers[0], centers[-2], centers[-1]
            remaining_points = sorted(centers[1:-2], key=lambda p: p[1])
            point_4, point_2, point_1 = remaining_points

            ordered_points = [point_1, point_2, point_3, point_4, point_5, point_6]
            for i, center in enumerate(ordered_points, start=1):
                x, y = center
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"{i}", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            for i in range(len(ordered_points) - 1):
                cv2.line(frame, ordered_points[i], ordered_points[i + 1], (255, 0, 0), 2)

            for i, point_index in enumerate([2, 3, 4, 5], start=1):
                angle = self.angle_calculator.calculate_angle(ordered_points[i - 1], ordered_points[i], ordered_points[i + 1])
                x, y = ordered_points[i]
                cv2.putText(frame, f"{angle:.1f}", (x + 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                self.angle_calculator.store_angle(point_index, angle)
            
            cv2.imshow('Puntos Detectados y Conectados con Ángulos', frame)
            if cv2.waitKey(1) == 13:  # Enter key
                break

        cap.release()
        cv2.destroyAllWindows()
        self.angle_calculator.save_angles_to_csv()
