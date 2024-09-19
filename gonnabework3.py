import cv2
import serial
import os
import time
import threading
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import statistics

class Test:
    def __init__(self, port='COM10', baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.filename = None
        self.frame_per_second = 30.0
        self.res = None
        self.STD_DIMENSIONS = {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        self.VIDEO_TYPE = {
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
        self.out = None
        self.handmp = mp.solutions.hands
        self.hands = None
        self.Fg_thresh = 115  # ตั้งค่า Threshold เริ่มต้น
        self.Fg_thresh1 = 255
        self.LightCondition = 0  # 0 = open LED ; 1 = open UV
        self.max_area_left_LED = 0
        self.max_area_right_LED = 0
        self.max_area_left_UV = 0
        self.max_area_right_UV = 0

    def Name(self, filename, frame_per_second, res):
        self.filename = filename
        self.frame_per_second = frame_per_second
        self.res = res

    def change_res(self, cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    def get_dims(self, cap, res='1080p'):
        width, height = self.STD_DIMENSIONS["720p"]
        if res in self.STD_DIMENSIONS:
            width, height = self.STD_DIMENSIONS[res]
        self.change_res(cap, width, height)
        return width, height

    def get_video_type(self, filename):
        filename, ext = os.path.splitext(filename)
        if ext in self.VIDEO_TYPE:
            return self.VIDEO_TYPE[ext]
        return self.VIDEO_TYPE['avi']

    def send_command(self, command):
        self.arduino.write(bytes(command, 'utf-8'))
        time.sleep(0.05)
        return self.arduino.readline()
    
    def initialize_hand_detection(self):
        self.hands = self.handmp.Hands(
            static_image_mode=False, 
            model_complexity=1, 
            min_detection_confidence=0.75, 
            min_tracking_confidence=0.75, 
            max_num_hands=2
        )

    def process_frame(self, frame):
        # frame = cv2.flip(frame, 1)
        frame = cv2.rotate(frame,cv2.ROTATE_180)
        frame = cv2.line(frame, (640, 0), (640, 720), (0, 255, 0), 5)
        ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        blur = cv2.GaussianBlur(ImageLAB[:, :, 0], (3, 3), 0)
        _, Fg_thresh = cv2.threshold(blur, self.Fg_thresh, self.Fg_thresh1 , cv2.THRESH_BINARY)
        FgHand_contours, hierarchy = cv2.findContours(Fg_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # print("hierarchy",hierarchy)
        # parent =statistics.mode(hierarchy[3])
        # print(parent)
    
        sumArea = 0
        for c in FgHand_contours:
            area = cv2.contourArea(c)
            if (area > 1000) :
                sumArea = sumArea + area
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            cx = M["m10"] / M["m00"]

            if self.LightCondition == 0:  # LED light condition
                if cx < 640:
                    self.max_area_left_LED = max(self.max_area_left_LED, sumArea)
                else:
                    self.max_area_right_LED = max(self.max_area_right_LED, sumArea)
            elif self.LightCondition == 1:  # UV light condition
                if cx < 640:
                    self.max_area_left_UV = max(self.max_area_left_UV, sumArea)
                else:
                    self.max_area_right_UV = max(self.max_area_right_UV, sumArea)

            if len(c) > 100:
                hull = cv2.convexHull(c)
                Xbar = int(M["m10"] / M["m00"])  # centroid along x-axis
                Ybar = int(M["m01"] / M["m00"])  # centroid along y-axis
                cv2.circle(frame, (Xbar, Ybar), 5, (0, 0, 255), -1)
                cv2.drawContours(frame, [c], -1, (0, 0, 255), 4)
                # cv2.drawContours(frame, [hull], -1, (0, 255, 0), 4)
                cv2.putText(frame, f"Area: {area:.2f}", (Xbar, Ybar - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for i, hand_handedness in enumerate(results.multi_handedness):
                label = MessageToDict(hand_handedness)['classification'][0]['label']
                pos = (45, 50) if label == 'Left' else (980, 50)
                cv2.putText(frame, label + ' Hand', pos, cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Foreground', frame)

    def camera1(self, cam):
        self.cam = cv2.VideoCapture(cam)
        width, height = self.get_dims(self.cam, self.res)
        self.out = cv2.VideoWriter(self.filename, self.get_video_type(self.filename), self.frame_per_second, (width, height))
        self.initialize_hand_detection()
        while self.cam.isOpened():
            ret, frame = self.cam.read()
            if not ret:
                break
            self.out.write(frame)
            self.process_frame(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 
        self.cam.release()
        self.out.release()
        cv2.destroyAllWindows()
            

    def calculate_percentage_difference(self, area1, area2):
        if area1 == 0 or area2 == 0:  # เพื่อป้องกันการหารด้วย 0
            return 0
        return 100 - (abs(area1 - area2) / max(area1, area2) * 100)

    def compare_areas(self):
        print(f"Max Area Left LED: {self.max_area_left_LED}")
        print(f"Max Area Right LED: {self.max_area_right_LED}")
        print(f"Max Area Left UV: {self.max_area_left_UV}")
        print(f"Max Area Right UV: {self.max_area_right_UV}")

        difference_left = self.calculate_percentage_difference(self.max_area_left_LED, self.max_area_left_UV)
        difference_right = self.calculate_percentage_difference(self.max_area_right_LED, self.max_area_right_UV)

        print(f"Percentage Difference Left: {difference_left:.2f}%")
        print(f"Percentage Difference Right: {difference_right:.2f}%")

    def start_timer(self, minutes, seconds):  # open LED
        total_seconds = minutes * 60 + seconds
        print(f"Timer was set to {minutes} min {seconds} sec")
        start_time = time.time()
        self.LightCondition = 0

        while True:
            elapsed_time = time.time() - start_time
            time_left = max(total_seconds - elapsed_time, 0)
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)
            print(f"time 1 {minutes_left} min {seconds_left} sec", end="\r")

            if elapsed_time >= total_seconds:
                print(f"LightCondition{self.LightCondition}")
                print(f"Max Area Left LED: {self.max_area_left_LED}")
                print(f"Max Area Right LED: {self.max_area_right_LED}")
                print("\nTimer ended")
                break

            if elapsed_time > 9:  # Send command after 5 seconds
                response = self.send_command("a")
                self.Fg_thresh = 110  # Example command
                self.Fg_thresh1 = 255

            time.sleep(1)

    def start_timer1(self, minutes, seconds):
        total_seconds = minutes * 60 + seconds
        print(f"Timer was set to {minutes} min {seconds} sec")
        start_time = time.time()
        self.LightCondition = 2

        while True:
            elapsed_time = time.time() - start_time
            time_left = max(total_seconds - elapsed_time, 0)
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)
            print(f"time 2 {minutes_left} min {seconds_left} sec", end="\r")

            if elapsed_time >= total_seconds:
                print("\nTimer ended")
                break

            if elapsed_time >= 0.1:  # Send command after 1 second
                response = self.send_command("c")
                self.Fg_thresh = 250  # Example command
                self.Fg_thresh1 = 255

            time.sleep(1)

    def start_timer2(self, minutes, seconds):  # open UV blacklight
        total_seconds = minutes * 60 + seconds
        print(f"Timer was set to {minutes} min {seconds} sec")
        start_time = time.time()
        self.LightCondition = 1

        while True:
            elapsed_time = time.time() - start_time
            time_left = max(total_seconds - elapsed_time, 0)
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)
            print(f"time 3 {minutes_left} min {seconds_left} sec", end="\r")

            if elapsed_time >= total_seconds:
                print(f"LightCondition{self.LightCondition}")
                print(f"Max Area Left UV: {self.max_area_left_UV}")
                print(f"Max Area Right UV: {self.max_area_right_UV}")
                print("\nTimer ended")
                self.compare_areas()
                break

            if elapsed_time > 1:  # Send command after 1 second
                response = self.send_command("b")
                self.Fg_thresh = 17  # Example command
                self.Fg_thresh1 = 250

            time.sleep(1)
        
            
if __name__ == '__main__':
    tester = Test()
    tester.Name("hand3.avi", 30, '720p')
    camera_thread = threading.Thread(target=tester.camera1, args=(0,))
    camera_thread.start()

    tester.start_timer(0, 13)
    tester.start_timer1(0, 1)
    tester.start_timer2(0, 13)
