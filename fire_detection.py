import cv2
import numpy as np

cap = cv2.VideoCapture("fire1.mp4")
#cap = cv2.VideoCapture(0)

lowRed = np.array([0, 50, 50]) #kırmızı ve turuncu renklerini kapsayan ortak değerler kullanılmıştır.
upRed = np.array([35, 255, 255])

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (600, 600))
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, lowRed, upRed)
    red = cv2.bitwise_and(frame, frame, mask = red_mask)
    red = cv2.resize(red, (600, 600))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #bir görüntünün aynı renk yoğunluğuna sahip tüm noktaları birleştiren fonksiyon denebilir.

    x, y, w, h = 0, 0, 0, 0

    if contours:
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), ((x+w), (y+h)), (255, 0, 0), 2) #çerçeve çizip text olarak fire yazıldı.
                cv2.putText(frame,"fire",(x,y),2,2,(0,255,0),2)
                break


        x_c = ((2 * x) + w) / 2
        y_c = ((2 * y) + h) / 2
        center = (x_c, y_c)
        cv2.circle(frame, (int(x_c), int(y_c)), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(red, (int(x_c), int(y_c)), 5, (255, 0, 0), cv2.FILLED)

        print("[INFO].. center is calculated", center)

    cv2.imshow("mask", red)
    cv2.imshow("red", frame)

   key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
