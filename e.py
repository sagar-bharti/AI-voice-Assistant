import speech_recognition as sr
import webbrowser
from google import genai
import pywhatkit
import pygame
import os
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import threading
import time

import edge_tts
import asyncio
import nest_asyncio
from gtts import gTTS
import re
import datetime


# =====================================================
# 🤖 NOVA - CONTEXT-AWARE VOICE ASSISTANT
# =====================================================
# 
# 🎯 FEATURES:
# ✔️ Single command execution
# ✔️ Multi-step conversation with memory
# ✔️ Intent + Context detection
# ✔️ Smart auto-completion
#
# 📝 EXAMPLE USAGE:
#
# Case 1️⃣ - SINGLE COMMAND (Ek hi line):
# "WhatsApp kholo Mikku ko message kar do 'mai kal college nahi aaunga'"
# → WhatsApp opens
# → Message sends to Mikku
#
# Case 2️⃣ - STEP BY STEP (Multiple commands):
# "WhatsApp kholo"
# → WhatsApp opens, memory remembers intent
# 
# "Mikku ko message bhejo"
# → Memory knows it's WhatsApp, detects contact
#
# "mai kal college nahi aaunga"
# → Memory knows app, contact, and gets message
# → Message sends automatically!
#
# 🧠 MEMORY TRACKS:
# - current_app: Konsa app work kar raha hai
# - intent: User ka goal kya hai (send_message, play, open, etc)
# - contact: Kisko message/call karna hai
# - pending_message: Bhejne wala message
#
# =====================================================


# --- Error se bachne ke liye nest_asyncio zaroori hai ---
nest_asyncio.apply()


# --- Configuration (FIXED: New google-genai SDK syntax) ---
client = genai.Client(api_key="AIzaSyARlNdrSqS302FybObI_9REvJaquVCrub4")


# --- FREE INDIAN VOICE (Swara) ---
# VOICE = "hi-IN-SwaraNeural"
VOICE = "en-US-EmmaMultilingualNeural"


# =====================================================
# 🔊 SPEAK FUNCTION
# =====================================================

def speak(text):
    print(f"Nova: {text}")

    async def _speak_async():
        output_file = "nova_edge.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)

        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        if os.path.exists(output_file):
            os.remove(output_file)

    try:
        asyncio.run(_speak_async())
    except Exception as e:
        print(f"Speaking Error: {e}")


# =====================================================
# 🎙️ TAKE COMMAND FUNCTION
# =====================================================

def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=6)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"Sagar said: {query}\n")
    except Exception:
        return "none"
    return query.lower()


# =====================================================
# 🤖 AI RESPONSE FUNCTION (FIXED: New SDK syntax)
# =====================================================

def get_ai_response(user_text):
    try:
        prompt = (f"You are a young, sweet, and cheerful girl named Nova. "
                  f"Use friendly words like 'Sure!', 'Of course!', 'I'd love to help'. "
                  f"Keep your responses very warm and brief: {user_text}")

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm a bit sleepy, can you repeat that?"


# =====================================================
# 📇 CONTACTS
# =====================================================

CONTACTS = {
    "sameer goswami": "+919893558503",
    "mikku": "+918085055261",
}


# =====================================================
# 🧠 CONTEXT-AWARE MEMORY SYSTEM
# =====================================================

assistant_memory = {
    "current_app": None,
    "intent": None,
    "contact": None,
    "pending_message": None,
    "last_action": None,
    "retry_count": 0
}


def reset_memory():
    global assistant_memory
    assistant_memory = {
        "current_app": None,
        "intent": None,
        "contact": None,
        "pending_message": None,
        "last_action": None,
        "retry_count": 0
    }


