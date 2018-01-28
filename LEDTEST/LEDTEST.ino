#include <Adafruit_NeoPixel.h>
#define PIN 6

int colours[8][3]={{204, 0, 0},{191,0,151},{171, 9, 36},{0,204,0},{150,125,0},{200,200,200},{25,25,240},{0, 125, 53}};

/*anger: red
"contempt": reddy purple
"disgust": pink
"fear": green
"happiness": light yellow,
"neutral": white
"sadness": blue
"surprise: teal*/

Adafruit_NeoPixel strip = Adafruit_NeoPixel(150, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // declare the ledPin as an OUTPUT:
  strip.begin();
  strip.clear();
  strip.show();
  Serial.begin(9600);
  Serial.print("Ready");
}

void loop() {
  if (Serial.available() >= 4) {
    int colour = Serial.parseInt();
    int strength = Serial.parseInt();
    Serial.print("Rx");
    Serial.print(colour);
    Serial.print(":");
    Serial.print(strength);
    Serial.print('\n');

    int r = strength*colours[colour][0] /100;
    int g = strength*colours[colour][1] /100;
    int b = strength*colours[colour][2] /100;

    for (int i=0; i <= 86; i++){
      strip.setPixelColor(i,r,g,b);
    }
    int brightness = (200*strength)/brightness;
    strip.setBrightness(brightness);
    strip.show();
  }
}
