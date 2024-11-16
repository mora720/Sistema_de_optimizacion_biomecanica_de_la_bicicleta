from ColorCalibration import ColorCalibration
from ColorDetection import PointAnalyzer  
from CameraSettings import CameraSettings
from BackPartAnalysis import BackPartAnalysis
def main():
    # Calibrar la iluminocidad
    Camera = CameraSettings()
    Brightness = Camera.adjust_brightness()
    
    # Capturar los colores HSV del objeto
    camera_capture = ColorCalibration(Brightness)
    lower_color, upper_color = camera_capture.capture_color()
    
    # Usar los colores capturados para analizar los puntos y ángulos
    analyzer = PointAnalyzer(lower_color, upper_color)    
    analyzer.analyze_points()

    #Empieza el analisis trasero
    Back = BackPartAnalysis(lower_color, upper_color)
    Back.identify_points()


if __name__ == "__main__":
    main()