def detect_app(query):
    query = query.lower()
    apps = {
        "whatsapp": ["whatsapp", "wa", "message", "text", "bhejo"],
        "youtube": ["youtube", "yt", "play", "music", "song", "video"],
        "google": ["google", "search", "dhundo"],
        "chrome": ["chrome", "browser", "internet"],
        "notepad": ["notepad", "note"],
        "calculator": ["calculator", "calc", "ganit"],
    }
    for app, keywords in apps.items():
        for keyword in keywords:
            if keyword in query:
                assistant_memory["current_app"] = app
                return app
    return None


def detect_intent(query):
    query = query.lower()
    intents = {
        "send_message": ["message", "bhejo", "send", "text", "tipo"],
        "open_app": ["open", "kholo", "launch", "chalu"],
        "search": ["search", "dhundo", "find", "ढूंढ"],
        "play": ["play", "sun", "suno", "chalao"],
        "close": ["close", "band", "karo", "exit"],
    }
    for intent_name, keywords in intents.items():
        for keyword in keywords:
            if keyword in query:
                assistant_memory["intent"] = intent_name
                return intent_name
    return None


def detect_contact(query):
    query = query.lower()
    for contact_name in CONTACTS.keys():
        if contact_name in query:
            assistant_memory["contact"] = contact_name
            return contact_name
    return None


def extract_name_message(query):
    query = query.lower()
    pattern = r"([a-zA-Z ]+)\sko\s(.+)"
    match = re.search(pattern, query)
    if match:
        name = match.group(1).strip()
        message = match.group(2).strip()
        return name, message
    pattern2 = r"([a-zA-Z ]+)\sko"
    match2 = re.search(pattern2, query)
    if match2:
        name = match2.group(1).strip()
        return name, ""
    return "", ""


def extract_message(query):
    query = query.lower()
    name, message = extract_name_message(query)
    if message:
        assistant_memory["pending_message"] = message
        return message
    if assistant_memory["intent"] == "send_message":
        if assistant_memory["contact"]:
            filtered_msg = query
            for keyword in ["message", "bhejo", "send", "text", "tipo", "ko", "par"]:
                filtered_msg = filtered_msg.replace(keyword, "").strip()
            if filtered_msg and len(filtered_msg) > 2:
                assistant_memory["pending_message"] = filtered_msg
                return filtered_msg
    return None


def extract_contact_name(text):
    text = text.lower()
    keywords = ["ko", "call", "message", "msg", "par"]
    words = text.split()
    for i, word in enumerate(words):
        if word in keywords and i > 0:
            return words[i - 1]
    return None


def ask_for_missing_info():
    global assistant_memory
    print("⚠️ Incomplete information detected, asking user...")

    if assistant_memory["intent"] == "send_message":
        if not assistant_memory["contact"]:
            speak("Which contact should I send the message to?")
            response = take_command()
            if response != "none":
                detect_contact(response)

        if not assistant_memory["pending_message"]:
            if assistant_memory["contact"]:
                speak(f"What message should I send to {assistant_memory['contact']}?")
            else:
                speak("What message should I send?")
            response = take_command()
            if response != "none":
                extract_message(response)

    elif assistant_memory["intent"] == "play":
        if not assistant_memory["pending_message"]:
            speak("What song or video should I play?")
            response = take_command()
            if response != "none":
                assistant_memory["pending_message"] = response

    elif assistant_memory["intent"] == "open_app":
        if not assistant_memory["current_app"]:
            speak("Which app should I open?")
            response = take_command()
            if response != "none":
                detect_app(response)


def process_with_memory(query):
    detect_app(query)
    detect_intent(query)
    detect_contact(query)
    extract_message(query)

    print("\n📊 Memory Status:")
    print(f"   App: {assistant_memory['current_app']}")
    print(f"   Intent: {assistant_memory['intent']}")
    print(f"   Contact: {assistant_memory['contact']}")
    print(f"   Message: {assistant_memory['pending_message']}")
    print()

    has_enough_info = (
        assistant_memory["current_app"] is not None or
        assistant_memory["intent"] is not None
    )
    return has_enough_info


# =====================================================
# 📱 WHATSAPP FUNCTIONS
# =====================================================

