import threading
import cv2
from camera_handler import CameraHandler
from hand_processing import HandProcessing
from arduino_handler import ArduinoHandler
from light_control import LightControl

if __name__ == '__main__':
    # สร้าง object
    camera = CameraHandler('hand.avi', 30, '1080p')
    hand_proc = HandProcessing()
    arduino = ArduinoHandler()
    light_ctrl = LightControl(arduino)


    # Start camera
    cam, out = camera.record(1)
    hand_proc.initialize_hand_detection()

    def camera_loop():
        while cam.isOpened():
            # รูปภาพ(เฟรม)
            ret, frame = cam.read() # read return -> ret: ค่าบูลีน (True:อ่านเฟรมสำเร็จ หรือ False:อ่านเฟรมไม่สำเร็จ),frame -> เฟรมภาพเป็น array
            if not ret: # อ่านเฟรมไม่สำเร็จออกจาก loop (False)
                break
            out.write(frame) # เขียนเฟรมภาพแต่ละเฟรมลงในไฟล์วิดีโอที่จะบันทึกเก็บไว้

            '''เรียกใช้กระบวนการประมวลผลหาพื้นที่ของมือ'''
            hand_proc.process_frame(frame, light_ctrl.LightCondition, light_ctrl.Fg_thresh, light_ctrl.Fg_thresh1)
            
            '''หากผู้ใช้กดปุ่ม 'q' ลูปจะหยุดทำงาน -> ปิดกล้อง'''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        camera.release() # คืน memory และปิดทุกอย่างที่เปิดด้วย OpenCV

    '''สร้าง thread ใหม่โดยใช้โมดูล threading ของ Python เพื่อรันฟังก์ชัน camera_loop ในเธรดแยก,
    ใช้เธรดเพื่อจับภาพจากกล้องและบันทึกลงไฟล์วิดีโอในขณะที่ยังสามารถควบคุมแสงและทำการประมวลผลภาพได้พร้อมกัน'''
    camera_thread = threading.Thread(target=camera_loop)
    camera_thread.start() # เริ่มต้นรันฟังก์ชัน camera_loop ในเธรดแยก

    # เริ่มจับเวลาสำหรับการเปิดปิดแส(LED, UV)
    light_ctrl.start_timer(0, 13, 0)  # LED
    light_ctrl.start_timer1(0, 1)     # Delay
    light_ctrl.start_timer2(0, 13)    # UV

    '''เธรดนี้จะทำงานแยกจากโปรแกรมหลัก โดยจะทำการจับภาพจากกล้องและประมวลผลเฟรมในฟังก์ชัน camera_loop 
    ในขณะเดียวกัน โปรแกรมหลักจะดำเนินการต่อไปยังการเริ่มต้นจับเวลาและการควบคุมแสง'''
    camera_thread.join() # เมื่อเรียกใช้ join() โปรแกรมหลักจะหยุดรอจนกว่าเธรด camera_thread จะทำงานเสร็จ