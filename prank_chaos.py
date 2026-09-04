import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import subprocess
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

def get_all_windows():
    """Récupère toutes les fenêtres ouvertes"""
    windows = []
    def enum_windows(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLength(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                windows.append((hwnd, buff.value))
        return True
    
    enum_func = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(enum_func(enum_windows), 0)
    return windows

def save_window_positions():
    """Sauvegarde les positions des fenêtres"""
    global app_positions
    print("Sauvegarde des positions...")
    windows = get_all_windows()
    for hwnd, title in windows:
        if title and len(title) > 0 and "STOP PRANK" not in title:
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
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
                user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
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
                x = random.randint(100, 1400)
                y = random.randint(100, 700)
                user32.SetWindowPos(hwnd, HWND_TOP, x, y, 600, 400, 0)
                print(f"✓ Fenêtre bougée: {title} à ({x}, {y})")
    except Exception as e:
        print(f"Erreur déplacement: {e}")

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

def open_google():
    """Ouvre Google dans le navigateur"""
    try:
        print("✓ Ouverture de Google...")
        os.startfile("https://www.google.com")
    except Exception as e:
        print(f"Erreur Google: {e}")

def show_virus_notification():
    """Affiche une notification VIRUS"""
    try:
        print("✓ Notification VIRUS affichée!")
        messagebox.showwarning("⚠️ VIRUS DÉTECTÉ!", "VIRUS TROUVÉ!\n\nTon PC est hacké! 😂\n\n(C'est juste un prank!)")
    except Exception as e:
        print(f"Erreur notification: {e}")

def chaos_loop():
    """Boucle principale du chaos"""
    global running
    
    save_window_positions()
    
    # Liste des actions possibles
    all_actions = [1, 2, 3, 4, 5, 6]  # 1=fermer, 2=bouger, 3=curseur, 4=écran noir, 5=Google, 6=notification
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
                open_google()
            elif action == 6 and running:
                show_virus_notification()
        except Exception as e:
            print(f"Erreur action {action}: {e}")
        
        if running:
            # 3 minutes = 180 secondes
            wait_time = 180
            print(f"\n⏰ Prochaine action dans {wait_time} secondes (3 minutes)...")
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
                
                user32.SetWindowPos(hwnd, HWND_TOP, left, top, width, height, 0)
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
    print("Actions: Fermeture / Déplacement / Curseur / Écran noir / Google / Notifications")
    print("Délai: 3 minutes entre chaque action")
    print("Bouton STOP: Indestructible!")
    print("=" * 50)
    print()
    
    chaos_thread = threading.Thread(target=chaos_loop, daemon=True)
    chaos_thread.start()
    
    create_stop_button()

if __name__ == "__main__":
    main()