def send_whatsapp_by_name(name, message):
    try:
        speak(f"Opening WhatsApp to send message to {name}")

        whatsapp_paths = [
            "C:\\Users\\samee\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
            os.path.expandvars(r"%USERPROFILE%\AppData\Local\WhatsApp\WhatsApp.exe"),
            r"C:\Program Files\WhatsApp\WhatsApp.exe",
            r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe",
        ]

        whatsapp_opened = False
        for path in whatsapp_paths:
            if os.path.exists(path):
                os.startfile(path)
                whatsapp_opened = True
                speak("WhatsApp opening...")
                time.sleep(5)
                break

        if not whatsapp_opened:
            speak("WhatsApp not found. Please open it manually and try again.")
            return False

        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.write(name)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(1.5)
        pyautogui.write(message)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "enter")
        time.sleep(1)

        speak(f"Message sent to {name}")
        return True

    except Exception as e:
        speak(f"Sorry, I couldn't send the message to {name}")
        print(f"Error in send_whatsapp_by_name: {e}")
        return False


def send_whatsapp_message(phone, message):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 1
    speak(f"Sending message: {message}")
    pywhatkit.sendwhatmsg(phone, message, hour, minute)


def try_execute_task():
    global assistant_memory

    # WhatsApp message send
    if (assistant_memory["current_app"] == "whatsapp" and
            assistant_memory["intent"] == "send_message" and
            assistant_memory["contact"] and
            assistant_memory["pending_message"]):
        try:
            contact = assistant_memory["contact"]
            message = assistant_memory["pending_message"]
            speak(f"Sending message to {contact}")
            success = send_whatsapp_by_name(contact, message)
            if success:
                speak("Message sent successfully!")
                assistant_memory["last_action"] = "message_sent"
                reset_memory()
                return True
            else:
                speak("Sorry, I couldn't send the message. Please try again.")
                assistant_memory["retry_count"] += 1
                return False
        except Exception as e:
            print(f"Error executing WhatsApp task: {e}")
            speak("Something went wrong.")
            assistant_memory["retry_count"] += 1
            return False

    # WhatsApp open only
    elif (assistant_memory["current_app"] == "whatsapp" and
          assistant_memory["intent"] == "open_app"):
        try:
            speak("Opening WhatsApp for you.")
            webbrowser.open("https://web.whatsapp.com")
            reset_memory()
            return True
        except Exception as e:
            print(f"Error opening WhatsApp: {e}")
            return False

    # YouTube open
    elif (assistant_memory["current_app"] == "youtube" and
          assistant_memory["intent"] == "open_app"):
        try:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            reset_memory()
            return True
        except Exception as e:
            print(f"Error opening YouTube: {e}")
            return False

    # YouTube play
    elif (assistant_memory["current_app"] == "youtube" and
          assistant_memory["intent"] == "play" and
          assistant_memory["pending_message"]):
        try:
            song = assistant_memory["pending_message"]
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
            reset_memory()
            return True
        except Exception as e:
            print(f"Error playing on YouTube: {e}")
            speak("Couldn't play the song.")
            return False

    return False


def try_execute_with_prompts(query):
    has_info = process_with_memory(query)
    if not has_info:
        return False

    if try_execute_task():
        print("✅ Task executed successfully!")
        return True

    if assistant_memory["intent"]:
        print("🤔 Detecting missing information...")
        ask_for_missing_info()
        if try_execute_task():
            print("✅ Task executed after collecting info!")
            return True

    return False


# =====================================================
# ⚡ SPLIT COMMANDS
# =====================================================

def split_commands(query):
    separators = [" and ", " aur ", " then ", " phir "]
    commands = [query]
    for sep in separators:
        temp = []
        for cmd in commands:
            temp.extend(cmd.split(sep))
        commands = temp
    return [c.strip() for c in commands if c.strip()]


# =====================================================
# 🎮 SINGLE COMMAND EXECUTOR
# =====================================================

