import cv2
import os

class CameraHandler: # ใช้สำหรับการจัดการกล้องและบันทึกวิดีโอ
    def __init__(self, filename, frame_per_second, res): # (ชื่อไฟล์ที่จะบันทึก, อัตราเฟรมต่อวินาทีสำหรับการบันทึกวิดีโอ, ความละเอียดของวิดีโอที่จะบันทึก)
        self.filename = filename
        self.frame_per_second = frame_per_second
        self.res = res
        self.STD_DIMENSIONS = { # ขนาดความละเอียดมาตรฐานสำหรับวิดีโอ
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160),
        }
        self.VIDEO_TYPE = { # เก็บข้อมูลประเภทไฟล์วิดีโอที่ต้องการบันทึก .avi และ .mp4
            'avi': cv2.VideoWriter_fourcc(*'XVID'),
            'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
        self.out = None

    def change_res(self, cap, width, height):
        '''ฟังก์ชันนี้ทำหน้าที่ตั้งค่าความละเอียดของวิดีโอที่ได้จากกล้อง (หรือออบเจ็กต์ VideoCapture)
        โดยการใช้เมธอด set ของ OpenCV VideoCapture เพื่อกำหนดความกว้างและความสูงของเฟรมวิดีโอที่ต้องการ'''
        cap.set(3, width) # cap คือออบเจ็กต์ของ VideoCapture(OpenCV) ที่ได้รับจากการเปิดกล้อง
        cap.set(4, height) # 3:เข้าถึงการตั้งค่าความกว้าง 4:เข้าถึงการตั้งค่าความสูง

    def get_dims(self, cap, res='1080p'): # เปลี่ยนแปลงความละเอียดของเฟรมวิดีโอ
        width, height = self.STD_DIMENSIONS["720p"]
        if res in self.STD_DIMENSIONS:
            width, height = self.STD_DIMENSIONS[res]
        self.change_res(cap, width, height) # ตั้งค่าความกว้างและความสูงของออบเจ็กต์ VideoCapture ตามค่าที่กำหนด
        return width, height

    def get_video_type(self, filename):
        '''ตรวจสอบนามสกุลของไฟล์วิดีโอ (จากชื่อไฟล์) และเลือกประเภทการบันทึกวิดีโอที่เหมาะสมจาก VIDEO_TYPE
           ถ้านามสกุลของไฟล์ตรงกับที่มีใน VIDEO_TYPE จะส่งค่าของประเภทนั้นๆ กลับมา ถ้าไม่ตรงกับประเภทที่รู้จักจะส่งค่าดีฟอลต์เป็น avi'''
        filename, ext = os.path.splitext(filename) # ตัดนามสกุลของไฟล์ออกจากชื่อไฟล์ -> ชื่อไฟล์,นามสกุลไฟล์(ไม่มีจุด) : String 
        if ext in self.VIDEO_TYPE:
            return self.VIDEO_TYPE[ext]
        return self.VIDEO_TYPE['avi']

    def record(self, cam):
        # เปิดกล้องหรืออุปกรณ์การจับภาพที่เชื่อมต่อกับคอม cam คือหมายเลขกล้อง
        self.cam = cv2.VideoCapture(cam)
        
        # เรียกใช้ฟังก์ชัน get_dims เพื่อกำหนดความกว้างและความสูงของเฟรมวิดีโอ
        width, height = self.get_dims(self.cam, self.res)
        
        # สร้างออบเจ็กต์ VideoWriter เพื่อบันทึกวิดีโอ
        # self.filename: ชื่อไฟล์ที่จะบันทึก
        # self.get_video_type(self.filename): ประเภทของไฟล์วิดีโอ (เช่น .avi หรือ .mp4)
        # self.frame_per_second: อัตราเฟรมต่อวินาทีสำหรับการบันทึกวิดีโอ
        # (width, height): ความกว้างและความสูงของเฟรมวิดีโอ
        self.out = cv2.VideoWriter(self.filename, self.get_video_type(self.filename), self.frame_per_second, (width, height))
        
        # ส่งคืนออบเจ็กต์ VideoCapture และ VideoWriter
        return self.cam, self.out

    def release(self):
        self.cam.release() # คืนทรัพยากรที่ถูกใช้ในการเปิดกล้อง
        self.out.release() # คืนทรัพยากรที่ถูกใช้ในการบันทึกวิดีโอ
        cv2.destroyAllWindows() # ปิดหน้าต่างทั้งหมดที่ถูกเปิดด้วย OpenCV
