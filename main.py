from tkinter import *
from functools import partial
from math import floor

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

checker_list = []
#rests = 0
cycles = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def timer_reset():
    global rests
    cycles = 0
    state_label.config(text='Pomodoro', fg=GREEN)
    canvas.itemconfig(timer_text, text=f'00:00')
    checker_label.config(text="")
    window.after_cancel(timer)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer_start_work():
    state_label.config(text='Work', fg=GREEN, font=(FONT_NAME, '38', 'bold'))
    #time_sec(5, is_rest=False)
    count_down(WORK_MIN*60)

def timer_start_short():
    state_label.config(text='Break', foreground=PINK, font=(FONT_NAME, '38', 'bold'))
    #time_sec(4, is_rest=True)
    count_down(SHORT_BREAK_MIN*60)

def timer_start_long():
    state_label.config(text='Break', fg=RED, font=(FONT_NAME, '38', 'bold'))
    #time_sec(3, is_rest=True)
    count_down(LONG_BREAK_MIN*60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    global cycles
    total_time = count
    minutes = floor(total_time / 60)
    seconds = floor(total_time % 60)
    if minutes < 10:
        minutes_display = f"0{minutes}"
    else:
        minutes_display = f"{minutes}"
    if seconds >= 10:
        seconds_display = f"{seconds}"
    else:
        seconds_display = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f'{minutes_display}:{seconds_display}')
    if floor(count) > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    if floor(count) == 0:
        cycles +=1
        if cycles < 7:
            #Short rests on odd
            if cycles%2 != 0:
                checker_list.append('✔️')
                checker_label.config(text=checker_list)
                timer_start_short()
            #Works on even
            elif cycles%2 == 0:
                timer_start_work()
        #Long rests are the (n*8)th 
        elif cycles == 7:
            checker_list.append('✔️')
            checker_label.config(text=checker_list)
            timer_start_long()
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Pomodoro')
window.minsize(height=500, width=525)
window.config(padx=100, pady=100,background=YELLOW)

canvas = Canvas(width=250, height=224, background=YELLOW, highlightthickness=0)
pomodoro_tomato = PhotoImage(file='tomato.png')
canvas.create_image(110, 112, image=pomodoro_tomato)
timer_text = canvas.create_text(110, 130, fill='white', text='00:00', font=(FONT_NAME, '30', 'bold'))
canvas.grid(row=1, column=1, pady=10)

state_label = Label(text="Pomodoro", font=(FONT_NAME, '38', 'bold'), background=YELLOW, fg=GREEN)
state_label.grid(row=0, column=1)

start_button = Button(text='Start', font=(FONT_NAME, '10', 'bold'), command=timer_start_work)
start_button.grid(row=2, column=0)

reset_button = Button(text='Reset', font=(FONT_NAME, '10', 'bold'), command=timer_reset)
reset_button.grid(row=2, column=2)

checker_label = Label(text=checker_list, background=YELLOW, foreground=GREEN)
checker_label.grid(row=2, column=1)



window.mainloop()

