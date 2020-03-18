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
    sms_data_int = list(map(ch_to_hex, sms_data.split()))

    print sms_data_int
    print_hex(sms_data_int)

    if sms_data_int[0] == 0:
        print 'input success!'

    show_info_txt(sms_data)



# Place button: Decode and Code
Decode_button = tk.Button(window, text='Decode', command=SMS_decode)
Code_button = tk.Button(window, text='Code', command=None)


Decode_button.pack()
Code_button.pack()


SMS_show = tk.Text(window, width=65, height=10)
SMS_show.pack()


# 第8步，主窗口循环显示 
window.mainloop()
