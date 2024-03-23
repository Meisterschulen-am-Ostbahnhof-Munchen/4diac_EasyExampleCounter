// ISO-Designer ISO 11783   Version 5.6.2.5533 Jetter AG
// Do not change!

#define WorkingSet_0_Offset                                     1
#define DataMask_Home_Offset                                   21
#define Container_Gesamtzaehler_Offset                         71
#define Container_Tageszaehler_Offset                         129
#define SoftKeyMask_Home_Offset                               187
#define SoftKey_PlusPlus_Offset                               217
#define SoftKey_Reset_Gesamtzaehler_Offset                    230
#define SoftKey_Reset_Tageszaehler_Offset                     243
#define SoftKey_MinusMinus_Offset                             256
#define Button_PlusPlus_Offset                                269
#define Button_Reset_Gesamtzaehler_Offset                     288
#define Button_Reset_Tageszaehler_Offset                      307
#define Button_MinusMinus_Offset                              326
#define InputNumber_Gesamtziel_Offset                         345
#define InputNumber_Tagesziel_Offset                          383
#define OutputString_Fasszaehler_Offset                       421
#define OutputString_Reset_Gesamtzaehler_Offset               450
#define OutputString_Gesamtzaehler_Offset                     480
#define OutputString_Tageszaehler_Offset                      509
#define OutputString_Reset_Tageszaehler_Offset                537
#define OutputString_SoftKey_Reset_Gesamtzaehler_Offset       566
#define OutputString_SoftKey_Reset_Tageszaehler_Offset        596
#define OutputString_Ziel_Offset                              625
#define OutputString_ZielErreicht_Offset                      646
#define OutputNumber_Tageszaehler_Offset                      676
#define OutputNumber_Gesamtzaehler_Offset                     705
#define Rectangle_Box_Offset                                  734
#define Meter_Gesamtzaehler_Offset                            747
#define Meter_Tageszaehler_Offset                             768
#define LinearBargraph_Gesamtzaehler_Offset                   789
#define LinearBargraph_Tageszaehler_Offset                    813
#define Icon_Button_MinusMinus_Offset                         837
#define Icon_Button_PlusPlus_Offset                          1502
#define Icon_SoftKey_MinusMinus_Offset                       2167
#define IconSoftKey_PlusPlus_Offset                          2832
#define NumberVariable_Tageszaehler_Offset                   3497
#define NumberVariable_Gesamtzaehler_Offset                  3504
#define NumberVariable_Gesamtziel_Offset                     3511
#define NumberVariable_Tagesziel_Offset                      3518
#define FontAttributes_Default_Offset                        3525
#define FontAttributes_Button_Offset                         3533
#define LineAttributes_Border_Offset                         3541
#define FillAttributes_DarkerBG_Offset                       3549
#define ObjectPointer_Null2_Offset                           3557
#define ObjectPointer_Tagesziel_Offset                       3562
#define ObjectPointer_Gesamtziel_Offset                      3567
#define AuxFunction2_PlusPlus_Offset                         3572
#define AuxFunction2_MinusMinus_Offset                       3584

#define ISO_OP_MEMORY_CLASS

#define ISO_OP_DefaultPool_Size   3596
extern const unsigned char ISO_OP_MEMORY_CLASS isoOP_DefaultPool[];

#define ISO_OP_DefaultPool_ObjectNumber     48
extern const unsigned long ISO_OP_MEMORY_CLASS isoOP_DefaultPool_Offset[];
extern const unsigned long ISO_OP_MEMORY_CLASS isoOP_DefaultPool_Offset_Id[];
#define ISO_OP_DefaultPool_Scale_Offset      1

#define ID_NULL  0xFFFF

#define TYPEID_WORKSET        0
#define TYPEID_DATAMASK       1
#define TYPEID_ALARMMASK      2
#define TYPEID_CONTAINER      3
#define TYPEID_SKEYMASK       4
#define TYPEID_SOFTKEY        5
#define TYPEID_BUTTON         6
#define TYPEID_INBOOL         7
#define TYPEID_INSTR          8
#define TYPEID_INNUM          9
#define TYPEID_INLIST        10
#define TYPEID_OUTSTR        11
#define TYPEID_OUTNUM        12
#define TYPEID_OUTLINE       13
#define TYPEID_OUTRECT       14
#define TYPEID_OUTELLIPSE    15
#define TYPEID_OUTPOLY       16
#define TYPEID_OUTMETER      17
#define TYPEID_OUTLINBAR     18
#define TYPEID_OUTARCBAR     19
#define TYPEID_OUTPICT       20
#define TYPEID_VARNUM        21
#define TYPEID_VARSTR        22
#define TYPEID_FONTATTR      23
#define TYPEID_LINEATTR      24
#define TYPEID_FILLATTR      25
#define TYPEID_INPATTR       26
#define TYPEID_OBJPTR        27
#define TYPEID_MACRO         28
#define TYPEID_AUXFUNC       29
#define TYPEID_AUXINP        30
#define TYPEID_AUXFUNC2      31
#define TYPEID_AUXINP2       32
#define TYPEID_AUXPTR        33
#define TYPEID_WINMASK       34
#define TYPEID_KEYGROUP      35
#define TYPEID_GRPHCTXT      36
#define TYPEID_OUTLIST       37
#define TYPEID_EXTINPATTR    38
#define TYPEID_COLORMAP      39
#define TYPEID_OBJLBLREF     40
#define TYPEID_EXTOBJDEF     41
#define TYPEID_EXTREFNAME    42
#define TYPEID_EXTOBJPTR     43
#define TYPEID_ANIMATION     44
#define TYPEID_COLORPAL      45
#define TYPEID_GRAPHDATA     46
#define TYPEID_WSSPECIAL     47
#define TYPEID_SCALEGRAPH    48

