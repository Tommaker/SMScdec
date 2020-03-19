#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import Tkinter as tk 
import tkMessageBox as mb

# 第1步，实例化object，建立窗口window 
window = tk.Tk() 

# 第2步，给窗口的可视化起名字 
window.title('SMS Deocder') 
# 第3步，设定窗口的大小(长 * 宽) 
window.geometry('500x560') # 这里的乘是小x 

# SMS input label
#SMS_input_label = tk.Label(window, text='Please Input the sms data to decode', bg='red', fg='yellow',font=('Arial', 18))
#SMS_input_label.pack()


sms_input_frame = tk.LabelFrame(window, text="输入编码的短信内容", width=65)
# Place a Entry - to get the SMS data
SMS_input_entry = tk.Text(sms_input_frame, width=35, height=8, font=('Arial', 14))
SMS_input_entry.pack()
sms_input_frame.pack(padx=10,pady=10)

#scroll = tk.Scrollbar(window, command=SMS_input_entry.yview)
#scroll.grid



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
    hex_num = [hex(int(i)) for i in list_num]
    print "Hex stream ".join(hex_num)


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
