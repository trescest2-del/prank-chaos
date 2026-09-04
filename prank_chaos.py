import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import subprocess
from PIL import Image, ImageDraw
import os

# Variables globales
running = True
app_positions = {}
stop_window = None

def get_all_windows():
    """Récupère toutes les fenêtres ouvertes"""
    try:
        result = subprocess.run(['tasklist', '/v'], capture_output=True, text=True)
        return result.stdout
    except:
        return []

def save_window_positions():
    """Sauvegarde les positions des fenêtres"""
    global app_positions
    try:
        result = subprocess.run(['powershell', '-Command', 
            'Get-Process | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object ProcessName, MainWindowHandle'],
            capture_output=True, text=True)
        app_positions = {}
    except:
        pass

def close_random_window():
    """Ferme une fenêtre aléatoire"""
    try:
        subprocess.run(['powershell', '-Command',
            'Get-Process | Where-Object {$_.MainWindowHandle -ne 0} | Get-Random | Stop-Process -Force'],
            capture_output=True)
    except:
        pass

def move_random_window():
    """Bouge une fenêtre aléatoire"""
    try:
        x = random.randint(100, 1200)
        y = random.randint(100, 600)
        subprocess.run(['powershell', '-Command',
            f'$window = Get-Process | Where-Object {{$_.MainWindowHandle -ne 0}} | Get-Random; ' +
            f'Add-Type -AssemblyName System.Windows.Forms; ' +
            f'[System.Windows.Forms.SendKeys]::SendWait("%{{UP}}")'],
            capture_output=True)
    except:
        pass

def move_cursor():
    """Bouge le curseur pendant 3 secondes"""
    try:
        pyautogui.FAILSAFE = False
        start_time = time.time()
        while time.time() - start_time < 3:
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            pyautogui.moveTo(x, y, duration=0.1)
            time.sleep(0.05)
    except:
        pass

def black_screen():
    """Écran noir pendant 5 secondes"""
    try:
        black_win = tk.Toplevel()
        black_win.attributes('-fullscreen', True)
        black_win.configure(bg='black')
        black_win.attributes('-topmost', True)
        black_win.update()
        
        time.sleep(5)
        black_win.destroy()
    except:
        pass

def show_virus_notification():
    """Affiche une notification VIRUS"""
    try:
        subprocess.run(['powershell', '-Command',
            '[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; ' +
            '[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; ' +
            '[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null; ' +
            '$APP_ID = "Python_Prank"; ' +
            '$template = @" ' +
            '<toast><visual><binding template="ToastText02"><text id="1">⚠️ VIRUS DÉTECTÉ!</text><text id="2">Ton PC est hacké! 😂</text></binding></visual></toast> ' +
            '"@; ' +
            '$xml = New-Object Windows.Data.Xml.Dom.XmlDocument; ' +
            '$xml.LoadXml($template); ' +
            '$toast = New-Object Windows.UI.Notifications.ToastNotification $xml; ' +
            '[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)'],
            capture_output=True)
    except:
        messagebox.showwarning("VIRUS!", "⚠️ VIRUS DÉTECTÉ!\nTon PC est hacké! 😂")

def chaos_loop():
    """Boucle principale du chaos"""
    global running
    
    save_window_positions()
    
    while running:
        if not running:
            break
            
        action = random.choice([1, 2, 3, 4, 5, 0, 0, 0])
        
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
                show_virus_notification()
        except:
            pass
        
        if running:
            time.sleep(random.randint(2, 6))

def stop_chaos():
    """Arrête le chaos"""
    global running
    running = False
    
    # Restaure les positions des fenêtres
    try:
        subprocess.run(['powershell', '-Command',
            'Get-Process | Where-Object {$_.MainWindowHandle -ne 0} | ForEach-Object {$_.MainWindowHandle}'],
            capture_output=True)
    except:
        pass
    
    messagebox.showinfo("Stopped!", "Le chaos s'arrête! 😎\nTout revient à la normale!")
    stop_window.destroy()

def create_stop_button():
    """Crée la fenêtre STOP indestructible"""
    global stop_window
    
    stop_window = tk.Tk()
    stop_window.title("🛑 STOP PRANK")
    stop_window.geometry("300x100")
    stop_window.configure(bg='red')
    stop_window.attributes('-topmost', True)
    stop_window.resizable(False, False)
    
    # Empêche la fermeture par la croix
    def on_closing():
        pass
    
    stop_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    label = tk.Label(stop_window, text="🛑 PRANK EN COURS!", bg='red', fg='white', font=('Arial', 16, 'bold'))
    label.pack(pady=10)
    
    button = tk.Button(stop_window, text="ARRÊTER LE CHAOS", command=stop_chaos, 
                       bg='yellow', fg='red', font=('Arial', 14, 'bold'), padx=20, pady=10)
    button.pack(pady=10)
    
    stop_window.mainloop()

def main():
    """Fonction principale"""
    print("🎮 PRANK CHAOS DÉMARRÉ!")
    print("Une fenêtre STOP va s'afficher...")
    print("Ne peut pas être fermée! 😈")
    
    # Lance la boucle de chaos dans un thread
    chaos_thread = threading.Thread(target=chaos_loop, daemon=True)
    chaos_thread.start()
    
    # Crée le bouton STOP
    create_stop_button()

if __name__ == "__main__":
    main()
