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
        self.CANVAS_WIDTH = self.master.winfo_width()
        self.CANVAS_HEIGHT = self.master.winfo_height()
        self.print_xy()
        self.pack()
        self.create_widgets()
        self.startup()
        self.print_xy()
        print("hwnd(winfo_id):"+str(self.master.winfo_id()))

    def create_widgets(self):

        self.test_canvas = tkinter.Canvas(self, bg='lightblue',
            width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
            highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, padx=0, pady=0)
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
            self.rect_start_x = event.x
            self.rect_start_y = event.y

    def pickup_position(self, event):
        if 0 <= event.x <= self.CANVAS_WIDTH and 0 <= event.y <= self.CANVAS_HEIGHT:
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

root = tkinter.Tk()
app = Application(master=root)
root.overrideredirect(True)
app.mainloop()