//pin definitions
#define TMS 8
#define TDI 9
#define TDO 10
#define TCK 11

//device config stuff
#define FREQUENCY 1e3 //1khz data transfer
#define BAUDRATE 57600

//jtag state definitions
#define JTAG_RESET 0
#define JTAG_IDLE 1

#define JTAG_SELECT_DR 2
#define JTAG_CAPTURE_DR 3
#define JTAG_SHIFT_DR 4
#define JTAG_EXIT1_DR 5
#define JTAG_PAUSE_DR 6
#define JTAG_EXIT2_DR 7
#define JTAG_UPDATE_DR 8

#define JTAG_SELECT_IR 9
#define JTAG_CAPTURE_IR 10
#define JTAG_SHIFT_IR 11
#define JTAG_EXIT1_IR 12
#define JTAG_PAUSE_IR 13
#define JTAG_EXIT2_IR 14
#define JTAG_UPDATE_IR 15

//program state definintions


//lookup table for JTAG state transitions.
//value = current state + target state * 16 also note that 0xFFFF will be a do nothing transistion,
//first nible stores number of transistion, next 3 nibles store the transition map (least significnat bit first)
//maybe add the standby information on the diagnonal of the transisiton talbe
                                                                  //reset   idle    drSel   drCap   drShift drEx1   drPus   drEx2   drUp    irSel   irCap   irShift irEx1   irPus   irEx2   irUp
const unsigned short Transfer_Table[256] PROGMEM = /* reset */     {0x0000, 0x1000, 0x2002, 0x3002, 0x4002, 0x400A, 0x500A, 0x5002, 0x501A, 0x3006, 0x4006, 0x5006, 0x5016, 0x6016, 0x6006, 0x6036,
                                                  /* idle */        0x3007, 0x0000, 0x1001, 0x2001, 0x3001, 0x3006, 0x4006, 0x4001, 0x400D, 0x2003, 0x3003, 0x4003, 0x400B, 0x500B, 0x5003, 0x501B,
                                                  /* drSel */       0x3003, 0x400B, 0x0000, 0x1000, 0x2000, 0x2002, 0x3002, 0x3000, 0x3006, 0x1001, 0x2001, 0x3001, 0x3005, 0x4005, 0x4001, 0x400D,
                                                  /* drCap */       0x501A, 0x3003, 0x400F, 0x0000, 0x1000, 0x1001, 0x2001, 0x2000, 0x2003, 0x400F, 0x500F, 0x600F, 0x602F, 0x700F, 0x700F, 0x706F,
                                                  /* drShift */     
                                                  /* drEx1 */
                                                  /* drPus */
                                                  /* drEx2 */
                                                  /* drUp */
                                                  /* irSel */
                                                  /* irCap */
                                                  /* irShift */
                                                  /* irEx1 */
                                                  /* irPus */
                                                  /* irEx2 */
                                                  /* irUp */
                                                  };

int jtag_state = 0;
int program_state = 0;







void setup() {
  pinMode(TMS, output);
  pinMode(TDI, output);
  pinMode(TCK, output);
  Serial.begin(BAUDRATE);
  Serial.setTimeout(1);
  }

void loop() {
  while (!Serial.available());
  byte data = Serial.read();
  if (data == 0x30) {

  }
  else {
  }
}