def execute_single_command(cmd):

    # GOOGLE OPEN
    if "google" in cmd and "open" in cmd:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True

    # SEND MESSAGE (check before whatsapp open)
    if "message" in cmd or "bhejo" in cmd:
        name, message = extract_name_message(cmd)
        print("Extracted Name:", name)
        print("Extracted Message:", message)

        if name != "":
            if message == "":
                speak(f"What should I send to {name}?")
                message = take_command()
            if message != "none":
                success = send_whatsapp_by_name(name, message)
                if not success:
                    if name in CONTACTS:
                        send_whatsapp_message(CONTACTS[name], message)
            return True
        else:
            speak("I couldn't find the name")
            return True

    # WHATSAPP OPEN (only if not a message command)
    if "whatsapp" in cmd and "message" not in cmd and "bhejo" not in cmd:
        name = extract_contact_name(cmd)
        if name and name in CONTACTS:
            webbrowser.open("https://web.whatsapp.com")
            speak(f"Opening WhatsApp chat with {name}")
            return True
        else:
            if "open" in cmd or "kholo" in cmd:
                speak("Opening WhatsApp for you.")
                webbrowser.open("https://web.whatsapp.com")
            return True

    return False


# =====================================================
# 📷 CAMERA SETUP
# =====================================================

cam_active = False
current_frame = None


