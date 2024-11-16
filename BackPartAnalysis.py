import cv2
import numpy as np
import pandas as pd

class BackPartAnalysis:
    def __init__(self, lower_color, upper_color, min_contour_area=10):
        self.lower_color = np.array(lower_color)
        self.upper_color = np.array(upper_color)
        self.min_contour_area = min_contour_area
        self.kernel1 = np.ones((9, 9), np.uint8)
        self.kernel2 = np.ones((7, 7), np.uint8)
        self.point_trajectories = {"I1": [], "I2": [], "R1": [], "R2": []}

    def identify_points(self, video_source=0):  # Usar una segunda cámara (cambiar si se usa un archivo de video)
        cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: No se puede abrir la cámara/video")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fin del video o error al recibir el fotograma")
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

            if len(centers) != 4:
                cv2.putText(frame, f"Advertencia: {len(centers)} puntos detectados (se necesitan 4)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                top_points = sorted(centers, key=lambda p: p[1], reverse=True)[:2]
                bottom_points = sorted(centers, key=lambda p: p[1])[:2]

                I1 = min(bottom_points, key=lambda p: p[0])
                R1 = max(bottom_points, key=lambda p: p[0])
                I2 = min(top_points, key=lambda p: p[0])
                R2 = max(top_points, key=lambda p: p[0])

                labeled_points = {"I1": I1, "I2": I2, "R1": R1, "R2": R2}

                for label, (center_x, center_y) in labeled_points.items():
                    self.point_trajectories[label].append((center_x, center_y))
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                    cv2.putText(frame, label, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                for label, trajectory in self.point_trajectories.items():
                    for i in range(1, len(trajectory)):
                        cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 255, 255), 1)

            cv2.imshow('Puntos de Color Detectados', frame)
            cv2.imshow('Máscara de Color', mask)

            if cv2.waitKey(1) == 13:  # Enter para salir
                break

        cap.release()
        cv2.destroyAllWindows()
        self.show_trajectory_table()

    def show_trajectory_table(self):
        data = {label: coords for label, coords in self.point_trajectories.items()}
        max_length = max(len(coords) for coords in data.values())
        for label, coords in data.items():
            data[label] = coords + [("", "")] * (max_length - len(coords))
        df = pd.DataFrame(data, columns=["I1", "I2", "R1", "R2"])
        df = df.applymap(lambda coord: f"{coord}" if coord != ("", "") else "")
        print(df)
