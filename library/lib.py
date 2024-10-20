import cv2
from datetime import datetime

def tirar_foto():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Não foi possível acessar a câmera.")
        return False

    ret, frame = camera.read()

    if ret:
        cv2.imwrite("./tmp/image.jpg", frame)
    else:
        return False
    
    camera.release()

    cv2.destroyAllWindows()

    return True

if __name__ == "__main__":
    pass