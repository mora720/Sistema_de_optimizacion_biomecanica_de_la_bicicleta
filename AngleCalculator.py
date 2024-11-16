import numpy as np

class AngleCalculator:
    def __init__(self):
        self.angle_data = {2: [], 3: [], 4: [], 5: []}  # Almacena ángulos para cada punto intermedio

    def calculate_angle(self, pt1, pt2, pt3):
        vec1 = np.array([pt1[0] - pt2[0], pt1[1] - pt2[1]])
        vec2 = np.array([pt3[0] - pt2[0], pt3[1] - pt2[1]])
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0  # evitar división por cero en vectores nulos
        cos_theta = np.dot(vec1, vec2) / (norm_vec1 * norm_vec2)
        angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
        return angle

    def store_angle(self, point_index, angle):
        if point_index in self.angle_data:
            self.angle_data[point_index].append(angle)

    def save_angles_to_csv(self, csv_path="angle_summary.csv"):
        import pandas as pd

        angle_summary = {
            "Punto": ["2", "3", "4", "5"],
            "Ángulo Mínimo": [min(self.angle_data[2]), min(self.angle_data[3]), min(self.angle_data[4]), min(self.angle_data[5])],
            "Ángulo Máximo": [max(self.angle_data[2]), max(self.angle_data[3]), max(self.angle_data[4]), max(self.angle_data[5])]
        }
        df = pd.DataFrame(angle_summary)
        df.to_csv(csv_path, index=False)
        print(f"Ángulos máximos y mínimos guardados en: {csv_path}")
