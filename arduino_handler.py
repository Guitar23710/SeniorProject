import serial
import time

class ArduinoHandler:
    def __init__(self, port='COM3', baudrate=9600):
        # เปิดการเชื่อมต่อกับ Arduino ผ่านพอร์ตที่กำหนด
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    
    # ส่งคำสั่งไปยัง Arduino โดยแปลงคำสั่งเป็นไบต์
    def send_command(self, command): # comand คือคำสั่งที่ต้องการส่งไปยัง Arduino
        self.arduino.write(bytes(command, 'utf-8')) # ส่งคำสั่งไปยัง Arduino โดยแปลงคำสั่งเป็นไบต์ด้วยการเข้ารหัสแบบ UTF-8
        time.sleep(0.05)
        return self.arduino.readline() # อ่านข้อมูลที่ส่งกลับมาจาก Arduino และ return ค่าที่ได้
