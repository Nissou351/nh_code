from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.core.window import Window
import webbrowser
import random
from plyer import tts

# الألوان
SOFT_CYAN = (0, 0.8, 1, 1) 
HACKER_GREEN = (0, 1, 0, 1)
BRIGHT_MATRIX = (0, 1, 0, 0.7) 
DARK_BG = (0, 0, 0, 1)

def speak(text):
    try:
        tts.speak(text.replace("[", "").replace("]", "").replace("-", " "))
    except:
        pass

# --- 1. واجهة الماتريكس (محسنة وواضحة) ---
class MatrixSplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.matrix_container = BoxLayout(orientation='horizontal', spacing=2)
        self.labels = []
        for _ in range(50): 
            lbl = Label(text="", color=BRIGHT_MATRIX, font_size='15sp', bold=True)
            self.matrix_container.add_widget(lbl)
            self.labels.append(lbl)
        layout.add_widget(self.matrix_container)

        self.start_btn = Button(text="[ START SYSTEM ]", size_hint=(0.65, 0.14),
                                pos_hint={'center_x': 0.5, 'y': 0.15},
                                background_color=(0, 0.6, 0, 1), color=(1,1,1,1),
                                font_size='26sp', bold=True, background_normal='')
        self.start_btn.bind(on_press=lambda x: [speak("System Online"), setattr(self.manager, 'current', 'main_menu')])
        layout.add_widget(self.start_btn)
        self.add_widget(layout)
        Clock.schedule_interval(self.update_matrix, 0.07)

    def update_matrix(self, dt):
        for lbl in self.labels:
            lbl.text = "\n".join([random.choice("01#!?@$%&") for _ in range(35)])

# --- 2. القائمة الرئيسية ---
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(text="Nh_code", font_size='80sp', color=SOFT_CYAN, pos_hint={'center_x': 0.5, 'top': 0.9}))

        btn_box = BoxLayout(orientation='vertical', size_hint=(0.85, 0.4), 
                            pos_hint={'center_x': 0.5, 'center_y': 0.4}, spacing=20)
        
        items = [("[ NetHunter Installer ]", 'steps_page'), 
                 ("[ Network Tools ]", 'network_page'), 
                 ("[ Pentest Suite ]", 'tools_page')]
        
        for txt, target in items:
            btn = Button(text=txt, background_color=(0, 0.4, 0, 1), color=(1,1,1,1), 
                         bold=True, font_size='22sp', background_normal='')
            btn.bind(on_press=lambda x, t=target, n=txt: [speak(n), setattr(self.manager, 'current', t)])
            btn_box.add_widget(btn)
        
        layout.add_widget(btn_box)
        self.add_widget(layout)

# --- 3. صفحة NetHunter (أزرار ضخمة) ---
class StepsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=[20, 30], spacing=30, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        content.add_widget(Label(text="NETHUNTER INSTALL", color=SOFT_CYAN, font_size='30sp', bold=True, size_hint_y=None, height=80))

        steps = [
            ("STEP 01: UPDATE", "pkg update && pkg upgrade -y"),
            ("STEP 02: TOOLS", "pkg install wget -y"),
            ("STEP 03: INSTALL", "wget -O install-nethunter-termux https://offs.ec/2Mdg7S2 && chmod +x install-nethunter-termux && ./install-nethunter-termux"),
            ("STEP 04: RUN", "nethunter"),
            ("STEP 05: GUI", "nethunter kex &")
        ]

        for title, cmd in steps:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=10)
            card.add_widget(Label(text=title, color=(1,1,1,1), font_size='20sp', bold=True))
            row = BoxLayout(size_hint_y=None, height=75, spacing=15)
            row.add_widget(TextInput(text=cmd, readonly=True, font_size='16sp', background_color=(0.1, 0.1, 0.1, 1), foreground_color=HACKER_GREEN))
            
            # تكبير زر COPY
            cp = Button(text="COPY", size_hint_x=0.35, background_color=(0, 0.5, 0.9, 1), font_size='18sp', bold=True)
            cp.bind(on_press=lambda x, c=cmd: [speak("Copied"), Clipboard.copy(c)])
            row.add_widget(cp)
            
            card.add_widget(row)
            content.add_widget(card)

        content.add_widget(Label(text="TIP: IP 127.0.0.1 | PORT 5901", color=(1, 0.8, 0, 1), font_size='22sp', bold=True, size_hint_y=None, height=70))
        
        # زر تحميل ضخم
        dl_btn = Button(text="DOWNLOAD KEX CLIENT", size_hint_y=None, height=100, background_color=(0, 0.4, 0.7, 1), font_size='20sp', bold=True)
        dl_btn.bind(on_press=lambda x: webbrowser.open("https://store.nethunter.com/repo/com.offsec.nethunter.kex_2020062900.apk"))
        content.add_widget(dl_btn)

        # زر رجوع ضخم
        back = Button(text="RETURN TO MENU", size_hint_y=None, height=100, background_color=(0.6, 0, 0, 1), font_size='22sp', bold=True)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        content.add_widget(back)

        scroll.add_widget(content)
        self.add_widget(scroll)

