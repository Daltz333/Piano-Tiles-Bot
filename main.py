# Copyright 2019 Dalton Smith
# Use at your own risk. I am not responsible for
# any damage or thermonuclear warfare that may have been caused by
# using this program. Enjoy :)

import keyboard
import pyautogui
import cv2
import numpy as np
import mss.tools

# auto-clicker for piano tiles
window_preview_init_x = 0
window_preview_init_y = 0

window_preview_width = 400
window_preview_height = 700

tile_color_min = np.array([0, 0, 0])
tile_color_max = np.array([0, 0, 0])

window_preview = {"top": window_preview_init_y, "left": window_preview_init_x,
                  "width": window_preview_width, "height": window_preview_height}

pyautogui.PAUSE = 0

sct = mss.mss()

tracking = False


def main():
    while True:
        img = np.array(sct.grab(window_preview))

        frame = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        frame = cv2.medianBlur(frame, 5)
        mask = cv2.inRange(frame, tile_color_min, tile_color_max)

        (_, cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[1], reverse=True)

        try:
            # iterate over our contours
            for cnt in cnts:
                if keyboard.is_pressed('q'):
                    continue

                # find all the rectangles
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # ensure proper width
                if w < 20:
                    print("Too small!")
                    continue

                # ensure below threshold
                if y > 400:
                    print("Detected Blob!")
                    print("X: " + str(x) + " Y: " + str(y) + " W: " + str(w) + " H: " + str(h))
                    cv2.putText(mask, "Tracking", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                                lineType=cv2.LINE_AA)

                    x_location = round((x+(w/4)))

                    print(x_location)

                    pyautogui.click(x_location, y+(h/2), 1, 0)
                    break

                else:
                    print("No blob detected!")
                    continue

        except cv2.error:
            print("error")
            pass

        cv2.imshow("Script", mask)

        cv2.waitKey(5)

        # globally begone thot
        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
