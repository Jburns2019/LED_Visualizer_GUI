#include <SoftwareSerial.h>
#include "headerFile.h"
SoftwareSerial btConnection(5, 6); // RX, TX. Arduino digital PWM pins are 3, 5, 6, 9, 10, 11

int SER = 11;      // serial data to rows
int RCLK = 12;     // storage register clock
int SRCLK = 13;    // shift register clock for serial input
int GNDRCLK = 8;
int GNDSER = 9;
int GNDSRCLK = 10;

unsigned long t = 0;

int arr[15];

byte val_lsb;
byte val_msb;
uint16_t value;
unsigned long t1, t2, t3, t4;
int count;

int btReceived = 0;
uint16_t animationLength;
unsigned long animationSpeed;

void setup() {

  /* Set pins to correct setting */
  pinMode(SER, OUTPUT);
  pinMode(RCLK, OUTPUT);
  pinMode(SRCLK, OUTPUT);
  pinMode(GNDSER, OUTPUT);
  pinMode(GNDRCLK, OUTPUT);
  pinMode(GNDSRCLK, OUTPUT);

  Serial.begin(9600);
  btConnection.begin(9600);
}


void loop() {

  /* Ground the LED for the first cycle */
  count = 0;
  do {
    if (btConnection.available() > 0) {
      btReceived = btConnection.read() - 48; // 48 is character '0'
      count = 0;
    }
    if (Serial.available() > 0) {
      btReceived = Serial.read() - 48;
      count = 0;
    }
    if (count == 0 && (btReceived < 0 || btReceived > 5)) {
      btConnection.println("\nYou entered an invalid animation number");
      count++;
    }
  } while (btReceived < 0 || btReceived > 5);
  //btReceived = 3;
  switch (btReceived) {
    case 0:
      colorCycle();
      break;

    case 1:
      changeLayers();
      break;

    case 2:
      swirl();
      break;

    case 3:
    case 4:
    case 5:
      customAnimation(btReceived - 3);
      break;
  }
}

void customAnimation(int btValue) {
  animationLength = pgm_read_word(&customLengths[btValue]);
  animationSpeed = pgm_read_dword(&customSpeeds[btValue]);

  for (int i = 0; i < animationLength; i++) { // for each animation frame

    //for (int k = 0; k < animationSpeed; k++) { // slow the animation down by repeating the same frame
    t1 = micros();
    while ((micros() - t1) < animationSpeed) { // slow the animation down by repeating the same frame
      resetGND();
      for (int j = 0; j < 35; j++) { // for each row

        
        /*
            Running nextRow() right before the next pushArr function ensures
            that the 2nd color from the previous row will be on during the
            time-comsuming Serial.read() functions, meaning that the two
            colors will be on for equal time intervals. However, it should
            only run this after the first iteration, or else the 1st row will
            only be grounded for one of its colors.
        */
        

        pushBlankArr();
        if (j != 0)
          nextRow();
          
        value = pgm_read_word(&colorArr[btValue][0][i][j]);

        num2arr(arr, value);
        pushArr(arr);

        //while ((micros() - t1) < 200) {}
        /* Read and combine the bytes, then display them */
        //t1 = micros();
        value = pgm_read_word(&colorArr[btValue][1][i][j]);
        num2arr(arr, value);
        pushArr(arr);
      }
      pushBlankArr();
    }
  }
}

void colorCycle() {
  uint16_t colors[6] = {18724, 28086, 9362, 14043, 4681, 23405}; // rainbow colors
  for (int frame = 0; frame < 6; frame++) {
    value = colors[frame];
    num2arr(arr, value);
    for (int repeat = 0; repeat < 500; repeat++) {
      //t1 = micros();
      resetGND();
      for (int row = 0; row < 35; row++) {
        if (row != 0)
          nextRow();
        pushArr(arr);
      }
      nextRow();
      //t2 = micros();
      //Serial.println(t2 - t1);
    }
  }
}

void changeLayers() {
  uint16_t white = 32767;
  for (int frame = 0; frame < 7; frame++) { // for each layer
    for (int repeat = 0; repeat < 100; repeat++) {
      //t1 = micros();
      resetGND();
      for (int row = 0; row < 35; row++) {
        pushBlankArr();
        if (row != 0)
          nextRow();

        if (row < (frame + 1) * 5 && row >= frame * 5) {
          num2arr(arr, white);
          pushArr2(arr);
        }
        else {
          value = 0;
          num2arr(arr, value);
          pushArr2(arr);
        }
      }
      pushBlankArr();
    }
  }
}

void swirl() {
  for (int frame = 0; frame < 16; frame++) {
    for (int repeat = 0; repeat < 50; repeat++) {
      t1 = micros();
      value = 0;
      num2arr(arr, value);
      pushArr(arr);
      resetGND();
      for (int layer = 0; layer < 7; layer++) {
        for (int row = 0; row < 5; row++) {
          if (frame < 5 && row == frame) { // front part
            value = 7;
          }
          else if (frame < 9 && frame > 4 && row == 4) { // one side
            value = 7 * (1 << (3 * (frame - 4)));
          }
          else if (frame < 13 && frame > 8 && row == 12 - frame) { // back part
            value = 28672;
          }
          else if (frame > 12 && row == 0) {
            value = 7 * (1 << (3 * (16 - frame))); // second side
          }
          else {
            value = 0;
          }

          if (row != 0 || layer != 0) {
            pushBlankArr();
            nextRow();
          }
          num2arr(arr, value);

          while (micros() - t1 < 150) {}

          pushArr(arr);
        }
      }
      //      t2 = micros();
      //      Serial.println(t2 - t1);
    }
  }
}

