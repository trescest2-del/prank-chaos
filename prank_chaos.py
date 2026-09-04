import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import ctypes
from ctypes import wintypes
import os

# Variables globales
running = True
app_positions = {}
stop_window = None

# API Windows pour bouger les fenêtres
user32 = ctypes.windll.user32
HWND_TOP = 0

# Définir les bonnes fonctions Windows
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
GetWindowRect = user32.GetWindowRect
SetWindowPos = user32.SetWindowPos
SetForegroundWindow = user32.SetForegroundWindow
PostMessageW = user32.PostMessageW
IsWindowVisible = user32.IsWindowVisible
EnumWindows = user32.EnumWindows

def get_all_windows():
    """Récupère toutes les fenêtres ouvertes"""
    windows = []
    def enum_windows(hwnd, lParam):
        try:
            if IsWindowVisible(hwnd):
                length = GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowTextW(hwnd, buff, length + 1)
                    windows.append((hwnd, buff.value))
        except:
            pass
        return True
    
    enum_func = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    EnumWindows(enum_func(enum_windows), 0)
    return windows

def save_window_positions():
    """Sauvegarde les positions des fenêtres"""
    global app_positions
    print("Sauvegarde des positions...")
    windows = get_all_windows()
    for hwnd, title in windows:
        if title and len(title) > 0 and "STOP PRANK" not in title:
            rect = wintypes.RECT()
            GetWindowRect(hwnd, ctypes.byref(rect))
            app_positions[hwnd] = {
                'title': title,
                'left': rect.left,
                'top': rect.top,
                'right': rect.right,
                'bottom': rect.bottom
            }
            print(f"Sauvegardé: {title}")

def close_random_window():
    """Ferme une fenêtre aléatoire"""
    try:
        windows = get_all_windows()
        if windows:
            safe_windows = [w for w in windows if "STOP PRANK" not in w[1] and w[1] != ""]
            if safe_windows:
                hwnd, title = random.choice(safe_windows)
                PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
                print(f"✓ Fenêtre fermée: {title}")
    except Exception as e:
        print(f"Erreur fermeture: {e}")

def move_random_window():
    """Bouge une fenêtre aléatoire"""
    try:
        windows = get_all_windows()
        if windows:
            safe_windows = [w for w in windows if "STOP PRANK" not in w[1] and w[1] != ""]
            if safe_windows:
                hwnd, title = random.choice(safe_windows)
                x = random.randint(50, 1300)
                y = random.randint(50, 600)
                width = 800
                height = 600
                
                # Force la fenêtre à l'avant
                SetForegroundWindow(hwnd)
                time.sleep(0.2)
                
                # Bouge la fenêtre avec SetWindowPos
                SetWindowPos(hwnd, HWND_TOP, x, y, width, height, 0x0040)
                print(f"✓ Fenêtre bougée: {title} à ({x}, {y})")
                time.sleep(0.5)
    except Exception as e:
        print(f"Erreur déplacement: {e}")

def move_desktop_icons():
    """Bouge les icônes du bureau"""
    try:
        print("✓ Icônes du bureau en chaos pendant 5 secondes...")
        pyautogui.FAILSAFE = False
        
        # Positions aléatoires pour les icônes
        positions = [
            (100, 100), (200, 100), (300, 100), (400, 100),
            (100, 200), (200, 200), (300, 200), (400, 200),
            (100, 300), (200, 300), (300, 300), (400, 300),
        ]
        
        start_time = time.time()
        while time.time() - start_time < 5 and running:
            for _ in range(3):
                if not running:
                    break
                    
                # Clique sur une icône aléatoire
                x = random.randint(50, 300)
                y = random.randint(50, 250)
                
                # Clique droit pour le menu contextuel
                pyautogui.rightClick(x, y, duration=0.1)
                time.sleep(0.3)
                
                # Clique ailleurs pour fermer le menu
                pyautogui.click(800, 400, duration=0.1)
                time.sleep(0.2)
                
                # Glisse les icônes
                start_x = random.randint(50, 300)
                start_y = random.randint(50, 250)
                end_x = random.randint(50, 1000)
                end_y = random.randint(50, 600)
                
                pyautogui.drag(end_x - start_x, end_y - start_y, duration=0.5, _pause=False)
                time.sleep(0.3)
                
    except Exception as e:
        print(f"Erreur icônes: {e}")

def move_cursor():
    """Bouge le curseur pendant 3 secondes"""
    try:
        print("✓ Curseur en chaos pendant 3 secondes...")
        pyautogui.FAILSAFE = False
        start_time = time.time()
        while time.time() - start_time < 3 and running:
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            pyautogui.moveTo(x, y, duration=0.02)
            time.sleep(0.01)
    except Exception as e:
        print(f"Erreur curseur: {e}")

