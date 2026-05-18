import os
import pyautogui
import webbrowser
import psutil
import datetime
import screen_brightness_control as sbc
import socket
import cv2
import threading
import time
import pywhatkit


# Minimal runtime stubs to allow safe syntax and smoke testing
def speak(text):
    print(f"[speak] {text}")


def take_command():
    # Stub for voice input - return a neutral value
    return "none"


def get_ai_response(query):
    return "(stub) I don't have a detailed response in test mode."


# Camera state stubs used by the command handlers
cam_active = False
current_frame = None


def camera_stream():
    global cam_active, current_frame
    # Simple non-blocking stub: keep looping while camera is active
    while cam_active:
        time.sleep(0.5)




def execute_task(query):
    query = query.lower()

    # 1. System Controls (Inhe AI se pehle check karna zaroori hai)
 # --- 1. PEHLE GOOGLE KHOLNE KE LIYE ---
    if "open google" in query or "google kholo" in query:
        speak("Opening Google for you, Sagar.")
        webbrowser.open("https://www.google.com")

   
 # --- GOOGLE PAR USI TAB MEIN SEARCH ---
    elif "search on google" in query or "google par dhundo" in query:
        speak("What should I search for you?")
        search_query = take_command()
        
        if search_query != "none":
            speak(f"Searching for {search_query}")
            
            # 1. Google Chrome/Browser par focus karke address bar par jao (Ctrl + L)
            pyautogui.hotkey('ctrl', 'l') 
            
            # 2. Purana address delete karke naya query likho
            pyautogui.write(search_query, interval=0.1) 
            
            # 3. Enter dabao search karne ke liye
            pyautogui.press('enter')
        else:
            speak("I didn't hear the query.")

    # --- YOUTUBE PAR USI TAB MEIN SEARCH ---elif "search on youtube" in query or "youtube par search" in query:
        speak("What do you want to watch?")
        video_query = take_command()
        
        if video_query != "none":
            speak(f"Searching and playing {video_query} in this tab.")
            
            # 1. YouTube ki search bar par focus karo ('/' key press karke)
            pyautogui.press('/') 
            time.sleep(0.5)
            
            # 2. Purana text clear karke naya song name type karo
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(video_query, interval=0.1)
            pyautogui.press('enter')
            
            # 3. Wait karein jab tak results load na ho jayein (Internet slow ho toh 5-7 sec karein)
            import time
            time.sleep(5) 
            
            # 4. Same tab mein first video play karne ka sabse fast shortcut:
            # Pehle focus ko search bar se hatane ke liye 'Esc' dabayein
            pyautogui.press('esc')
            time.sleep(0.5)
            
            # 5. YouTube ke layout mein pehle video par jane ke liye 2 baar 'Tab' dabayein
            # Phir 'Enter' dabayein video play karne ke liye
            for i in range(2): 
                pyautogui.press('tab')
                time.sleep(0.3)
            
            pyautogui.press('enter')
            speak("Playing the first video for you.")
            
        else:
            speak("I didn't hear the song name.")
    # --- SIMILAR LOGIC FOR YOUTUBE ---
    elif "open youtube" in query or "youtube kholo" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "search on youtube" in query or "youtube par search" in query:
        speak("What do you want to watch?")
        video_query = take_command()
        if video_query != "none":
            speak(f"Searching for {video_query} on YouTube.")
            pywhatkit.playonyt(video_query)

    elif "youtube" in query:
        speak("Opening YouTube, sir.")
        webbrowser.open("https://www.youtube.com")
    
    elif "play" in query:
        song = query.replace("play", "").strip()
        speak(f"Sure, playing {song} for you.")
        pywhatkit.playonyt(song)

