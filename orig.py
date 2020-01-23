import tkinter

# 解読関数
def decode_line(event):
    global current_line, title,bgimg, lcharimg, ccharimg, rcharimg
    if current_line >= len(scenario):
        return;
    # 1行読み込み
    line = scenario[current_line]
    current_line = current_line + 1
    line = line.replace("\\n", "\n").strip()
    params = line.split(" ")

    # 分岐
    if line[0] != "#":
        message["text"] = line
        return;
    elif params[0] == "#back":
        canvas.delete("all")
        bgimg = tkinter.PhotoImage(file=params[1])
        canvas.create_image(450, 230, image=bgimg)
    elif params[0] == "#putChar":
        if params[2] == "L":
            canvas.delete("left")
            lcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(180, 160, image=lcharimg, tag="left")
        elif params[2] == "R":
            canvas.delete("right")
            rcharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(720, 160, image=rcharimg, tag="right")
        else:
            canvas.delete("center")
            ccharimg = tkinter.PhotoImage(file=params[1])
            canvas.create_image(450, 160, image=ccharimg, tag="center")
    
    elif params[0] == "#delChar":
        if params[2] == "L":
            canvas.delete("left") 
        elif params[2] == "R":
            canvas.delete("right") 
        else:
            canvas.delete("center")
       
    elif params[0] == "#branch":
        message.unbind("<Button-1>")
        btn = tkinter.Button(text=params[2], width=18)
        branch.append(btn)
        btn["command"] = lambda : jump_to_line(int(params[1])-1)
        btn.place(x=325, y=70+int(params[1])*60)
        jumplabel.append(params[3])
        if params[4] == "n":
            return
    elif params[0] == "#jump":
        label = params[1].strip()
        # ジャンプ先を探す
        for l in range(len(scenario)):
            if scenario[l].strip() == "## " + label:
                current_line = l
                decode_line(None)
                return
    #勉強内容を入力
    elif params[0].strip() == "#in":
        message.unbind("<Button-1>")
        
        #テキストボックス表示
        entry=tkinter.Entry(width=30,bd=4)
        entry.place(x=50,y=83)

        entry2=tkinter.Entry(width=30,bd=4)
        entry2.place(x=50,y=133)

        entry3=tkinter.Entry(width=30,bd=4)
        entry3.place(x=50,y=183)
        
        #記録ボタン表示
        askbutton=tkinter.Button(text="記録")
        askbutton.place(x=420,y=75)
        
        askbutton2=tkinter.Button(text="記録")
        askbutton2.place(x=420,y=125)

        askbutton3=tkinter.Button(text="記録")
        askbutton3.place(x=420,y=175)

        #決定ボタン
        re_button=tkinter.Button(text="決定")
        re_button.place(x=420,y=250)
        
        #イベント設定
        def ask_click():  
            global val  
            val=entry.get()
            print(val)
            file=open("content.txt","w",encoding="utf-8")
            file.write(val)  
        askbutton["command"]=ask_click

        def ask_click2():  
            global val2  
            val2=entry2.get()
            print(val2)
            file=open("content.txt","w",encoding="utf-8")
            file.write(val+"\n"+val2)  
        askbutton2["command"]=ask_click2
       
        def ask_click3():   
            global val3  
            val3=entry3.get()
            print(val3)
            file=open("content.txt","w",encoding="utf-8")
            file.write(val+"\n"+val2+"\n"+val3)    
        askbutton3["command"]=ask_click3
       
        def re_click():  
            message["text"]="オッケー！　じゃ、あとは早く寝ようね♪"   
        re_button["command"]=re_click
       
    #勉強内容を出力
    elif params[0].strip() == "#out":
        file=open("content.txt","r",encoding="utf-8")
        line=file.readlines()

        if not line:
            message["text"] ="\n昨日の記録は特になしだね。\n\n今日の夜から計画してみよう♪"
            file.close()
            current_line=99999999
        else:    
            message["text"] ="\n【"+line[0].rstrip()+"】 と 【"+line[1].rstrip()+"】 と 【"+line[2]+"】 だよ!\n\n実践できるといいね♪"
            message.unbind("<Button-1>")
            current_line=99999999 
   
    elif params[0].strip() == "#end":
        message.unbind("<Button-1>")
        current_line=9999999
        
    # 再帰呼び出し
    decode_line(None)

# ジャンプ関数
def jump_to_line(branchID):
    global current_line
    # ボタンを消す
    for btn in branch:
        btn.place_forget()
        btn.destroy()
    branch.clear()
    label = jumplabel[branchID]
    jumplabel.clear()
    message.bind("<Button-1>", decode_line)
    # ジャンプ先を探す
    for l in range(len(scenario)):
        if scenario[l].strip() == "## " + label:
            current_line = l
            decode_line(None)
            return

# ウィンドウ作成
root = tkinter.Tk()
root.title("夜計画して朝振り返ろう！")
root.minsize(900, 460)
root.option_add("*font", ["メイリオ", 15])
# キャンバス作成
canvas = tkinter.Canvas(bg="blue",width=900, height=460)
canvas.place(x=0, y=0)

# メッセージエリア
message = tkinter.Label(width=70, height=5, wraplength=840,
    bg="white", justify="left", anchor="nw")
message.place(x=20, y=320)
message["text"] = "「一日の終わり」に計画して次の日に実践する、を始めましょう！！\n\n※ここか、出てくるボタンをクリックしながら進んでね♪\n初めてやる場合は、ワンクリック後、「一日の終わり」から進んでください。"

# ファイル読み込み
scenario = []
file = open("orig.txt", "r", encoding="utf-8")
while True:
    line = file.readline()
    scenario.append(line)
    if not line:
        file.close()
        break

# 現在の行数
current_line = 0
# イベント設定
message.bind("<Button-1>", decode_line)
# 画像
bgimg = None
lcharimg = None
ccharimg = None
rcharimg = None
# 選択肢
branch = []
jumplabel = []

root.mainloop()