def black_screen():
    """Écran noir pendant 5 secondes"""
    try:
        print("✓ Écran noir pendant 5 secondes...")
        black_win = tk.Toplevel()
        black_win.attributes('-fullscreen', True)
        black_win.configure(bg='black')
        black_win.attributes('-topmost', True)
        black_win.update()
        
        time.sleep(5)
        black_win.destroy()
    except Exception as e:
        print(f"Erreur écran noir: {e}")

def open_random_site():
    """Ouvre un site aléatoire"""
    try:
        sites = [
            "https://www.google.com",
            "https://www.youtube.com",
            "https://www.tukif.com"
        ]
        site = random.choice(sites)
        print(f"✓ Ouverture de {site}...")
        os.startfile(site)
    except Exception as e:
        print(f"Erreur ouverture site: {e}")

def chaos_loop():
    """Boucle principale du chaos"""
    global running
    
    save_window_positions()
    
    # Liste des actions possibles
    all_actions = [1, 2, 3, 4, 5, 6]  # 1=fermer, 2=bouger fenêtres, 3=curseur, 4=écran noir, 5=sites aléatoires, 6=icônes
    actions_to_do = all_actions.copy()
    
    while running:
        if not actions_to_do:
            actions_to_do = all_actions.copy()
        
        action = random.choice(actions_to_do)
        actions_to_do.remove(action)
        
        try:
            if action == 1 and running:
                close_random_window()
            elif action == 2 and running:
                move_random_window()
            elif action == 3 and running:
                move_cursor()
            elif action == 4 and running:
                black_screen()
            elif action == 5 and running:
                open_random_site()
            elif action == 6 and running:
                move_desktop_icons()
        except Exception as e:
            print(f"Erreur action {action}: {e}")
        
        if running:
            # Temps aléatoire entre 1 et 10 minutes
            wait_time = random.randint(60, 600)
            minutes = wait_time // 60
            secondes = wait_time % 60
            print(f"\n⏰ Prochaine action dans {minutes}m {secondes}s...")
            time.sleep(wait_time)

def restore_windows():
    """Restaure toutes les fenêtres à leur position d'origine"""
    print("\n🔄 Restauration des fenêtres...")
    try:
        for hwnd, info in app_positions.items():
            try:
                left = info['left']
                top = info['top']
                right = info['right']
                bottom = info['bottom']
                width = right - left
                height = bottom - top
                
                SetWindowPos(hwnd, HWND_TOP, left, top, width, height, 0x0040)
                print(f"✓ Restauré: {info['title']}")
                time.sleep(0.5)
            except:
                pass
    except Exception as e:
        print(f"Erreur restauration: {e}")

def stop_chaos():
    """Arrête le chaos"""
    global running
    running = False
    print("\n🛑 Arrêt du chaos...")
    
    restore_windows()
    
    time.sleep(1)
    messagebox.showinfo("Arrêté! 😎", "Le chaos s'arrête!\n\nTout revient à la normale! ✅")
    stop_window.destroy()

def create_stop_button():
    """Crée la fenêtre STOP indestructible"""
    global stop_window
    
    stop_window = tk.Tk()
    stop_window.title("🛑 STOP PRANK")
    stop_window.geometry("350x150")
    stop_window.configure(bg='red')
    stop_window.attributes('-topmost', True)
    stop_window.resizable(False, False)
    
    def on_closing():
        pass
    
    stop_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    label = tk.Label(stop_window, text="🛑 PRANK EN COURS!", bg='red', fg='white', font=('Arial', 18, 'bold'))
    label.pack(pady=10)
    
    info_label = tk.Label(stop_window, text="Appuie pour arrêter le chaos!", bg='red', fg='white', font=('Arial', 11))
    info_label.pack(pady=5)
    
    button = tk.Button(stop_window, text="ARRÊTER LE CHAOS", command=stop_chaos, 
                       bg='yellow', fg='red', font=('Arial', 13, 'bold'), padx=25, pady=12)
    button.pack(pady=15)
    
    stop_window.mainloop()

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🎮 PRANK CHAOS DÉMARRÉ!")
    print("=" * 50)
    print("Actions: Fermeture / Déplacement fenêtres / Curseur / Écran noir / Sites aléatoires / Icônes bureau")
    print("Délai: Aléatoire entre 1 et 10 minutes")
    print("Sites: Google, YouTube, Tukif")
    print("Bouton STOP: Indestructible!")
    print("=" * 50)
    print()
    
    chaos_thread = threading.Thread(target=chaos_loop, daemon=True)
    chaos_thread.start()
    
    create_stop_button()

if __name__ == "__main__":
    main()
