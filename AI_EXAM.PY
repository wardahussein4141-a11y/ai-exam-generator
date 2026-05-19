import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os
from fpdf import FPDF

BG = "#eef2f7"
CARD = "#ffffff"
PRIMARY = "#4a6cf7"
SECONDARY = "#6c63ff"
TEXT = "#2d2d2d"
ACCENT = "#ff6b6b"

BANK_FILE = "question_bank.json"

def load_bank():
    if os.path.exists(BANK_FILE):
        with open(BANK_FILE, "r") as f:
            return json.load(f)
    return []

def save_bank(data):
    with open(BANK_FILE, "w") as f:
        json.dump(data, f)

question_bank = load_bank()

def login():
    if user_entry.get() == "admin" and pass_entry.get() == "1234":
        login_win.destroy()
        main_app()
    else:
        messagebox.showerror("Error", "Invalid login")

def mcq(topic, diff):
    return {"type":"MCQ","q":f"What is {topic}?","a":"A","d":diff}

def tf(topic, diff):
    return {"type":"TF","q":f"{topic} is important. True/False","a":"True","d":diff}

def short(topic, diff):
    return {"type":"SHORT","q":f"Explain {topic}.","a":topic.lower(),"d":diff}

time_left = 0
current_exam = []
answer_entries = []

def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer.config(text=f"Time Left: {time_left}s")
        root.after(1000, countdown)
    else:
        submit()

def generate():
    global current_exam, time_left, answer_entries

    topic = topic_entry.get()
    diff = diff_var.get()

    if topic == "" or name_entry.get() == "" or id_entry.get() == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    try:
        num = int(num_entry.get())
    except:
        messagebox.showerror("Error", "Enter number")
        return

    current_exam = []
    answer_entries = []
    output_frame.destroy()

    create_output_frame()

    time_left = 60
    countdown()

    for i in range(num):
        t = random.choice(["MCQ","TF","SHORT"])

        if t == "MCQ":
            q = mcq(topic,diff)
        elif t == "TF":
            q = tf(topic,diff)
        else:
            q = short(topic,diff)

        current_exam.append(q)
        question_bank.append(q)

        tk.Label(output_frame, text=f"{i+1}. {q['q']}", bg=CARD, fg=TEXT).pack(anchor="w", pady=2)

        entry = tk.Entry(output_frame, width=40)
        entry.pack(pady=2)

        answer_entries.append(entry)

    save_bank(question_bank)

def submit():
    score = 0

    for i, q in enumerate(current_exam):
        user_ans = answer_entries[i].get().strip().lower()

        if user_ans == q["a"].lower():
            score += 1

    messagebox.showinfo("Result", f"Score: {score}/{len(current_exam)}")

def view_bank():
    for widget in output_frame.winfo_children():
        widget.destroy()

    for i,q in enumerate(question_bank[-10:],1):
        tk.Label(output_frame, text=f"{i}. {q['q']}", bg=CARD).pack(anchor="w")

def export_pdf():
    if not current_exam:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files","*.pdf")])
    if not file_path:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",12)

    pdf.cell(200,10,"FINAL EXAM",ln=True,align="C")
    pdf.ln(5)

    pdf.cell(200,10,f"Name: {name_entry.get()}",ln=True)
    pdf.cell(200,10,f"ID: {id_entry.get()}",ln=True)
    pdf.ln(5)

    for i,q in enumerate(current_exam):
        user_ans = answer_entries[i].get()

        pdf.multi_cell(0,10,f"{i+1}. {q['q']}\nAnswer: {user_ans}\nCorrect: {q['a']}\n")

    pdf.output(file_path)
    messagebox.showinfo("Saved","PDF saved")

def create_output_frame():
    global output_frame
    output_frame = tk.Frame(card, bg=CARD)
    output_frame.pack(pady=10, fill="both", expand=True)

def main_app():
    global root,topic_entry,num_entry,diff_var,name_entry,id_entry,timer,card,output_frame

    root = tk.Tk()
    root.title("AI Exam Generator")
    root.geometry("820x700")
    root.configure(bg=BG)

    card = tk.Frame(root, bg=CARD)
    card.place(relx=0.5, rely=0.5, anchor="center", width=760, height=650)

    tk.Label(card, text="AI EXAM SYSTEM", bg=CARD, fg=PRIMARY,
             font=("Segoe UI",18,"bold")).pack(pady=10)

    timer = tk.Label(card, text="Time Left: 0", bg=CARD, fg=ACCENT)
    timer.pack()

    form = tk.Frame(card, bg=CARD)
    form.pack(pady=5)

    tk.Label(form, text="Name", bg=CARD).grid(row=0,column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0,column=1)

    tk.Label(form, text="ID", bg=CARD).grid(row=1,column=0)
    id_entry = tk.Entry(form)
    id_entry.grid(row=1,column=1)

    tk.Label(form, text="Topic", bg=CARD).grid(row=2,column=0)
    topic_entry = tk.Entry(form)
    topic_entry.grid(row=2,column=1)

    tk.Label(form, text="Number", bg=CARD).grid(row=3,column=0)
    num_entry = tk.Entry(form)
    num_entry.grid(row=3,column=1)

    tk.Label(form, text="Difficulty", bg=CARD).grid(row=4,column=0)

    diff_var = tk.StringVar(value="easy")
    tk.Radiobutton(form, text="Easy", variable=diff_var, value="easy", bg=CARD).grid(row=4,column=1,sticky="w")
    tk.Radiobutton(form, text="Medium", variable=diff_var, value="medium", bg=CARD).grid(row=5,column=1,sticky="w")
    tk.Radiobutton(form, text="Hard", variable=diff_var, value="hard", bg=CARD).grid(row=6,column=1,sticky="w")

    btns = tk.Frame(card, bg=CARD)
    btns.pack(pady=5)

    tk.Button(btns, text="Generate", bg=PRIMARY, fg="white", width=12, command=generate).grid(row=0,column=0,padx=5)
    tk.Button(btns, text="Submit", bg=SECONDARY, fg="white", width=12, command=submit).grid(row=0,column=1,padx=5)
    tk.Button(btns, text="View Bank", bg="#9b59b6", fg="white", width=12, command=view_bank).grid(row=0,column=2,padx=5)
    tk.Button(btns, text="Save PDF", bg="#ff7f50", fg="white", width=12, command=export_pdf).grid(row=0,column=3,padx=5)

    create_output_frame()

    root.mainloop()

login_win = tk.Tk()
login_win.title("Login")
login_win.geometry("350x260")
login_win.configure(bg=BG)

login_card = tk.Frame(login_win, bg=CARD)
login_card.place(relx=0.5, rely=0.5, anchor="center", width=280, height=200)

tk.Label(login_card, text="Login", bg=CARD, fg=PRIMARY,
         font=("Segoe UI",14,"bold")).pack(pady=10)

tk.Label(login_card, text="Username", bg=CARD).pack()
user_entry = tk.Entry(login_card)
user_entry.pack(pady=5)

tk.Label(login_card, text="Password", bg=CARD).pack()
pass_entry = tk.Entry(login_card, show="*")
pass_entry.pack(pady=5)

tk.Button(login_card, text="Login", bg=PRIMARY, fg="white",
          width=15, command=login).pack(pady=10)

login_win.mainloop()
