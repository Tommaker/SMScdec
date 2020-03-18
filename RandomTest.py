import Tkinter as tk

window = tk.Tk()

window.title("Test window")

text1 = tk.Text(window, width=20, height=10)

text1.pack()

text_content = []
def getData():
    text_content = text1.get("0.0", "end")
    print text_content

button1 = tk.Button(window, text='OK', command=getData)
button1.pack()

window.mainloop()
