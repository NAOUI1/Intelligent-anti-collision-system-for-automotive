# install opencv "pip install opencv-python"
import cv2
import RPi.GPIO as GPIO
import time

buzzer_pin=40
GPIO.setup(buzzer_pin,GPIO.OUT)

display = drivers.Lcd()

###################### commande de robot ###############################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

def back():
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,False)
    GPIO.output(15,True)
def forward():
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,True)
    GPIO.output(15,False)
def right():
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,True)
def left():
    GPIO.output(7,False)
    GPIO.output(11,True)
    GPIO.output(13,True)
    GPIO.output(15,False)
def stop():
    GPIO.output(7,False)
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)
# distance from camera to object(face) measured
# centimeter
Known_distance = 300.2

# width of face in the real world or Object Plane
# centimeter
Known_width = 85.3

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

# face detector object
face_detector = cv2.CascadeClassifier("pedestrian.xml")

# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):

    distance = (real_face_width * Focal_Length)/face_width_in_frame

    # return the distance
    return distance


def face_data(image):

    face_width = 0 # making face width to zero

    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.2, 4)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in faces:

        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)

        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width


# reading reference_image from directory
ref_image = cv2.imread("sa.png")

# find the face width(pixels) in the reference_image
ref_image_face_width = face_data(ref_image)

# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)

print(Focal_length_found)

# show the reference image
cv2.imshow("ref_image", ref_image)

# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(0)

# looping through frame, incoming from
# camera/video
while True:

    # reading the frame from camera
    _, frame = cap.read()

    # calling face_data function to find
    # the width of face(pixels) in the frame
    face_width_in_frame = face_data(frame)

    # check if the face is zero then not
    # find the distance
    if face_width_in_frame != 0:
    
        # finding the distance by calling function
        # Distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)

        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)q 

        # Drawing Text on the screen
        cv2.putText(
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),
        fonts, 0.6, GREEN, 2)
        while D>=500:
            
            GPIO.output(buzzer_pin, False)
            forward()
            display.lcd_display_string("systeme anticollision",1)
            display.lcd_display_string("Ds="+str(Ds)+"cm",2)
            display.lcd_clear()
        while D<500:
            
            GPIO.output(buzzer_pin, True)
            forward()
            display.lcd_display_string("attension",1)
            display.lcd_display_string("Ds="+str(Ds)+"cm",2)
            display.lcd_clear()
        while D<=400 :
            
            GPIO.output(buzzer_pin, True)
            stop()
            display.lcd_display_string("freinage automatique est activé",1)
            display.lcd_display_string("Dd="+str(Dd)+"cm",2)
            display.lcd_clear()

    # show the frame on the screen
    cv2.imshow("frame", frame)

    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# closing the camera
cap.release()

# closing the the windows that are opened
cv2.destroyAllWindows()



