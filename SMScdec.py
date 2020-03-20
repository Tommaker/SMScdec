#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import Tkinter as tk 
import tkMessageBox as mb


########################################################## SMS decode code below ################################################################
ProtocolDiscriminator = (
        "group call control",
        "broadcast call control",
        "EPS session management messages",
        "call control; call related SS messages",
        "GPRS Transparent Transport Protocol (GTTP)",
        "mobility management messages",
        "radio resources management messages",
        "EPS mobility management messages",
        "GPRS mobility management messages",
        "SMS messages",
        "GPRS session management messages",
        "non call related SS messages",
        "Location services specified in 3GPP TS 44.071",
        "",
        "extension of the PD to one octet length",
        "used by tests procedures described in 3GPP TS 44.014"
        )

'''
class NASPDUHeader():
    def __init__(self):
        self.Sec
'''

# Decode BCD stream.
def BCDDecode(RawData, StartIndex, NumLen):
    NumList = []
    if len(RawData) - StartIndex < NumLen:
        print 'Input BCD Decode data is shorter than input len.'
    elif NumLen <= 0:
        print 'Input BCD Decode NumLen is 0.'
    else:
        for i in range(NumLen):
            HighNum = RawData[StartIndex + i] & 0X0F
            LowNum = (RawData[StartIndex + i] & 0XF0) >> 4
            NumList.append(HighNum)
            if 0x0F != LowNum:
                NumList.append(LowNum)
    return NumList



# Parse RP Address
class RPAddr():
    def __init__(self):
        self.Len = 0
        self.Ext = 0
        self.NumType = 0
        self.NumPlan = 0
        self.Numdigit = []  # string type

    def Parse(self, DataArray, StartIndex):
        self.Len = DataArray[StartIndex]
        Offset = StartIndex + 1
        self.Ext = (DataArray[Offset] & 0x80) >> 7
        self.NumType = (DataArray[Offset] & 0x70)>>4
        self.NumPlan = (DataArray[Offset] & 0x0F)

        NumBytes = self.Len - 1

        self.Numdigit = BCDDecode(DataArray, Offset + 1, NumBytes)


# Parse RP Address
class TPAddr():
    def __init__(self):
        self.DigitLen = 0
        self.Ext = 0
        self.NumType = 0
        self.NumPlan = 0
        self.Numdigit = []  # string type

    def Parse(self, DataArray, StartIndex):
        self.DigitLen = DataArray[StartIndex]
        Offset = StartIndex + 1
        self.Ext = (DataArray[Offset] & 0x80) >> 7
        self.NumType = (DataArray[Offset] & 0x70)>>4
        self.NumPlan = (DataArray[Offset] & 0x0F)

        if 0 == self.DigitLen % 2:
            NumBytes = self.DigitLen / 2
        else:
            NumBytes = self.DigitLen /2 + 1

        self.Numdigit = BCDDecode(DataArray, Offset + 1, NumBytes)

class CPLayer():
    def __init__(self):
        self.PD = 0
        self.TransId = 0
        self.MsgType = 0
        self.CPDataLen = 0

    def Parse(self, DataArray):
        # check the length is validation
        if len(DataArray) < 3:
            return 0

        # set each field
        self.PD = DataArray[0] & 0x0F
        self.TransId = (DataArray[0] & 0xF0) >> 4
        self.MsgType = DataArray[1]
        self.CPDataLen = DataArray[2]
        return 3;


class RPLayer():
    def __init__(self):
        self.MsgType = 0
        self.MsgRef = 0
        self.RPOriAddr = RPAddr()
        self.RPDstAddr = RPAddr()
        self.UserDataLen = 0


    def Parse(self, DataArray, StartIndex):
        self.MsgType = DataArray[StartIndex]
        self.MsfRef = DataArray[StartIndex + 1]
        self.RPOriAddr.Parse(DataArray, StartIndex + 2)
        Offset = StartIndex + 2 + self.RPOriAddr.Len + 1
        self.RPDstAddr.Parse(DataArray, Offset)
        Offset = Offset + self.RPDstAddr.Len + 1

        self.UserDataLen = DataArray[Offset]




