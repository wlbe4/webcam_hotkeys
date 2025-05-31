import os,sys,cv2, time, pyautogui

def main():
    key_names = pyautogui.KEY_NAMES
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit(1)
    detector = cv2.QRCodeDetector()
    FRAMES_TO_DETECT = 30
    detected_frames = 0
    b_rq_detected = False
    detected_data = ''
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
        else:
            data, bbox, _ = detector.detectAndDecode(frame)
            # check if there is a QRCode in the image
            if data:
                if data == detected_data:
                    if detected_frames <  FRAMES_TO_DETECT:
                        detected_frames = FRAMES_TO_DETECT
                elif not b_rq_detected:
                    detected_data = data
                    b_rq_detected = True
                    detected_frames = FRAMES_TO_DETECT
                    print("QR Code detected:", data)
                    key_detected = data.lower()
                    # Send a keyboard event with the detected data
                    if len(key_detected) == 2 and key_detected[0] == 'f':
                        pyautogui.press(key_detected)
                    
                    # Optionally, draw a bounding box around the QR code
                    for box in bbox:
                        cv2.polylines(frame, [box.astype(int)], True, (0, 255, 0), 2)
            else:
                if b_rq_detected:
                    if detected_frames:
                        detected_frames -= 1
                    else:
                        print("QR Code lost")
                        b_rq_detected = False
                        detected_data = ''
            cv2.imshow('Webcam Feed', frame)
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
# This script captures video from the webcam and displays it in a window.
