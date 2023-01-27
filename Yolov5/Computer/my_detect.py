from models.experimental import attempt_load
from utils.general import non_max_suppression
from models.common import DetectMultiBackend
import torch
import cv2
import numpy as np
from utils.distance import Distance_finder, know_distance,known_width_sign, known_width_traffic_light, stackImages


names = ['speedlimit', 'stop', 'crosswalk', 'trafficlight']
stop_flag = False

#names = ['trafficlight']


colors_random = list(np.random.rand(len(names),3)*255)
colors = {
    'speedlimit':(0,128,255),
    'stop':(0,0,255),
    'crosswalk':(255,0,0),
    'trafficlight':(0,255,0)
}
color_name = ["orange", "red", "blue", "green"]

yolov5_file = r'moje_modele/best_nowe.pt'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = attempt_load(yolov5_file, device=device)

focal_length = 520
yolo_width = 640
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def detect_color(img,Threshold=0.01):
    height, width = img.shape[:2]
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red1 = np.array([170, 70, 50])
    upper_red1 = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

    lower_yellow = np.array([21, 120, 50])
    upper_yellow = np.array([31, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    mask_red = mask0 + mask1 #+ mask2

    rate_red = np.count_nonzero(mask_red) / (height * width)
    
    lower_green = np.array([35, 70, 70])
    upper_green = np.array([70, 255, 255])
    mask3 = cv2.inRange(img_hsv, lower_green, upper_green)

    lower_green1 = np.array([170, 70, 50])
    upper_green1 = np.array([150, 255, 255])
    mask4 = cv2.inRange(img_hsv, lower_green1, upper_green1)
    
    mask_green = mask3 + mask4
    
    rate_green = np.count_nonzero(mask_green) / (height * width)
    
    lower_yellow1 = np.array([170, 120, 50])
    upper_yellow1 = np.array([180, 255, 51])
    mask5 = cv2.inRange(img_hsv, lower_yellow1, upper_yellow1)
    
    mask_yellow = mask2 + mask5
    
    rate_yellow = np.count_nonzero(mask_yellow) / (height * width)

    if rate_red > Threshold:
        return 'red'
    elif rate_green > Threshold:
        return 'green'
    elif rate_yellow > Threshold:
        return 'yellow'
    else:
        return 'nothing'
    # result = cv2.bitwise_and(img, img, mask=mask_red)
    # return result

def object_detection(frame, frame_t):
    global stop_flag
    height, width = frame.shape[:2]
    new_height = int((((yolo_width/width)*height)//32)*32)
    frame = cv2.resize(frame, (yolo_width,new_height))
    img = torch.from_numpy(frame).to(device)
    img = img.permute(2, 0, 1).float().to(device)  
    img /= 255.0  
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, 0.45, 0.45) 
   
    detection_result = []
    crop_img = np.copy(frame_t)
    # crop_res = np.copy(frame_t)
    for i, det in enumerate(pred):
        if len(det): 
            for d in det: 
                x1 = int(d[0].item() * width/yolo_width)
                y1 = int(d[1].item() * height/new_height)
                x2 = int(d[2].item() * width/yolo_width)
                y2 = int(d[3].item()* height/new_height)
                conf = round(d[4].item(), 2)
                c = int(d[5].item())
                traffic_color = ""
                
                object_width = x2 - x1
                if names[c] != 'trafficlight':
                    distance = Distance_finder(known_width_sign, focal_length, object_width)
                    if names[c] == "stop" or names[c] == "crosswalk":
                        stop_flag = True
                    else:
                        stop_flag = False
                else:
                    distance = Distance_finder(known_width_traffic_light, focal_length, object_width)
                    #crop_res = np.copy(frame_t)
                    try:
                        crop_img = crop_img[int(y1):int(y2),int(x1):int(x2),:]
                        #crop_res = detect_red_and_yellow(crop_img, 0.15)
                        if detect_color(crop_img, 0.30) == 'red':
                            traffic_color = "Red"
                            stop_flag = True
                            # print("Red")
                        elif detect_color(crop_img, 0.30) == 'green':
                            traffic_color = "Green"
                            # print("Green")
                            stop_flag = False
                        elif detect_color(crop_img, 0.30) == 'yellow':
                            traffic_color = 'Yellow'
                            # print("Yellow")
                        else:
                            traffic_color = 'No color'
                            #print("Traffic with no color")
                        frame_t = cv2.putText(frame_t, f'Traffic color: {traffic_color}', (x2, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1, cv2.LINE_AA) 
                    except:
                        None
                        #print("Unable to crop Image")
                
                detected_name = names[c]
                # if stop_flag:
                #     print("STOP")

                # print(f'Detected: {detected_name} conf: {conf}  bbox: x1:{x1}    y1:{y1}    x2:{x2}    y2:{y2}')
                detection_result.append([x1, y1, x2, y2, conf, names[c], color_name[c]])
                
                frame_t = cv2.rectangle(frame_t, (x1, y1), (x2, y2), colors[names[c]], 1) # box
                frame_t = cv2.putText(frame_t, f'{names[c]} {str(conf)}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[names[c]], 1, cv2.LINE_AA)
                frame_t = cv2.putText(frame_t, f'Distance: {round(distance,2)}', (x1, y2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[names[c]], 1, cv2.LINE_AA) 
                

    return frame_t, detection_result, crop_img

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    
    while True:
        ret,frame = cap.read()
        frame_c = np.copy(frame)
        result, box, crop = object_detection(frame_c, frame)
        
        result_stack = stackImages(0.5, [result, crop])
        cv2.imshow("Result", result_stack)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
