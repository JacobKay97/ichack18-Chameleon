########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import simplejson as json
import numpy as np
import cv2
import time
import serial

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '*INSERT KEY HERE*',
}

params = urllib.parse.urlencode({
})

req = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']


ser = serial.Serial('COM8',9600)

im = cv2.VideoCapture(0)
while(1):

    ret, frame = im.read()
    cv2.imshow('frame',frame)

    #cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    img_str = cv2.imencode('.jpg', frame)[1].tostring()
    body = bytearray(img_str)

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        #print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
    except Exception as e:
        print(e.args)
    ####################################
    if parsed:
        moodvals = []
        for x in req:
            moodvals.append(parsed[0]['scores'][x])

        print(moodvals)
        maxmood = max(moodvals);
        print(maxmood)
        maxmoodindex = [i for i, j in enumerate(moodvals) if j == maxmood]
        print (maxmoodindex)
        maxmood =int(maxmood*100)
        print(maxmood)
        print(req[maxmoodindex[0]])
        towrite = str(maxmoodindex[0]) + ',' + str(maxmood)
        #ser.write(bytearray(maxmoodindex,maxmood))
        ser.write(bytes(towrite,'ASCII'))
        #ser.write(bytes(maxmood))
    time.sleep(0.2)

im.release()
cv2.destroyAllWindows()
ser.close()
