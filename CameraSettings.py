import cv2

class CameraSettings:
    def __init__(self):
        self.brightness = 0.5  

    def adjust_brightness(self):

        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("Error: No se puede abrir la cámara")
            return
        
        cv2.namedWindow("Adjust Brightness")

        def update_brightness(value):
            self.brightness = value / 100  
            cap.set(cv2.CAP_PROP_BRIGHTNESS, self.brightness)

        cv2.createTrackbar("Brightness", "Adjust Brightness", int(self.brightness * 100), 100, update_brightness)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se puede recibir el fotograma")
                break
            frame = cv2.flip(frame, 1)
            cv2.imshow("Adjust Brightness", frame)
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
        return self.brightness

