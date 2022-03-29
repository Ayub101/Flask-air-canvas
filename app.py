from flask import Flask,render_template,Response,request
import cv2
import HandMotion as hm
import ColorDetect as dt
import numpy as np


app=Flask(__name__)
camera=cv2.VideoCapture(1)
pen = dt.Pen()
htm = hm.handTraking()
color = {"Green":(0,255,0),"White":(255,255,255),"Orange":(0,140,255),
        "LightBlue":(255,255,0),"Blue":(255,0,0),"Yellow":(0,255,255)
        ,"Red":(0,0,255)}
selected_color = "Green"
selected_size = 2

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            canvas = pen.write(frame,color[selected_color],int(selected_size))
            result = htm.trakHands(cam=camera,frame=frame)
            frame = result.get('frame')
            [x,y] = result.get('erase')
            pen.erase(canvas,x,y)
            frame = cv2.add(canvas,frame)
            frame = np.hstack((frame,canvas))
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global selected_color
        selected_color =request.form.get('color', '')
        global selected_size
        selected_size=  int(request.form.get('size',''))
        return render_template('index.html',color=selected_color,size=selected_size )
    return render_template('index.html',color=selected_color,size=selected_size)

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="main_":
    app.run(debug=True)