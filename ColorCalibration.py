import cv2
import numpy as np

class ColorCalibration:
    def __init__(self, Brightness, box_width=50, box_height=50, max_captures=3):
        self.Brightness = Brightness
        self.box_width = box_width
        self.box_height = box_height
        self.max_captures = max_captures
        self.lower_hsv_values = []
        self.upper_hsv_values = []

    def capture_color(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, self.Brightness)
        cv2.namedWindow('Select Color Region')
        capture_count = 0

        while capture_count < self.max_captures:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se puede recibir el fotograma")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            start_point = (width // 2 - self.box_width // 2, height // 2 - self.box_height // 2)
            end_point = (width // 2 + self.box_width // 2, height // 2 + self.box_height // 2)

            cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow('Select Color Region', frame)

            if cv2.waitKey(1) == 13:  # Enter key
                x1, y1 = start_point
                x2, y2 = end_point
                selected_region = frame[y1:y2, x1:x2]
                hsv_region = cv2.cvtColor(selected_region, cv2.COLOR_BGR2HSV)

                # Aplanar la región y calcular los valores mínimos y máximos
                reshaped_hsv = hsv_region.reshape(-1, 3)
                lower_color = np.min(reshaped_hsv, axis=0)
                upper_color = np.max(reshaped_hsv, axis=0)

                self.lower_hsv_values.append(lower_color)
                self.upper_hsv_values.append(upper_color)

                print(f"Captura {capture_count + 1}:")
                print("Lower HSV Bound: ", lower_color.astype(int))
                print("Upper HSV Bound: ", upper_color.astype(int))
                capture_count += 1

        cap.release()
        cv2.destroyAllWindows()

        if capture_count == self.max_captures:
            avg_lower_hsv = [sum(x) // self.max_captures for x in zip(*self.lower_hsv_values)]
            avg_upper_hsv = [sum(x) // self.max_captures for x in zip(*self.upper_hsv_values)]

            print("\nPromedio final:")
            print("Lower HSV Bound promedio: ", avg_lower_hsv)
            print("Upper HSV Bound promedio: ", avg_upper_hsv)

        return avg_lower_hsv, avg_upper_hsv
