from ultralytics import YOLO
import cv2
import numpy as np
import easyocr
import math

class LicensePlateDetector:
    def __init__(self, model_path="plate_model.pt"):
        self.model = YOLO(model_path)
        self.labels = ["Embossed", "Provincial", "Regional"]
        self.nepali_ocr = easyocr.Reader(['ne'])
        self.english_ocr = easyocr.Reader(['en'])
        
    def _rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    def _compute_skew(self, src_img):

        if len(src_img.shape) == 3:
            h, w, _ = src_img.shape
        elif len(src_img.shape) == 2:
            h, w = src_img.shape
        else:
            print('upsupported image type')

        img = cv2.medianBlur(src_img, 3)

        edges = cv2.Canny(img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
        lines = cv2.HoughLinesP(edges, 1, math.pi/180, 30, minLineLength=w / 4.0, maxLineGap=h/4.0)
        angle = 0.0
        nlines = lines.size
        cnt = 0
        for x1, y1, x2, y2 in lines[0]:
            ang = np.arctan2(y2 - y1, x2 - x1)
            if math.fabs(ang) <= 30: 
                angle += ang
                cnt += 1

        if cnt == 0:
            return 0.0
        return (angle / cnt)*180/math.pi

    def _deskew(self, src_img):
        return self._rotate_image(src_img, self._compute_skew(src_img))
    
    def _crop_plate(self, image, xyxy):
        x1, y1, x2, y2 = xyxy
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        return image[y1:y2, x1:x2]

        
    def predict(self, image:np.ndarray):
        results = self.model.predict(image)
        for r in results:
            if len(r.boxes) == 0:
                raise Exception("No Plates Detected")
            predictions = {
                "cls" : self.labels[int(r.boxes.cls[0])],
                "conf": float(r.boxes.conf[0])
            }
            break
        cropped_image = self._crop_plate(image, (r.boxes.xyxy.numpy())[0])
        corrected_image = self._deskew(cropped_image)
        blue_channel, green_channel, red_channel = cv2.split(corrected_image)
        if predictions["cls"] == self.labels[0]:
            ocr = self.english_ocr.readtext(blue_channel, paragraph=True)
            ocr_text = ocr[0][-1]
            ocr_text = ocr_text.replace("BAGMATI", "")
            ocr_text= ocr_text.replace("NEP", "")
        else:
            ocr = self.nepali_ocr.readtext(blue_channel, paragraph=True)
            ocr_text = ocr[0][-1]

        ocr_text = ocr_text.replace(" ", "")
        predictions["ocr"] = ocr_text
        
        return predictions
        
            
        
if __name__ == "__main__":
    img = cv2.imread("sample.jpg")
    model = LicensePlateDetector(model_path="plate_model.pt")
    print(model.predict(img))
    
        
        
        
