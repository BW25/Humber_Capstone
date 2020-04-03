
import cv2

video = cv2.VideoCapture(-1)


if video.isOpened() == True:
    while True:
        ret, frame = video.read()
        
        
        cv2.imshow("video", frame)
        

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
else:
    print('Cannot access camera')
