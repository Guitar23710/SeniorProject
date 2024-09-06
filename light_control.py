import time

class LightControl:
    def __init__(self, arduino_handler):
        # รับออบเจ็กต์ ArduinoHandler เพื่อใช้ในการส่งคำสั่งไปยัง Arduino
        self.arduino_handler = arduino_handler
        self.LightCondition = 0 # สถานะของแสง (0:LED, 1:UV)
        self.Fg_thresh = 115 # threshold เริ่มต้น
        self.Fg_thresh1 = 255 # threshold เริ่มต้น

    def send_command(self, command):
        # ส่งคำสั่งไปยัง Arduino ผ่าน ArduinoHandler
        return self.arduino_handler.send_command(command)

    def start_timer(self, minutes, seconds, LightCondition): # คำนวณเวลาทั้งหมดในหน่วยวินาที
        total_seconds = minutes * 60 + seconds
        print(f"Timer set to {minutes} min {seconds} sec")
        start_time = time.time() # บันทึกเวลาเริ่มต้น
        self.LightCondition = LightCondition

        while True:
            # คำนวณเวลาที่ผ่านไป
            elapsed_time = time.time() - start_time
            # คำนวณเวลาที่เหลือ
            time_left = max(total_seconds - elapsed_time, 0)
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)
            print(f"time {LightCondition} {minutes_left} min {seconds_left} sec", end="\r")

            # ถ้าเวลาที่ผ่านไปมากกว่าหรือเท่ากับเวลาที่ตั้งไว้ ให้หยุดการทำงานของ timer
            if elapsed_time >= total_seconds:
                print("\nTimer ended")
                break
            
            # ถ้าเวลาที่ผ่านไปมากกว่า 1 วินาที ให้ส่งคำสั่งไปยัง Arduino
            if elapsed_time > 1:
                command = 'a' if LightCondition == 0 else 'b'
                response = self.send_command(command)

                # ปรับค่า threshold ตามสถานะของแสง
                self.Fg_thresh = 110 if LightCondition == 0 else 17
                self.Fg_thresh1 = 255 if LightCondition == 0 else 250

            time.sleep(1)
