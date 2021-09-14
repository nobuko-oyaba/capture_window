import tkinter
import tkinter.ttk
from tkinter import messagebox
import ctypes
#from ctypes import cast
#from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM

#todo: フレームを見えなくする＋ウィンドウ終了の実装方法を決める
#⇒一旦これでOKとする・・・。
#doco: 全画面＋常に前に表示
#⇒全画面はできてる。常に前もなってる・・・と思っている。
#todo: 座標をファイルに保存する
#⇒できてる。でも出力フォーマットはJSONにしようと思う。
#todo: 座標リストを指定し、キャプチャ＋クリップボード保存
#todo: 座標アイテムをファイルに出力するモード、キャプチャするモードで振り分け

class Application(tkinter.Frame):

    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 300

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.master.wm_attributes("-transparentcolor", "lightblue")
        
        #disabledにすると一切キー入力を受け付けなくなってしまった・・・。
        #self.master.wm_attributes("-disabled", True)
        
        #半透明化
        self.master.attributes("-alpha",0.8)
        
        #画面最大化
        self.master.attributes('-fullscreen', True)
        #tkinter.ttk.Style().configure("TP.TFrame", background="lightblue")
        self.master.title('tkinter canvas trial')
        
        self.master.update_idletasks()
        self.print_xy()
        self.pack()
        self.create_widgets()
        self.startup()
        self.print_xy()
        print("hwnd(winfo_id):"+str(self.master.winfo_id()))
        #window_no_title_bar(self.master)

    def create_widgets(self):
        self.start_x = tkinter.StringVar()
        self.start_y = tkinter.StringVar()
        self.current_x = tkinter.StringVar()
        self.current_y = tkinter.StringVar()

        self.label_description = tkinter.ttk.Label(self, text='Mouse position')
        self.label_description.grid(row=0, column=1)
        self.label_start_x = tkinter.ttk.Label(self, textvariable=self.start_x)
        self.label_start_x.grid(row=1, column=1)
        self.label_start_y = tkinter.ttk.Label(self, textvariable=self.start_y)
        self.label_start_y.grid(row=2, column=1)
        self.label_current_x = tkinter.ttk.Label(self, textvariable=self.current_x)
        self.label_current_x.grid(row=3, column=1)
        self.label_current_y = tkinter.ttk.Label(self, textvariable=self.current_y)
        self.label_current_y.grid(row=4, column=1)

        self.select_all_button = tkinter.ttk.Button(self, text='Select All', command=self.select_all)
        self.select_all_button.grid(row=5, column=1)

        self.test_canvas = tkinter.Canvas(self, bg='lightblue',
            width=(self.master.winfo_width()/3)+1, height=(self.master.winfo_height()/3)+1,
            highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        self.test_canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.test_canvas.bind('<B1-Motion>', self.pickup_position)
        self.test_canvas.bind('<Button-3>', self.close_window)
        self.test_canvas.bind('<Double-Button-1>', self.select_rectangle)

    def print_xy(self):
        print(self.master.winfo_width())    # ウィジェットの幅
        print(self.master.winfo_height())   # ウィジェットの高さ
        print(self.master.winfo_x())        # ウィジェットの位置 x
        print(self.master.winfo_y())        # ウィジェットの位置 y
    
    def startup(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    def start_pickup(self, event):
        if 0 <= event.x <= self.CANVAS_WIDTH and 0 <= event.y <= self.CANVAS_HEIGHT:
            self.start_x.set('x : ' + str(event.x))
            self.start_y.set('y : ' + str(event.y))
            self.rect_start_x = event.x
            self.rect_start_y = event.y

    def pickup_position(self, event):
        if 0 <= event.x <= self.CANVAS_WIDTH and 0 <= event.y <= self.CANVAS_HEIGHT:
            self.current_x.set('x : ' + str(event.x))
            self.current_y.set('y : ' + str(event.y))
            if self.rect:
                self.test_canvas.coords(self.rect,
                    min(self.rect_start_x, event.x), min(self.rect_start_y, event.y),
                    max(self.rect_start_x, event.x), max(self.rect_start_y, event.y))
            else:
                self.rect = self.test_canvas.create_rectangle(self.rect_start_x,
                    self.rect_start_y, event.x, event.y, outline='red')
        self.x0, self.y0, self.x1, self.y1 = self.test_canvas.coords(self.rect)

    def select_all(self):
        if self.rect:
            self.test_canvas.coords(self.rect, 0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        else:
            self.rect = self.test_canvas.create_rectangle(0, 0,
                self.CANVAS_WIDTH, self.CANVAS_HEIGHT, outline='red')
        self.x0, self.y0, self.x1, self.y1 = self.test_canvas.coords(self.rect)
        self.start_x.set('x : ' + str(self.x0))
        self.start_y.set('y : ' + str(self.y0))
        self.current_x.set('x : ' + str(self.x1))
        self.current_y.set('y : ' + str(self.y1))

    def close_window(self, event):
        ret = messagebox.askyesno('確認', '終了しますか？')
        if ret == True:
            self.master.destroy()

    def select_rectangle(self, event):
        with open("rectangle.txt", "a", encoding='UTF-8') as f:
            result = "x0:"+str(self.x0)+","+"y0:"+str(self.y0)+","+"x1:"+str(self.x1)+","+"y1:"+str(self.y1)
            print(result, file=f)
            print(result)
        f.close()

#このコードは動作しないためお蔵入りさせる・・・。ctypesよくわからなかった・・・。
def window_no_title_bar(master):
    #exStyle = HWND.WS_EX_COMPOSITED | ctypes.wintypes.WS_EX_TOPMOST
    GWL_EXSTYLE = -20
    GWL_STYLE = -16
    exStyle = 0
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    WS_CAPTION = 0x00C00000
    WS_THICKFRAME = 0x00040000
    hwnd = ctypes.windll.user32.GetParent(master.winfo_id())
    print("hwnd(winfo_id):"+str(master.winfo_id()))
    #hwnd = int(master.wm_frame(),16)
    print("hwnd:"+str(hwnd))
    #hwnd = int(master.frame(),16)
    print("hwnd:"+str(hwnd))
    #GWL_STYLE GWL_EXSTYLE
    style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    print("GetLastError:"+str(ctypes.GetLastError()))
    #style = style & ~WS_EX_TOOLWINDOW
    #style = style | WS_EX_APPWINDOW
    print("style:"+str(style))
    style &= ~(WS_CAPTION | WS_THICKFRAME)
    #ctypes.windll.user32.SetLastError(0)
    print("style:"+str(style))
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style)
    print("GetLastError:"+str(ctypes.GetLastError()))
    #self.master.withdraw()
    #ctypes.windll.user32.SetWindowPos(int(self.master.wm_frame(),16), 0,100, 100, 400,400,0)
    #print(ctypes.GetLastError())
    ctypes.windll.user32.SetWindowPos(hwnd, 0,0, 0, 0,0,0)
    print("GetLastError:"+str(ctypes.GetLastError()))

root = tkinter.Tk()
app = Application(master=root)
root.overrideredirect(True)
#root.after(10, lambda: window_no_title_bar(root))
app.mainloop()