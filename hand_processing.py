import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

# contour = ขอบของวัตถุ
class HandProcessing:
    def __init__(self):
        self.handmp = mp.solutions.hands # สร้างออบเจ็กต์สำหรับการตรวจจับมือจาก Mediapipe, โมดูลใน Mediapipe ที่มีฟังก์ชันและคลาสสำหรับการตรวจจับมือ
        self.hands = None
        self.max_area_left_LED = 0
        self.max_area_right_LED = 0
        self.max_area_left_UV = 0
        self.max_area_right_UV = 0

    def initialize_hand_detection(self):
        # กำหนดค่าการตรวจจับมือ
        # สร้างออบเจ็กต์ Hands จากโมดูล hands ของ Mediapipe และกำหนดค่าพารามิเตอร์ต่างๆ สำหรับการตรวจจับมือ
        self.hands = self.handmp.Hands(
            static_image_mode=False, # กำหนดให้การตรวจจับมือทำงานในโหมดวิดีโอ (ไม่ใช่ภาพนิ่ง)
            model_complexity=1, # กำหนดความซับซ้อนของโมเดลที่ใช้ในการตรวจจับมือ ค่า 1 หมายถึงใช้โมเดลที่มีความซับซ้อนปานกลาง
            # 1 คือสมดุลระหว่างความเร็วและความแม่นยำ (0 1 2)

            min_detection_confidence=0.75, # กำหนดค่าความมั่นใจขั้นต่ำในการตรวจจับมือ ถ้าค่าความมั่นใจต่ำกว่าค่านี้จะไม่ถือว่ามีการตรวจจับมือ
            min_tracking_confidence=0.75, # การตั้งค่าค่านี้ให้เหมาะสมจะช่วยให้การติดตามมือมีความแม่นยำและเสถียรมากขึ้น 
            # โดยเฉพาะในสถานการณ์ที่มีการเคลื่อนไหวของมืออย่างรวดเร็วหรือมีการเปลี่ยนแปลงของแสง

            max_num_hands=2 # กำหนดจำนวนมือสูงสุดที่สามารถตรวจจับได้ในแต่ละครั้ง 
        )

    def process_frame(self, frame, LightCondition, Fg_thresh, Fg_thresh1):
        # หมุนเฟรม 180 องศา
        frame = cv2.rotate(frame,cv2.ROTATE_180)

        # วาดเส้นแบ่งกลางเฟรม
        frame = cv2.line(frame, (640, 0), (640, 720), (0, 255, 0), 5)

        '''แปลงภาพจาก BGR color space เป็น LAB color space -> L (Lightness), A (สีแดง-เขียว), และ B (สีเหลือง-น้ำเงิน)
        การแปลงภาพไปยัง LAB color space สามารถช่วยในการประมวลผลภาพที่ต้องการความแม่นยำในการแยกสี'''
        ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        '''ใช้ในการเบลอภาพ,ImageLAB[:, :, 0]: เลือกช่องสี L (Lightness) จากภาพใน LAB color space '''
        blur = cv2.GaussianBlur(ImageLAB[:, :, 0], (3, 3), 0)
        
        '''การทำ threshold จะช่วยแยกวัตถุที่มีความสว่างมากกว่าค่า threshold ออกจากพื้นหลัง, Fg_thresh: ค่าพิกเซลต่ำกว่าค่า threshold นี้ จะ map เป็น 0,
        Fg_thresh1: ค่าที่พิกเซลจะถูกตั้งค่าเมื่อเกินค่า threshold'''
        _, Fg_thresh = cv2.threshold(blur, Fg_thresh, Fg_thresh1 , cv2.THRESH_BINARY)
        
        '''ค้นหา contours ในภาพ, ใช้ในการระบุขอบของมือในภาพ'''
        FgHand_contours, hierarchy = cv2.findContours(Fg_thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # FgHand_contours จะรับค่าเป็นอาเรย์ของจุดพิกเซล (x, y)

        '''ทำการประมวลผล contours ที่พบในภาพเพื่อคำนวณพื้นที่ของมือและจัดเก็บค่าพื้นที่สูงสุดในแต่ละฝั่ง (ซ้ายและขวา) ตามสถานะของแสง (LightCondition)'''
        sumArea = 0
        for c in FgHand_contours:
            area = cv2.contourArea(c)
            # การคำนวณพื้นที่ของคอนทัวร์: พิจารณาเฉพาะคอนทัวร์ที่มีพื้นที่มากกว่า 1000
            if area > 1000:
                sumArea += area
            
            # การคำนวณโมเมนต์: ใช้ในการหาจุดศูนย์กลางของ contour
            M = cv2.moments(c) # ซึ่งโมเมนต์เป็นค่าทางคณิตศาสตร์ที่ใช้ในการหาคุณสมบัติต่างๆ ของรูปร่าง เช่น พื้นที่ จุดศูนย์กลาง
            '''m00: พื้นที่ของคอนทัวร์, m10, m01: โมเมนต์ที่ใช้ในการคำนวณจุดศูนย์กลาง'''
            if M["m00"] == 0: # พื้นที่ของ contour เป็น 0 จะข้าม contour นี้ไป
                continue
            cx = M["m10"] / M["m00"] # คำนวณจุดศูนย์กลางในแนวนอน (cx), cy = m01/m00
            '''ถ้ามี contour สองอันที่ไม่ติดกัน มันจะทำการ return ค่า cx ออกมาสองค่า'''
            if LightCondition == 0: # คำนวณพื้นที่มือขณะเปิด LED
                if cx < 640:
                    self.max_area_left_LED = max(self.max_area_left_LED, sumArea)
                else:
                    self.max_area_right_LED = max(self.max_area_right_LED, sumArea)
            elif LightCondition == 1: # คำนวณพื้นที่มือขณะเปิด UV
                if cx < 640:
                    self.max_area_left_UV = max(self.max_area_left_UV, sumArea)
                else:
                    self.max_area_right_UV = max(self.max_area_right_UV, sumArea)

            if len(c) > 100: # ตรวจสอบและประมวลผลคอนทัวร์ที่มีความยาวมากกว่า 100
                # ฟังก์ชัน cv2.convexHull(c) ใน OpenCV จะคืนค่าเป็นคอนทัวร์ใหม่ ที่ครอบคลุมคอนทัวร์เดิมทั้งหมด(รูปหลายเหลี่ยม)
                hull = cv2.convexHull(c) 

                # คำนวณจุดศูนย์กลางในแนวนอน (Xbar) และแนวตั้ง (Ybar)
                Xbar = int(M["m10"] / M["m00"])
                Ybar = int(M["m01"] / M["m00"])

                cv2.circle(frame, (Xbar, Ybar), 5, (0, 0, 255), -1) # วาดจุดบนศูนย์กลาง
                cv2.drawContours(frame, [c], -1, (0, 0, 255), 4) # วาดเส้นขอบมือสีแดง
                cv2.drawContours(frame, [hull], -1, (0, 255, 0), 4) # วาดเส้นรอบมือสีเขียว ซึ่งเป็นรูปหลายเหลี่ยมที่ครอบคลุมมือทั้งหมด
                # แสดงข้อความบนภาพ
                cv2.putText(frame, f"Area: {area:.2f}", (Xbar, Ybar - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # แปลง BGR to RGB
        
        # self.hands = self.handmp.Hands in initialize_hand_detection function
        '''ประมวลผลภาพ frame_rgb ด้วยโมเดลการตรวจจับมือจาก Mediapipe
        return ค่าเป็น object ออกมา, multi_hand_landmarks: พิกัด x, y, z ที่แสดงตำแหน่งของจุดบนมือ(List)'''
        results = self.hands.process(frame_rgb) # create object from initialize_hand_detection function

        '''multi_handedness: ลิสต์ของข้อมูลเกี่ยวกับมือซ้ายหรือมือขวา, 
        [{"classification": [{"index": 0,"score": 0.95,"label": "Left"}]},
        {"classification": [{"index": 1,"score": 0.90,"label": "Right"}]}]'''
        
        if results.multi_hand_landmarks:
            for i, hand_handedness in enumerate(results.multi_handedness):

                # แปลงออบเจ็กต์ hand_handedness ให้เป็น dic ก่อนโดยใช้ฟังก์ชัน MessageToDict
                label = MessageToDict(hand_handedness)['classification'][0]['label']
                
                # กำหนดตำแหน่งของข้อความบนภาพ (ซ้ายหรือขวา)
                pos = (45, 50) if label == 'Left' else (980, 50)
                
                # แสดงข้อความบนภาพ
                cv2.putText(frame, label + ' Hand', pos, cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Foreground', frame)