#define EV_REFRESH            0
#define EV_ACT                1
#define EV_DEACT              2
#define EV_SHOW               3
#define EV_HIDE               4
#define EV_ENABLE             5
#define EV_DISABLE            6
#define EV_CHGACTMASK         7
#define EV_CHGSKEYMASK        8
#define EV_CHGATTR            9
#define EV_CHGBKCOLOR        10
#define EV_CHGFONTATTR       11
#define EV_CHGLINEATTR       12
#define EV_CHGFILLATTR       13
#define EV_CHGCHILDLOC       14
#define EV_CHGSIZE           15
#define EV_CHGVAL            16
#define EV_CHGPRIOR          17
#define EV_CHGENDPNT         18
#define EV_SELINPUT          19
#define EV_DESELINPUT        20
#define EV_ESC               21
#define EV_ENTERVAL          22
#define EV_ENTERCHGVAL       23
#define EV_KEYPRESS          24
#define EV_KEYRELEASE        25
#define EV_CHGCHILDPOS       26

#define CMD_HIDE_SHOW               160
#define CMD_ENABLE_DISABLE          161
#define CMD_SELECT_INPUT_OBJECT     162
#define CMD_CONTROL_AUDIO_DEVICE    163
#define CMD_SET_AUDIO_VOLUME        164
#define CMD_CHANGE_CHILD_LOCATION   165
#define CMD_CHANGE_SIZE             166
#define CMD_CHANGE_BACKGROUND_COLOR 167
#define CMD_CHANGE_NUMERIC_VALUE    168
#define CMD_CHANGE_END_POINT        169
#define CMD_CHANGE_FONT_ATTRIBUTES  170
#define CMD_CHANGE_LINE_ATTRIBUTES  171
#define CMD_CHANGE_FILL_ATTRIBUTES  172
#define CMD_CHANGE_ACTIVE_MASK      173
#define CMD_CHANGE_SOFT_KEY_MASK    174
#define CMD_CHANGE_ATTRIBUTE        175
#define CMD_CHANGE_PRIORITY         176
#define CMD_CHANGE_LIST_ITEM        177
#define CMD_CHANGE_STRING_VALUE     179
#define CMD_CHANGE_CHILD_POSITION   180
#define CMD_SET_OBJECT_LABEL        181
#define CMD_CHANGE_POLYGON_POINT    182
#define CMD_CHANGE_POLYGON_SCALE    183
#define CMD_GRAPHICS_CONTEXT        184
#define CMD_GET_ATTRIBUTE           185
#define CMD_SELECT_COLOURMAP_OR_PALETTE 186
#define CMD_EXECUTE_EXTENDED_MACRO  188
#define CMD_LOCK_UNLOCK_MASK        189
#define CMD_EXECUTE_MACRO           190

#define COLOR_BLACK       0
#define COLOR_WHITE       1
#define COLOR_GREEN       2
#define COLOR_TEAL        3
#define COLOR_MAROON      4
#define COLOR_PURPLE      5
#define COLOR_OLIVE       6
#define COLOR_SILVER      7
#define COLOR_GREY        8
#define COLOR_BLUE        9
#define COLOR_LIME       10
#define COLOR_CYAN       11
#define COLOR_RED        12
#define COLOR_MAGENTA    13
#define COLOR_YELLOW     14
#define COLOR_NAVY       15

#define FLOAT_1      0x00, 0x00, 0x80, 0x3F
#define FLOAT_10     0x00, 0x00, 0x20, 0x41
#define FLOAT_100    0x00, 0x00, 0xC8, 0x42
#define FLOAT_1000   0x00, 0x00, 0x7A, 0x44
#define FLOAT_0_1    0xCD, 0xCC, 0xCC, 0x3D
#define FLOAT_0_01   0x0A, 0xD7, 0x23, 0x3C
#define FLOAT_0_001  0x6F, 0x12, 0x83, 0x3A