# --- 100% WORKING VOLUME CONTROL (NO ERRORS) ---
  # --- SMART VOLUME CONTROL ---
    # Agar query mein 'volume' hai AUR badhane ka koi keyword hai
    elif "volume" in query and ("up" in query or "increase" in query or "badhao" in query or "high" in query):
        for i in range(5):
            pyautogui.press("volumeup")
        speak("Done!")

    # Agar query mein 'volume' hai AUR ghatane ka koi keyword hai
    elif "volume" in query and ("down" in query or "decrease" in query or "kam" in query or "low" in query):
        for i in range(5):
            pyautogui.press("volumedown")
        speak("Reduced.")

    elif "mute" in query or "chup" in query:
        pyautogui.press("volumemute")
        speak("Muted.")
    # Brightness
  # --- SMART BRIGHTNESS CONTROL ---
    elif "brightness" in query or "light" in query or "display" in query:
        try:
            current_brightness = sbc.get_brightness()[0]
            
            # Agar badhane ka koi keyword mile
            if "up" in query or "increase" in query or "badhao" in query or "jyada" in query:
                new_brightness = min(current_brightness + 25, 100)
                sbc.set_brightness(new_brightness)
                speak(f"Brightness increased to {new_brightness} percent.")
            
            # Agar kam karne ka koi keyword mile
            elif "down" in query or "decrease" in query or "kam" in query or "low" in query:
                new_brightness = max(current_brightness - 25, 0)
                sbc.set_brightness(new_brightness)
                speak(f"Brightness decreased to {new_brightness} percent.")
                
        except Exception:
            speak("Sorry Sagar, I can't control brightness on this monitor.")

    # --- SCREENSHOT ---
    elif "screenshot" in query or "screen capture" in query:
        pyautogui.screenshot("nova_screenshot.png")
        speak("Done! Screenshot saved.")

    # --- EXIT ---
    elif "stop" in query or "exit" in query or "goodbye" in query or "bye" in query:
        speak("Goodbye Sagar! Have a beautiful day.")
        return "Goodbye"

# --- STEP 1: CAMERA OPEN KARO ---
    elif "camera open" in query or "camera kholo" in query or "camera kholo" in query or "kholo camera" in query or "yaar camera"  in query:
        if not cam_active:
            cam_active = True
            threading.Thread(target=camera_stream).start()
            speak("Camera open ho gaya hai Sagar. Main screen par preview dekh sakte hain.")
        else:
            speak("Camera pehle se hi open hai.")

    # --- STEP 2: PHOTO CLICK KARO (VOICE SE) ---
    elif "click" in query or "photo khicho" in query:
        if cam_active and current_frame is not None:
            import time
            file_name = f"photo_{int(time.time())}.jpg"
            cv2.imwrite(file_name, current_frame)
            speak(f"Smile! Photo click ho gayi aur {file_name} ke naam se save ho gayi hai.")
        else:
            speak("Sagar, pehle camera kholne ko boliye tabhi toh photo khichungi!")

    # --- STEP 3: CAMERA BAND KARO ---
    elif "close camera" in query or "camera band" in query:
        if cam_active:
            cam_active = False
            speak("Theek hai Sagar, camera band kar rahi hoon.")
        else:
            speak("Camera toh pehle se hi band hai.")







    # 2. AI Response (Agar upar ka koi command match na ho)
    else:
        print("Thinking...")
        answer = get_ai_response(query)
        speak(answer)
    # --- 1. SYSTEM INFO (Start with IF) ---
    if "battery" in query:
        battery = psutil.sensors_battery()
        return f"Battery is at {battery.percent} percent."
    
    elif "cpu" in query:
        usage = psutil.cpu_percent()
        return f"CPU usage is at {usage} percent."

    elif "time" in query:
        return f"It's {datetime.datetime.now().strftime('%I:%M %p')}"

    elif "date" in query:
        return f"Today is {datetime.datetime.now().strftime('%d %B %Y')}"

    # --- 2. SYSTEM CONTROLS ---
    elif "screenshot" in query:
        pyautogui.screenshot("nova_screenshot.png")
        return "Screenshot saved successfully."


    elif "mute" in query:
        pyautogui.press("volumemute")
        return "System muted."

    elif "brightness" in query:
        curr = sbc.get_brightness()[0]
        if "increase" in query or "badhao" in query:
            sbc.set_brightness(min(curr + 25, 100))
            return "Brightness increased."
        else:
            sbc.set_brightness(max(curr - 25, 0))
            return "Brightness decreased."

    # --- 3. WINDOW AUTOMATION ---
    elif "minimize" in query:
        pyautogui.hotkey('win', 'd')
        return "Done."

    elif "maximize" in query:
        pyautogui.hotkey('win', 'up')
        return "Maximized."

    elif "close window" in query or "close app" in query:
        pyautogui.hotkey('alt', 'f4')
        return "Application closed."

    elif "switch tab" in query:
        pyautogui.hotkey('ctrl', 'tab')
        return "Tab switched."

    elif "task manager" in query:
        pyautogui.hotkey('ctrl', 'shift', 'esc')
        return "Opening Task Manager."

    # --- 4. OPEN APPS ---
    elif "open notepad" in query:
        os.system("notepad")
        return "Notepad is ready."

    elif "open calculator" in query:
        os.system("calc")
        return "Opening Calculator."

    elif "open cmd" in query:
        os.system("start cmd")
        return "Command Prompt opened."

    elif "open chrome" in query:
        os.system("start chrome")
        return "Chrome opened."

    # --- 5. WEB TASKS ---
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    # # Agar kuch match nahi hua toh return None
    # return None