class TPLayer():
    def __init__(self):
        #self.TPFlags = 0
        self.TPRP = 0 # bit7 Reply-Path
        self.TPUDHI = 0 #bit6 User Data Header Indicator, indicating whether TP-UD field contains a Header
        self.TPSRR = 0  # bit5, Status Report Request
        self.TPVPF = 0  # bit4-3 Validity Period Format. The SMS valid period whether is present.
        self.TPRD = 0  # bit2  Reject Duplicates. Whether the SC accept the duplicates SMS.
        self.TPMTI = 0 #  bit1-0 Message Type Indicator.


        self.TPMR = 0 # byte, Message Reference
        self.TPDstAddr = RPAddr() # Destination Addr
        self.TPPID = 0
        self.TPDCS = 0
        self.TPUserDataLen = 0


    def Parse(self, DataArray, StartIndex):
        if len(DataArray) <= StartIndex:
            print 'Input TP Layer data error, length error'
            return
        ''''
            0   0   SMS DELIVER (in the direction SC to MS) 
            0   0   SMS DELIVER REPORT (in the direction MS to SC)  
            1   0   SMS STATUS REPORT (in the direction SC to MS)       
            1   0   SMS COMMAND (in the direction MS to SC) 
            0   1   SMS SUBMIT (in the direction MS to SC)  
            0   1   SMS SUBMIT REPORT (in the direction SC to MS)   
        '''
        Offset = StartIndex
        self.TPMTI = DataArray[Offset] & 0x03
        # Decode Submit SMS
        if 1 == self.TPMTI:
            self.TPRP = (DataArray[Offset] & 0x80) >> 7
            self.TPUDHI = (DataArray[Offset] & 0x40) >> 6
            self.TPSRR = (DataArray[Offset] & 0x20) >> 5
            self.TPVPF = (DataArray[Offset] & 0x18) >> 3
            self.TPRD = (DataArray[Offset] & 0x04) >> 2

        Offset = Offset + 1
        self.TPMR= DataArray[Offset]


        
        



########################################################## GUI code below ################################################################

# 第1步，实例化object，建立窗口window 
window = tk.Tk() 

# 第2步，给窗口的可视化起名字 
window.title('SMS Deocder') 
# 第3步，设定窗口的大小(长 * 宽) 
window.geometry('500x560') # 这里的乘是小x 

# Input Frame
sms_input_frame = tk.LabelFrame(window, text="输入编码的短信内容", width=65)

# Place a Entry - to get the SMS data
SMS_input_entry = tk.Text(sms_input_frame, width=35, height=8, font=('Arial', 14))
SMS_input_entry.pack()
sms_input_frame.pack(padx=10,pady=10)


# transfer dec to hex
def ch_to_hex(ch):
    '''
    try:
        hex_num = int(ch,16)
    except ValueError:
        mb.showerror(title='Input Content Error', message='Please check the sms data\ndata range 0x00-0xFF.')
        return
        '''
    return int(ch,16)


# Print hex stream.
def print_hex(list_num):
    print "Hex stream :\n"
    hex_num = [hex(int(i)) for i in list_num]
    print " ".join(hex_num)


def show_info_txt(decode_result):
    if not decode_result:
        return
    SMS_show.insert('end', decode_result)


def SMS_decode():
    sms_str = SMS_input_entry.get("0.0", "end")
    print "sms_data is "+sms_str
    sms_data= sms_str.replace('\n','').replace('\r','').strip()
    if not sms_data:
        mb.showerror(title='Input Error', message='Empty sms content!!!\nPlease input sms data.')
        return
    try:
        sms_data_int = list(map(ch_to_hex, sms_data.split()))
    except:
        mb.showwarning(title='Warning', message='Please check the sms data!!!\ndata range 0x00-0xFF.')
        return

    print sms_data_int
    print_hex(sms_data_int)

    show_info_txt(sms_data)


# Operation Frame
op_frame = tk.LabelFrame(window, width=65)

op_txt_show = tk.Label(op_frame, text="Operation", width=15)
op_txt_show.grid(row=0, column=0,padx=5, pady=5)

decode_bt_left = tk.Button(op_frame, text='Decode', width=10, command=SMS_decode)
decode_bt_left.grid(row=0, column=1,pady=5, padx=5)

code_bt_right = tk.Button(op_frame, text='Code', width=10, command=None)
code_bt_right.grid(row=0, column=2,pady= 5,padx=5)


op_frame.pack(padx=10,pady=10)

# Place button: Decode and Code
#Decode_button = tk.Button(window, text='Decode', width=15, command=SMS_decode)
#Code_button = tk.Button(window, text='Code', width=15, command=None)


#Decode_button.pack(side=tk.LEFT)
#Code_button.pack(side=tk.LEFT)
#Decode_button.place(x=0, y=10)
#Code_button.place(x=10, y=10)


#decode result
result_frame = tk.LabelFrame(window, text="解码结果", width=65)
#result_frame = tk.LabelFrame(window, width=65)

peer_num = tk.Label(result_frame, text='对端号码')
peer_num.grid(row=0, column=0, padx=5)
peer_num_E = tk.Entry(result_frame, width=40)
peer_num_E.grid(row=0, column=1,padx=5)

base_num = tk.Label(result_frame, text='基站号码')
base_num.grid(row=1, column=0)
base_num_E = tk.Entry(result_frame, width=40)
base_num_E.grid(row=1, column=1,padx=5)

code_scheme = tk.Label(result_frame, text='编码方式')
code_scheme.grid(row=2, column=0)
code_scheme_E = tk.Entry(result_frame, width=40)
code_scheme_E.grid(row=2, column=1,padx=5)




#SMS_show = tk.Text(result_frame, width=65, height=10)
'''

'''
result_frame.pack(padx=10)


#decode result
sms_content_frame = tk.LabelFrame(window, text="短信解码内容", width=65)
SMS_show = tk.Text(sms_content_frame, width=50, height=10)
SMS_show.grid(row=0, column=0)

sms_content_frame.pack(padx=10)

# 第8步，主窗口循环显示 
window.mainloop()
