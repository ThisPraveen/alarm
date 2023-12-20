import flask
import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame

class AlarmClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Alarm Clock")

        self.label = tk.Label(master, text="Set Alarm (HH:MM):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(pady=10)

        self.set_button = tk.Button(master, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.alarm_active = False

        # Initialize Pygame for audio
        pygame.init()

    def set_alarm(self):
        alarm_time = self.entry.get()
        try:
            # Parse the entered time
            alarm_hour, alarm_minute = map(int, alarm_time.split(':'))

            # Validate the entered time
            if not (0 <= alarm_hour < 24 and 0 <= alarm_minute < 60):
                raise ValueError("Invalid time format")

            # Calculate the time until the alarm goes off
            current_time = time.localtime(time.time())
            seconds_until_alarm = (alarm_hour - current_time.tm_hour) * 3600 + (alarm_minute - current_time.tm_min) * 60

            # Set the alarm in a separate thread
            threading.Thread(target=self.run_alarm, args=(seconds_until_alarm,), daemon=True).start()

        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please enter HH:MM")

    def run_alarm(self, seconds_until_alarm):
        self.alarm_active = True
        self.set_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        time.sleep(seconds_until_alarm)

        if self.alarm_active:
            # Play the alarm sound
            self.play_alarm_sound()

            messagebox.showinfo("Alarm", "Time's up!")
            self.stop_alarm()

    def play_alarm_sound(self):
        # Change this path to the location of your alarm sound file
        sound_path = "D:\PRAVEEN\animal.mp3"

        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except pygame.error:
            messagebox.showerror("Error", "Failed to play the alarm sound")

    def stop_alarm(self):
        self.alarm_active = False
        self.set_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        pygame.mixer.music.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
