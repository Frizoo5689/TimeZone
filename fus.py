import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
from tkinter.font import Font

def get_utc_offset_str(timezone):
    now = datetime.now(pytz.timezone(timezone))
    offset_sec = now.utcoffset().total_seconds()
    offset_hrs = int(offset_sec / 3600)
    offset_min = int((offset_sec % 3600) / 60)
    sign = '+' if offset_hrs >= 0 else '-'
    return f'UTC{sign}{abs(offset_hrs):02d}:{abs(offset_min):02d}'

def update_times():
    for tz in timezones:
        formatted_time = format_time(tz)
        time_labels[tz].config(text=f'{formatted_time} {get_utc_offset_str(tz)}')
    root.after(60000, update_times)

def format_time(timezone):
    now = datetime.now(pytz.timezone(timezone))
    return now.strftime('%H:%M')

def convert_time():
    base_timezone_str = base_timezone_var.get().split(' ')[0]
    target_timezone_str = target_timezone_var.get().split(' ')[0]
    try:
        base_time_naive = datetime.strptime(base_time_entry.get(), '%H:%M')
        base_time_naive = base_time_naive.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    except ValueError:
        conversion_result_label.config(text="Invalid time format. Use HH:MM.")
        return

    base_timezone = pytz.timezone(base_timezone_str)
    target_timezone = pytz.timezone(target_timezone_str)
    base_time_utc = base_timezone.localize(base_time_naive).astimezone(pytz.utc)
    converted_time = base_time_utc.astimezone(target_timezone)
    conversion_result_label.config(text=converted_time.strftime('%H:%M'))

root = tk.Tk()
root.title("TimeZone by Lunedargent")
root.resizable(False, False)

bold_font = Font(family="Arial", size=10, weight="bold")
result_font = Font(family="Arial", size=16, weight="bold")
regular_font = Font(family="Arial", size=10)

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Timezone")

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Convert")
tab_control.pack(expand=1, fill="both")

timezones = [
    'Europe/Paris', 'Asia/Tokyo', 'America/New_York', 'America/Chicago',
    'America/Denver', 'America/Los_Angeles', 'Asia/Bangkok', 'Europe/Moscow'
]
time_labels = {}
for tz in timezones:
    frame = tk.Frame(tab1)
    frame.pack(anchor='center', fill='x', padx=10, pady=5)
    label = tk.Label(frame, text=f'{tz} {get_utc_offset_str(tz)}', width=35, anchor='w', font=bold_font)
    label.pack(side=tk.LEFT)
    time_label = tk.Label(frame, width=25, anchor='w', font=regular_font)
    time_label.pack(side=tk.LEFT)
    time_labels[tz] = time_label
    separator = ttk.Separator(tab1, orient='horizontal')
    separator.pack(fill='x')
update_times()

base_timezone_var = tk.StringVar()
base_timezone_var.set(timezones[0])
target_timezone_var = tk.StringVar()
target_timezone_var.set(timezones[0])

base_timezone_label = tk.Label(tab2, text="Base Timezone", font=bold_font)
base_timezone_label.pack()
base_timezone_menu = ttk.Combobox(tab2, textvariable=base_timezone_var, values=timezones, font=regular_font)
base_timezone_menu.pack()

base_time_label = tk.Label(tab2, text="Base Time (HH:MM)", font=bold_font)
base_time_label.pack()
base_time_entry = tk.Entry(tab2, font=regular_font)
base_time_entry.pack()

target_timezone_label = tk.Label(tab2, text="Target Timezone", font=bold_font)
target_timezone_label.pack()
target_timezone_menu = ttk.Combobox(tab2, textvariable=target_timezone_var, values=timezones, font=regular_font)
target_timezone_menu.pack()

convert_button = tk.Button(tab2, text="Convert", command=convert_time, font=regular_font)
convert_button.pack(pady=10)

conversion_result_label = tk.Label(tab2, text="", font=result_font)
conversion_result_label.pack()

root.mainloop()
