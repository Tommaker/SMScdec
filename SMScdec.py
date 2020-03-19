#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import Tkinter as tk 
import tkMessageBox as mb

# 第1步，实例化object，建立窗口window 
window = tk.Tk() 

# 第2步，给窗口的可视化起名字 
window.title('SMS Deocder') 
# 第3步，设定窗口的大小(长 * 宽) 
window.geometry('500x600') # 这里的乘是小x 

# SMS input label
SMS_input_label = tk.Label(window, text='Please Input the sms data to decode', bg='red', fg='yellow',font=('Arial', 18))
SMS_input_label.pack()


# Place a Entry - to get the SMS data
SMS_input_entry = tk.Text(window, width=40, height=10, font=('Arial', 14))
SMS_input_entry.pack()

#scroll = tk.Scrollbar(window, command=SMS_input_entry.yview)
#scroll.grid




def ch_to_hex(ch):
    try:
        hex_num = int(ch,16)
    except ValueError:
        mb.showwarning(title='Warning', message='Please check the sms data, data range 0x00-0xFF.')
        return 0x00
    return int(ch,16)

def print_hex(list_num):
    hex_num = [hex(int(i)) for i in list_num]
    print " ".join(hex_num)


def show_info_txt(decode_result):
    if not decode_result:
        return
    SMS_show.insert('end', decode_result)


def SMS_decode():
    sms_data = SMS_input_entry.get("0.0", "end")
    print "sms_data is "+sms_data
    if not sms_data:
        mb.showwarning(title='Warning', message='Empty sms content!!Please input sms data.')

        return
    try:
        sms_data_int = list(map(ch_to_hex, sms_data.split()))
    except UnicodeEncodeError:
        mb.showwarning(title='Warning', message='Please check the sms data, data range 0x00-0xFF.')

    print sms_data_int
    print_hex(sms_data_int)

    if sms_data_int[0] == 0:
        print 'input success!'

    show_info_txt(sms_data)


op_frame = tk.LabelFrame(window, width=60)

op_txt_show = tk.Label(op_frame, text="Operation", width=15)
op_txt_show.grid(row=0, column=0,padx=10,pady=10)

decode_bt_left = tk.Button(op_frame, text='Decode', width=15, command=SMS_decode)
decode_bt_left.grid(row=0, column=1,pady=10,padx=10)

code_bt_right = tk.Button(op_frame, text='Code', width=15, command=None)
code_bt_right.grid(row=0, column=2,pady=10,padx=10)


op_frame.pack()

# Place button: Decode and Code
#Decode_button = tk.Button(window, text='Decode', width=15, command=SMS_decode)
#Code_button = tk.Button(window, text='Code', width=15, command=None)


#Decode_button.pack(side=tk.LEFT)
#Code_button.pack(side=tk.LEFT)
#Decode_button.place(x=0, y=10)
#Code_button.place(x=10, y=10)

result_frame = tk.LabelFrame(window, width=65)

peer_num = tk.Label(result_frame, text='对端号码', widt=15)
peer_num.grid(row=0, column=0, padx=10, pady=10)


result_frame.pack()


SMS_show = tk.Text(window, width=65, height=10)
SMS_show.pack()


# 第8步，主窗口循环显示 
window.mainloop()
