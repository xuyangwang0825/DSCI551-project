import logging
import numpy as np
import cv2

def get_first_frame(save_path, video_oath):
    cap = cv2.VideoCapture(video_oath)
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, image = cap.read()
    cv2.imwrite(save_path, image)

    cap.release()
    cv2.destroyAllWindows()