# --- 4. صفحة Network Tools (أزرار ضخمة) ---
class NetworkPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=[20, 30], spacing=30, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        content.add_widget(Label(text="NETWORK TOOLS", color=SOFT_CYAN, font_size='30sp', bold=True, size_hint_y=None, height=80))

        tools = [
            ("IP INFO", "ifconfig"),
            ("SCAN LAN", "nmap -sn 192.168.1.0/24"),
            ("PING", "ping -c 4 google.com"),
            ("OPEN PORTS", "netstat -tuln")
        ]

        for title, cmd in tools:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=10)
            card.add_widget(Label(text=title, color=(1,1,1,1), font_size='20sp', bold=True))
            row = BoxLayout(size_hint_y=None, height=75, spacing=15)
            row.add_widget(TextInput(text=cmd, readonly=True, font_size='16sp', background_color=(0.1, 0.1, 0.1, 1), foreground_color=HACKER_GREEN))
            
            cp = Button(text="COPY", size_hint_x=0.35, background_color=(0, 0.5, 0.9, 1), font_size='18sp', bold=True)
            cp.bind(on_press=lambda x, c=cmd: [speak("Copied"), Clipboard.copy(c)])
            row.add_widget(cp)
            
            card.add_widget(row)
            content.add_widget(card)

        content.add_widget(Label(text="[ ADVICE: Stay secure and anonymous ]", color=(1, 0.5, 0, 1), font_size='18sp', italic=True, size_hint_y=None, height=60))

        back = Button(text="RETURN TO MENU", size_hint_y=None, height=100, background_color=(0.6, 0, 0, 1), font_size='22sp', bold=True)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        content.add_widget(back)
        scroll.add_widget(content)
        self.add_widget(scroll)

# --- 5. صفحة Pentest Suite (أزرار ضخمة) ---
class ToolsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=[20, 30], spacing=30, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        content.add_widget(Label(text="PENTEST SUITE", color=SOFT_CYAN, font_size='30sp', bold=True, size_hint_y=None, height=80))

        suite = [
            ("METASPLOIT", "pkg install metasploit -y"),
            ("SQLMAP", "pkg install sqlmap -y"),
            ("HYDRA", "pkg install hydra -y"),
            ("NMAP A", "nmap -A -T4 scanme.nmap.org")
        ]

        for title, cmd in suite:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=10)
            card.add_widget(Label(text=title, color=(1,1,1,1), font_size='20sp', bold=True))
            row = BoxLayout(size_hint_y=None, height=75, spacing=15)
            row.add_widget(TextInput(text=cmd, readonly=True, font_size='16sp', background_color=(0.1, 0.1, 0.1, 1), foreground_color=HACKER_GREEN))
            
            cp = Button(text="COPY", size_hint_x=0.35, background_color=(0, 0.5, 0.9, 1), font_size='18sp', bold=True)
            cp.bind(on_press=lambda x, c=cmd: [speak("Copied"), Clipboard.copy(c)])
            row.add_widget(cp)
            
            card.add_widget(row)
            content.add_widget(card)

        content.add_widget(Label(text="[ ADVICE: Ethical hacking is the way ]", color=(0, 1, 1, 1), font_size='18sp', bold=True, size_hint_y=None, height=60))

        back = Button(text="RETURN TO MENU", size_hint_y=None, height=100, background_color=(0.6, 0, 0, 1), font_size='22sp', bold=True)
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        content.add_widget(back)
        scroll.add_widget(content)
        self.add_widget(scroll)

class Nh_code(App):
    def build(self):
        Window.clearcolor = DARK_BG
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MatrixSplashScreen(name='splash'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(StepsPage(name='steps_page'))
        sm.add_widget(NetworkPage(name='network_page'))
        sm.add_widget(ToolsPage(name='tools_page'))
        return sm

if __name__ == '__main__':
    Nh_code().run()
