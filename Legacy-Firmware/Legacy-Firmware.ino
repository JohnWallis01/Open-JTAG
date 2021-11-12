#define BAUD 0
#define DRLENGTH 288



//TMS D8 PB0
//TDI D9 PB1
//TDO D10 == input PB2
//TCK D11 PB3

int Set_TMS(int value) {
  _delay_us(BAUD);
  if (value) {
    PORTB = PORTB | 0x01; //set to 1
  }
  else{
    PORTB = PORTB &  0xFE; //set to 0
  }
  return 0;
}

int Set_TDI(int value) {
  _delay_us(BAUD);
  if (value) {
    PORTB = PORTB | 0x02; //set to 1
  }
  else{
    PORTB = PORTB &  0xFD; //set to 0
  }
  return 0;
}

int Set_TCK(int value) {
  _delay_us(BAUD);
  if (value) {
    PORTB = PORTB | 0x08; //set to 1
  }
  else{
    PORTB = PORTB &  0xF7; //set to 0
  }
  return 0;
}


int JTAG_Reset() {
  //reset the jtag state
  Set_TMS(1);
  Set_TCK(0);
  int i = 0;
  for (i = 0; i < 5; i++) {
    Set_TCK(1);
    Set_TCK(0);
  }
}



int Set_Instruction(int instruction[]) {

  JTAG_Reset();


//move into the shit ir state

  //go to RUN-TEST
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);
  //go to SELECT-DR-SCAN
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);
  //go to SELECT-IR-SCAN
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);
  //go to CAPTURE-IR
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);
  //go to SHIFT-IR
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);

  //shift in the instruction
    int i;
  for (i = 0; i < 9; i++) {
    Set_TDI(instruction[i]);
    Set_TCK(1);
    Set_TCK(0);
  }

  //go to EXIT1-IR
  Set_TDI(instruction[9]);
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);

  //go to UPDATE-IR
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);

  //go to RUN-TEST
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);

  return 0;



}

int Set_Data(int data[]) {

//assume this is in the run test state

  //go to SELECT-DR-SCAN
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);
  //go to CAPTURE-DR
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);
  //go to SHIFT-DR
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);

  //shift in the data
  int i;
  for (i = 0; i < DRLENGTH - 1; i++) {
    Set_TDI(data[i]);
    Set_TCK(1);
    Set_TCK(0);
  }

  //go to EXIT1-DR
  Set_TDI(data[DRLENGTH]);
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);

  //go to UPDATE-DR
  Set_TMS(1);
  Set_TCK(1);
  Set_TCK(0);

  //go to RUN-TEST
  Set_TMS(0);
  Set_TCK(1);
  Set_TCK(0);

  return 0;
}


int Ready_EXTEST() {
  int extest[] = {0,0,0,0,0,0,0,0,0,0};
  //initalise the ports
  DDRB = 0x2B;
  //turn on LED
  PORTB = PORTB | 0x20;


  Set_Instruction(extest);


  return 0;
}



int writes_n = 0;
int shift_state = 0;
int DataDr[288];

void setup() {
  Ready_EXTEST();
  Serial.begin(57600);
  Serial.setTimeout(1);
//  Serial.println("System is in Extest");
}

void loop() {
  while (!Serial.available());
  byte data = Serial.read();
  if (data == 0x32) {
   Ready_EXTEST();
   Serial.print("E");
  }
  if (data == 0x33) {
    JTAG_Reset();
    Serial.print("Q");
  }
  if(data == 0x31) {
//    Serial.println("Scanned 1");
    DataDr[shift_state] = 1;
    shift_state++;
    Serial.print("1");
  }
  if(data == 0x30) {
//    Serial.println("Scanned 0");
    DataDr[shift_state] = 0;
    shift_state++;
    Serial.print("0");
  }

  if (shift_state == 288) {
//    Serial.println("Attempting a Datashift");
    Set_Data(DataDr);
    shift_state = 0;
    writes_n ++;
//    Serial.println("Success");
  }
  data == 0x00;
}
