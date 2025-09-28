import cv2
import numpy as np


def main():
    # Sliders
    WINDOW_NAME = "HSV Color Picker"
    cv2.namedWindow(WINDOW_NAME)
    cv2.createTrackbar("H", WINDOW_NAME, 0, 179, lambda _: None)
    cv2.createTrackbar("S", WINDOW_NAME, 255, 255, lambda _: None)
    cv2.createTrackbar("V", WINDOW_NAME, 255, 255, lambda _: None)

    # Create a black rectangle to store color info
    image_HSV = np.zeros((250, 500, 3), np.uint8)

    while True:
        H = cv2.getTrackbarPos("H", WINDOW_NAME)
        S = cv2.getTrackbarPos("S", WINDOW_NAME)
        V = cv2.getTrackbarPos("V", WINDOW_NAME)

        # Replace the whole black rectangle with the HSV color
        image_HSV[:] = (H, S, V)

        # Convert from HSV to BGR colors
        image_BGR = cv2.cvtColor(image_HSV, cv2.COLOR_HSV2BGR)

        cv2.imshow(WINDOW_NAME, image_BGR)

        # Wait for the 'q' key to leave the loopggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
