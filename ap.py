import flet as ft
import time
import threading
import pygame  # لإضافة الصوت المخصص

# تهيئة pygame للصوت
pygame.mixer.init()

class TimerApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Timers"
        self.page.window_width = 360
        self.page.window_height = 640

        self.running = False
        self.repetitions = 1  # عدد التكرارات الافتراضي
        self.current_repetition = 0

        # القيم الافتراضية للعدادات
        self.green_time = 90  # 1 دقيقة و 30 ثانية
        self.red_time = 90  # 1 دقيقة و 30 ثانية

        # مكونات واجهة المستخدم
        self.repetitions_entry = ft.TextField(
            value="1", 
            label="Repetitions", 
            keyboard_type=ft.KeyboardType.NUMBER, 
            width=200  
        )

        # إدخال الوقت للعداد الأخضر
        self.green_label = ft.Text(
            f"Green Timer: {self.format_time(self.green_time)}", 
            size=20,  
            color="black"
        )
        self.green_time_entry = ft.TextField(
            value="1:30", 
            label="Green Timer (Minutes:Seconds)", 
            width=200
        )

        # إدخال الوقت للعداد الأحمر
        self.red_label = ft.Text(
            f"Red Timer: {self.format_time(self.red_time)}", 
            size=20,  
            color="black"
        )
        self.red_time_entry = ft.TextField(
            value="1:30", 
            label="Red Timer (Minutes:Seconds)", 
            width=200
        )

        # أزرار التحكم
        self.start_green_btn = ft.ElevatedButton(
            text="Start Timer", 
            on_click=self.start_green_timer, 
            bgcolor="#4CAF50", 
            color="white",
            width=150  
        )
        self.stop_btn = ft.ElevatedButton(
            text="Stop Timers", 
            on_click=self.stop_timers, 
            bgcolor="#f44336", 
            color="white",
            width=150  
        )

        # إضافة المكونات إلى الصفحة
        self.page.add(
            ft.Column(
                [
                    self.repetitions_entry,
                    self.green_label,
                    self.green_time_entry,
                    self.red_label,
                    self.red_time_entry,
                    ft.Row(
                        [self.start_green_btn, self.stop_btn], 
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        spacing=10
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def format_time(self, total_seconds):
        """تحويل الثواني إلى دقائق وثواني."""
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def parse_time(self, time_str):
        """تحويل النص بصيغة دقائق:ثواني إلى مجموع الثواني."""
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds

    def start_green_timer(self, e):
        try:
            self.green_time = self.parse_time(self.green_time_entry.value)
            self.red_time = self.parse_time(self.red_time_entry.value)
            self.repetitions = int(self.repetitions_entry.value)
            self.current_repetition = 0
            self.running = True
            self.start_green_btn.disabled = True
            self.page.update()
            threading.Thread(target=self.run_green_timer).start()
        except ValueError:
            self.green_label.value = "Invalid input!"
            self.page.update()

    def run_green_timer(self):
        while self.current_repetition < self.repetitions and self.running:
            self.current_repetition += 1
            green_time_left = self.green_time  
            red_time_left = self.red_time

            while green_time_left >= 0 and self.running:
                self.green_label.value = f"Green Timer: {self.format_time(green_time_left)}"
                self.page.update()
                time.sleep(1)
                green_time_left -= 1

            if green_time_left < 0:
                self.green_label.value = "Green Timer: Done!"
                self.play_sound("kick.mp3")
                self.page.update()
                self.run_red_timer(red_time_left)

    def run_red_timer(self, red_time_left):
        while red_time_left >= 0 and self.running:
            self.red_label.value = f"Red Timer: {self.format_time(red_time_left)}"
            self.page.update()
            time.sleep(1)
            red_time_left -= 1

        if red_time_left < 0:
            self.red_label.value = "Red Timer: Done!"
            self.play_sound("k1.mp3")
            self.page.update()

            if self.current_repetition < self.repetitions:
                self.run_green_timer()  
            else:
                self.reset_timers()

    def reset_tTimers(self):
        self.green_label.value = f"Green Timer: {self.format_time(self.green_time)}"
        self.red_label.value = f"Red Timer: {self.format_time(self.red_time)}"
        self.start_green_btn.disabled = False
        self.page.update()
        self.running = False

    def stop_timers(self, e):
        self.running = False
        self.green_label.value = "Green Timer: Stopped"
        self.red_label.value = "Red Timer: Stopped"
        self.start_green_btn.disabled = False
        self.page.update()

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

def main(page: ft.Page):
    app = TimerApp(page)

ft.app(target=main)