def camera_stream():
    global cam_active, current_frame
    cap = cv2.VideoCapture(0)
    while cam_active:
        ret, frame = cap.read()
        if ret:
            current_frame = frame
            cv2.imshow("Nova Live Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam_active = False
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Camera Closed Successfully.")


# =====================================================
# 🚀 MAIN LOOP
# =====================================================

speak("Hey Sagar! Ready to dive in? Let me know how I can help you get things done today.")

while True:
    query = take_command()

    if query == "none":
        continue

    print(f"📝 User Command: {query}")

    # ===== STEP 1: CONTEXT-AWARE MEMORY SYSTEM =====
    task_completed = try_execute_with_prompts(query)

    if task_completed:
        print("✅ Task completed via Memory System!")
        continue

    # ===== STEP 2: INDIVIDUAL COMMANDS =====
    commands = split_commands(query)
    handled_any = False

    for cmd in commands:
        handled = execute_single_command(cmd)
        if handled:
            handled_any = True

    # --- GOOGLE OPEN ---
    if "open google" in query or "google kholo" in query:
        speak("Opening Google for you, Sagar.")
        webbrowser.open("https://www.google.com")

    # --- GOOGLE SEARCH IN SAME TAB ---
    elif "search on google" in query or "google par dhundo" in query:
        speak("What should I search for you?")
        search_query = take_command()
        if search_query != "none":
            speak(f"Searching for {search_query}")
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.write(search_query, interval=0.1)
            pyautogui.press('enter')
        else:
            speak("I didn't hear the query.")

    # --- YOUTUBE SEARCH IN SAME TAB ---
    elif "search on youtube" in query or "youtube par search" in query:
        speak("What do you want to watch?")
        video_query = take_command()
        if video_query != "none":
            speak(f"Searching and playing {video_query} in this tab.")
            pyautogui.press('/')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            pyautogui.write(video_query, interval=0.1)
            pyautogui.press('enter')
            time.sleep(5)
            pyautogui.press('esc')
            time.sleep(0.5)
            for i in range(2):
                pyautogui.press('tab')
                time.sleep(0.3)
            pyautogui.press('enter')
            speak("Playing the first video for you.")
        else:
            speak("I didn't hear the song name.")

    # --- YOUTUBE OPEN ---
    elif "open youtube" in query or "youtube kholo" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "youtube" in query:
        speak("Opening YouTube, sir.")
        webbrowser.open("https://www.youtube.com")

    # --- PLAY SONG ---
    elif "play" in query:
        song = query.replace("play", "").strip()
        speak(f"Sure, playing {song} for you.")
        pywhatkit.playonyt(song)

    # --- VOLUME CONTROL ---
    elif "volume" in query and ("up" in query or "increase" in query or "badhao" in query or "high" in query):
        for i in range(5):
            pyautogui.press("volumeup")
        speak("Done!")

    elif "volume" in query and ("down" in query or "decrease" in query or "kam" in query or "low" in query):
        for i in range(5):
            pyautogui.press("volumedown")
        speak("Reduced.")

    elif "mute" in query or "chup" in query:
        pyautogui.press("volumemute")
        speak("Muted.")

    # --- BRIGHTNESS CONTROL ---
    elif "brightness" in query or "light" in query or "display" in query:
        try:
            current_brightness = sbc.get_brightness()[0]
            if "up" in query or "increase" in query or "badhao" in query or "jyada" in query:
                new_brightness = min(current_brightness + 25, 100)
                sbc.set_brightness(new_brightness)
                speak(f"Brightness increased to {new_brightness} percent.")
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
        break

    # --- CAMERA OPEN ---
    elif "open camera" in query or "camera kholo" in query or "kholo camera" in query or "yaar camera" in query:
        if not cam_active:
            cam_active = True
            threading.Thread(target=camera_stream).start()
            speak("Camera open ho gaya hai Sagar.")
        else:
            speak("Camera pehle se hi open hai.")

    # --- PHOTO CLICK ---
    elif "click" in query or "photo khicho" in query:
        if cam_active and current_frame is not None:
            file_name = f"photo_{int(time.time())}.jpg"
            cv2.imwrite(file_name, current_frame)
            speak(f"Smile! Photo click ho gayi aur {file_name} ke naam se save ho gayi hai.")
        else:
            speak("Sagar, pehle camera kholne ko boliye tabhi toh photo khichungi!")

    # --- CAMERA CLOSE ---
    elif "close camera" in query or "camera band" in query:
        if cam_active:
            cam_active = False
            speak("Theek hai Sagar, camera band kar rahi hoon.")
        else:
            speak("Camera toh pehle se hi band hai.")

    # --- WINDOW CONTROLS ---
    elif "minimise" in query:
        pyautogui.hotkey('win', 'd')
        speak("Done, minimized everything.")

    elif "maximize" in query:
        pyautogui.hotkey('win', 'up')
        speak("Maximized.")

    elif "close window" in query or "close app" in query:
        pyautogui.hotkey('alt', 'f4')
        speak("Application closed.")

    elif "switch tab" in query:
        pyautogui.hotkey('ctrl', 'tab')
        speak("Tab switched.")

    elif "task manager" in query:
        pyautogui.hotkey('ctrl', 'shift', 'esc')
        speak("Opening Task Manager.")

    # --- OPEN APPS ---
    elif "open notepad" in query:
        os.system("notepad")
        speak("Notepad is ready.")

    elif "open calculator" in query:
        os.system("calc")
        speak("Opening Calculator.")

    elif "open cmd" in query:
        os.system("start cmd")
        speak("Command Prompt opened.")

    elif "open chrome" in query:
        os.system("start chrome")
        speak("Chrome opened.")

    # --- WHATSAPP MESSAGE (fallback) ---
    elif "send message to" in query or "ko" in query:
        try:
            if "send message to" in query:
                contact_name = query.split("send message to")[1].strip()
            else:
                contact_name = query.split("ko")[1].strip()
            if contact_name in CONTACTS:
                speak(f"What message do you want to send to {contact_name}?")
                message = take_command()
                if message != "none":
                    send_whatsapp_message(CONTACTS[contact_name], message)
                else:
                    speak("I didn't catch the message.")
            else:
                speak(f"I don't have a contact named {contact_name}.")
        except Exception as e:
            speak("Sorry, I couldn't process your request.")
            print(e)

    # --- AI RESPONSE (fallback for everything else) ---
    elif not handled_any:
        print("Thinking...")
        answer = get_ai_response(query)
        speak(answer)