void resetGND() {
  /*
      This function sets all the first ground pin LOW and the rest
      to HIGH, preparing the cube for another frame.
  */
  digitalWrite(GNDRCLK, LOW);
  digitalWrite(GNDSER, HIGH); // HIGH values
  for (int i = 0; i < 34; i++) { // Cycle ground serial clock 34 times
    digitalWrite(GNDSRCLK, LOW);
    delayMicroseconds(1);
    digitalWrite(GNDSRCLK, HIGH);
    delayMicroseconds(1);
  }
  /* Push one LOW value */
  digitalWrite(GNDSER, LOW);
  digitalWrite(GNDSRCLK, LOW); // Cycle ground serial clock once
  delayMicroseconds(1);
  digitalWrite(GNDSRCLK, HIGH);
  delayMicroseconds(1);

  digitalWrite(GNDRCLK, HIGH); // Push output values through storage registers
}


void nextRow() {
  /* This function cycles the ground clock, moving the program to the next row */
  digitalWrite(GNDSRCLK, LOW); // shift register clock low
  digitalWrite(GNDSER, HIGH);
  delayMicroseconds(1);
  digitalWrite(GNDRCLK, LOW); // storage register clock low
  digitalWrite(GNDSRCLK, HIGH); // cycle shift registers
  delayMicroseconds(1);
  digitalWrite(GNDRCLK, HIGH); // update output through storage registers
}

void nextRow_bitManipulation() {
  PORTB = B00111011;
  delayMicroseconds(1);
  PORTB = B00111110;
  delayMicroseconds(1);
  PORTB = B00111111;
}


void pushArr(int arr[15]) {
  /*
      This function pushes all 15 bits from the input array into the shift
      registers and then cycles the register clock, updating the color pins
      on the cube.
  */
  bitClear(PORTB, 4);
  t = micros();

  /* Feed the array into the shift registers 'backwards' and cycle the clock */
  for (int i = 14; i >= 0; i--) {

    PORTB = B00000111;
    if (arr[i] == 0) {
      PORTB = B00000111;
      delayMicroseconds(1);
      PORTB = B00100111;
    }
    else {
      PORTB = B00001111;
      delayMicroseconds(1);
      PORTB = B00101111;
    }
    delayMicroseconds(1);
  }
  bitSet(PORTB, 4);
}

void pushArr1(int arr[15]) {
  /*
      This function pushes all 15 bits from the input array into the shift
      registers and then cycles the register clock, updating the color pins
      on the cube.
  */
  digitalWrite(RCLK, LOW);
  t = micros();

  /* Feed the array into the shift registers 'backwards' and cycle the clock */
  for (int i = 14; i >= 0; i--) {
    digitalWrite(SRCLK, LOW);
    if (arr[i] == 0)
      digitalWrite(SER, LOW);
    else
      digitalWrite(SER, HIGH);
    delayMicroseconds(1);
    digitalWrite(SRCLK, HIGH);
    delayMicroseconds(1);
  }
  while ((micros() - t) < 234) {}
  digitalWrite(RCLK, HIGH);
}

void pushArr2(int arr[15]) {
  /*
      This function pushes all 15 bits from the input array into the shift
      registers and then cycles the register clock, updating the color pins
      on the cube.
  */
  bitClear(PORTB, 4);
  t = micros();

  /* Feed the array into the shift registers 'backwards' and cycle the clock */
  for (int i = 14; i >= 0; i--) {

    PORTB = B00000110;
    if (arr[i] == 0) {
      PORTB = B00000110;
      delayMicroseconds(1);
      PORTB = B00100110;
      delayMicroseconds(1);
      PORTB = B00110111;
    }
    else {
      PORTB = B00001110;
      delayMicroseconds(1);
      PORTB = B00101110;
      delayMicroseconds(1);
      PORTB = B00111111;
    }
    delayMicroseconds(1);
  }
  //bitSet(PORTB, 4);
}

void pushBlankArr(){
  /*
  This function simply pushes a blank array to the color pins. This
  is needed to prevent colors from 'bleeding' into adjacent rows
  because when the ground is switched, any remaining color will show
  up before the next color is sent.
  */
  num2arr(arr, 0);
  pushArr(arr);
}

void num2arr(int arr1[15], uint16_t value) {
  /*
     This function converts the value into an array of length 15,
     in which every value is a 0 or 1. It does so by converting
     the value to binary
  */
  for (int i = 0; i < 15; i++) {
    //arr1[i] = value % 2;
    arr1[i] = value - ((value >> 1) << 1);
    value = value >> 1;
  }
}
