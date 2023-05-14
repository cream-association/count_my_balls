import cv2
import numpy as np


cap = cv2.VideoCapture("http://localhost:8080/video")

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((7, 7), np.uint8)

    lower_red = np.array([164, 113, 139])
    upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # lower_red = np.array([170, 70, 50])
    # upper_red = np.array([180, 255, 255])
    # mask2 = cv2.inRange(hsv, lower_red, upper_red)
    # mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
    # mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)

    # mask = mask1 + mask2

    mask = cv2.GaussianBlur(mask, (9, 9), 2)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # if area > 1000:
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        # if aspect_ratio < 1.2:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1

    cv2.putText(
        frame,
        "Nombre de cerise: {}".format(count),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
