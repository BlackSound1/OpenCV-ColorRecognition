import sys

import cv2


def getWebCam() -> cv2.VideoCapture:
    """
    Grab the capture from the 0th webcam

    :return capture: The webcam capture
    """

    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("No webcam detected. Quitting")
        sys.exit(1)

    # Set resolution to FHD
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    return capture


def getCenterCoords(frame: cv2.typing.MatLike) -> tuple[int, int]:
    """
    Get center of the frame

    :param frame: The current frame
    :returns: A tuple of the center coordinates
    """
    HEIGHT, WIDTH, _ = frame.shape
    CENTER_X = WIDTH // 2
    CENTER_Y = HEIGHT // 2
    return CENTER_X, CENTER_Y


def getBGR(frame: cv2.typing.MatLike) -> tuple[int, int, int]:
    """
    Get the BGR color to change the text color with

    :param frame: The current frame
    :returns: A tuple of BGR values
    """
    CENTER_X, CENTER_Y = getCenterCoords(frame)
    PIXEL_CENTER_BGR = frame[CENTER_Y, CENTER_X]
    return int(PIXEL_CENTER_BGR[0]), int(PIXEL_CENTER_BGR[1]), int(PIXEL_CENTER_BGR[2])


def decideColor(frame: cv2.typing.MatLike) -> str:
    """
    Decide what color the center of the frame is

    :param frame: The current frame
    :returns: The color as a string
    """

    # Convert frame to HSV
    HSV_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get center of the frame
    CENTER_X, CENTER_Y = getCenterCoords(frame)

    # HSV is defined as (HUE, SATURATION, VALUE).
    # The color can be approximated by the HUE alone
    HUE = HSV_frame[CENTER_Y, CENTER_X, 0]

    COLORS = {
        (0, 5): "RED",
        (5, 22): "ORANGE",
        (22, 33): "YELLOW",
        (33, 78): "GREEN",
        (78, 131): "BLUE",
        (131, 170): "VIOLET",
        (170, 180): "RED",
    }

    # Look up the color
    for start, end in COLORS.keys():
        if start <= HUE <= end:
            color = COLORS[(start, end)]
            break
    else:
        color = "Unknown"

    return color


def main():
    WEBCAM = getWebCam()

    while True:
        _, frame = WEBCAM.read()

        CENTER_X, CENTER_Y = getCenterCoords(frame)

        # Show the color of the object
        color = decideColor(frame)

        cv2.putText(frame, text=color, org=(10, 70), fontFace=0, fontScale=1.5, color=getBGR(frame), thickness=2)

        # Show center of frame as a circle
        cv2.putText(
            frame,
            color=(255, 255, 0),
            text="Put an object in this circle",
            org=(CENTER_X - 250, CENTER_Y - 20),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=1.2,
        )
        cv2.circle(frame, center=(CENTER_X, CENTER_Y), radius=5, color=(0, 255, 0), thickness=3)

        cv2.imshow("Color Recognition", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    # Let go of the webcam so other processes can use it
    WEBCAM.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
