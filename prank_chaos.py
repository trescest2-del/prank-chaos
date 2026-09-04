import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import subprocess
import ctypes
from ctypes import wintypes

# Variables globales
running = True
app_positions = {}
stop_window = None
actions_done = set()

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
    windows = get_all_windows()
    for hwnd, title in windows:
        if title and len(title) > 0:
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            app_positions[hwnd] = (rect.left, rect.top, rect.right, rect.bottom)

def close_random_window():
    """Ferme une fenêtre aléatoire"""
    try:
        windows = get_all_windows()
        if windows:
            # Exclut le bouton STOP
            safe_windows = [w for w in windows if "STOP PRANK" not in w[1]]
            if safe_windows:
                hwnd, title = random.choice(safe_windows)
                user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
                print(f"Fenêtre fermée: {title}")
    except Exception as e:
        print(f"Erreur fermeture: {e}")

def move_random_window():
    """Bouge une fenêtre aléatoire"""
    try:
        windows = get_all_windows()
        if windows:
            # Exclut le bouton STOP
            safe_windows = [w for w in windows if "STOP PRANK" not in w[1]]
            if safe_windows:
                hwnd, title = random.choice(safe_windows)
                x = random.randint(50, 1400)
                y = random.randint(50, 700)
                user32.SetWindowPos(hwnd, HWND_TOP, x, y, 800, 600, 0)
                print(f"Fenêtre bougée: {title} à ({x}, {y})")
    except Exception as e:
        print(f"Erreur déplacement: {e}")

def move_cursor():
    """Bouge le curseur pendant 3 secondes"""
    try:
        print("Curseur en chaos pendant 3 secondes...")
        pyautogui.FAILSAFE = False
        start_time = time.time()
        while time.time() - start_time < 3 and running:
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            pyautogui.moveTo(x, y, duration=0.05)
            time.sleep(0.02)
        print("Curseur revenu à la normale")
    except Exception as e:
        print(f"Erreur curseur: {e}")

def black_screen():
    """Écran noir pendant 5 secondes"""
    try:
        print("Écran noir pendant 5 secondes...")
        black_win = tk.Toplevel()
        black_win.attributes('-fullscreen', True)
        black_win.configure(bg='black')
        black_win.attributes('-topmost', True)
        black_win.update()
        
        time.sleep(5)
        black_win.destroy()
        print("Écran revenu à la normale")
    except Exception as e:
        print(f"Erreur écran noir: {e}")

def chaos_loop():
    """Boucle principale du chaos"""
    global running, actions_done
    
    save_window_positions()
    
    # Liste des actions possibles
    all_actions = [1, 2, 3, 4]  # 1=fermer, 2=bouger, 3=curseur, 4=écran noir
    actions_to_do = all_actions.copy()
    
    while running:
        if not actions_to_do:
            # Quand toutes les actions sont faites, on les réinitialise
            actions_to_do = all_actions.copy()
        
        # Prend une action aléatoire de la liste
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
        except Exception as e:
            print(f"Erreur action {action}: {e}")
        
        if running:
            # Attente plus longue entre les actions (5 à 10 secondes)
            wait_time = random.randint(5, 10)
            print(f"Prochaine action dans {wait_time} secondes...")
            time.sleep(wait_time)

def stop_chaos():
    """Arrête le chaos"""
    global running
    running = False
    print("Arrêt du chaos...")
    
    # Restaure les positions des fenêtres
    try:
        for hwnd, (left, top, right, bottom) in app_positions.items():
            width = right - left
            height = bottom - top
            user32.SetWindowPos(hwnd, HWND_TOP, left, top, width, height, 0)
        print("Fenêtres restaurées")
    except Exception as e:
        print(f"Erreur restauration: {e}")
    
    time.sleep(1)
    messagebox.showinfo("Arrêté!", "Le chaos s'arrête! 😎\nTout revient à la normale!")
    stop_window.destroy()

def create_stop_button():
    """Crée la fenêtre STOP indestructible"""
    global stop_window
    
    stop_window = tk.Tk()
    stop_window.title("🛑 STOP PRANK")
    stop_window.geometry("300x120")
    stop_window.configure(bg='red')
    stop_window.attributes('-topmost', True)
    stop_window.resizable(False, False)
    
    # Empêche la fermeture par la croix
    def on_closing():
        pass
    
    stop_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    label = tk.Label(stop_window, text="🛑 PRANK EN COURS!", bg='red', fg='white', font=('Arial', 16, 'bold'))
    label.pack(pady=10)
    
    info_label = tk.Label(stop_window, text="Appuie pour arrêter", bg='red', fg='white', font=('Arial', 10))
    info_label.pack(pady=5)
    
    button = tk.Button(stop_window, text="ARRÊTER LE CHAOS", command=stop_chaos, 
                       bg='yellow', fg='red', font=('Arial', 12, 'bold'), padx=20, pady=10)
    button.pack(pady=10)
    
    stop_window.mainloop()

def main():
    """Fonction principale"""
    print("🎮 PRANK CHAOS DÉMARRÉ!")
    print("Une fenêtre STOP va s'afficher...")
    print("Actions: Fermeture / Déplacement / Curseur / Écran noir")
    print("Ne peut pas être fermée! 😈")
    
    # Lance la boucle de chaos dans un thread
    chaos_thread = threading.Thread(target=chaos_loop, daemon=True)
    chaos_thread.start()
    
    # Crée le bouton STOP
    create_stop_button()

if __name__ == "__main__":
    main()
