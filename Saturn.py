import cv2
import numpy as np
import pyautogui
from pynput.keyboard import Key , Controller    # Virtual keyboard is used to convey commands to the MBlock environment.
    # In MBlock, we used arrow keys to control the car. Our algorithm first detects the color, then clicks a key virtually.
import time
cc = 0
keyboard = Controller()
rt = 0
while True:
    img = np.array(pyautogui.screenshot(region = (380, 140, 320, 220))) # First we reflected the video stream to the desktop,
    # Then we capture the desktop as a webcam,
    # After that, we masked all the colours.
    # Then we measured their weights
    r_cc = 0
    antir_cc = 0
    antib_cc = 0
    antig_cc = 0
    g_cc = 0
    b_cc = 0

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    frame = img
    cv2.imshow("frame",frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    g_l_h = 44 # We restricted the color space to obtain more accurate results.
    g_l_s = 58
    g_l_v = 56
    g_u_h = 75
    g_u_s = 169
    g_u_v = 255
    lower_green = np.array([g_l_h,g_l_s,g_l_v])
    upper_green = np.array([g_u_h,g_u_s,g_u_v])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(frame, frame, mask=green_mask)

    keyboard.press(Key.up)

    for i in green_mask:
        for j in i :
            if j != 0 :
                g_cc += 1
            else :
                antig_cc += 1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    b_l_h = 79
    b_l_s = 65
    b_l_v = 83
    b_u_h = 141
    b_u_s = 197
    b_u_v = 190
    lower_blue = np.array([b_l_h, b_l_s, b_l_v])
    upper_blue = np.array([b_u_h, b_u_s, b_u_v])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=blue_mask)

    for i in blue_mask:
        for j in i:
            if j != 0:
                b_cc += 1
            else :
                antib_cc += 1


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    r_l_h = 132
    r_l_s = 0
    r_l_v = 0
    r_u_h = 179
    r_u_s = 104
    r_u_v = 255
    lower_red = np.array([r_l_h, r_l_s, r_l_v])
    upper_red = np.array([r_u_h, r_u_s, r_u_v])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=red_mask)

    for i in red_mask:
        for j in i:
            if j != 0:
                r_cc +=1
            else :
                antir_cc +=1
    try :
        if g_cc/(b_cc+r_cc+g_cc) > 0.5 or b_cc/(g_cc+r_cc+b_cc) > 0.7 or r_cc/(b_cc+g_cc+r_cc) > 0.7 :

            if g_cc > b_cc and g_cc > r_cc  :

                print("green")
                rt = 0
                keyboard.release(Key.up)
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                time.sleep(1) # To prevent miss calculation, we added some delay while turning
            elif b_cc > g_cc and b_cc > r_cc :
                print("blue")
                rt = 0
                keyboard.release(Key.up)
                keyboard.press(Key.left)
                keyboard.release(Key.left)
                time.sleep(1)
            elif r_cc > b_cc and r_cc > g_cc and rt == 0:
                rt = 1
                print("red")
                keyboard.release(Key.up)
                time.sleep(10)
    except ZeroDivisionError:
        key = cv2.waitKey(1)
        if key == 27:
            break
cap.release()
cv2.destroyAllWindows()