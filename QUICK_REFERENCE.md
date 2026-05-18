# 🎯 Nova Assistant - Quick Reference Cheat Sheet

## 📌 Most Common Commands

### WhatsApp Messaging 💬
```
Single Line:
├─ "WhatsApp kholo Mikku ko 'hi' bhejo"
├─ "Message Sameer go 'kaise ho'"
└─ "wa mein Priya ko 'good morning' send kar"

Multi-Step:
├─ Step 1: "WhatsApp kholo"
├─ Step 2: "Mikku ko"
└─ Step 3: "Hello brother"
```

### YouTube Music/Video 🎵
```
Single Line:
├─ "YouTube par Arijit Singh play kar"
├─ "YouTube mein 'Shape of You' gana baja"
└─ "Play some Bollywood music"

Multi-Step:
├─ Step 1: "YouTube kholo"
└─ Step 2: "Arijit Singh play kar"
```

### Google Search 🔍
```
Single Line:
├─ "Google par machine learning dhundo"
├─ "Search karo Python tutorial"
└─ "Google mein 'best pizza near me'"
```

### App Opening 🔧
```
├─ "Chrome kholo"
├─ "Notepad open kar"
├─ "Calculator kholo"
├─ "Task manager open"
└─ "Camera kholo"
```

---

## 🧠 Memory State Quick Reference

### What Gets Remembered
```
current_app      → WhatsApp, YouTube, Google, etc.
intent           → send_message, play, open, search
contact          → Mikku, Sameer, Priya, etc.
pending_message  → Actual message/song/search term
```

### How to Trigger Each
```
CURRENT_APP:     Say app name → "WhatsApp", "YouTube", "Google"
INTENT:          Say action verb → "message", "bhejo", "play", "kholo"
CONTACT:         Say name → "Mikku", "Sameer"
PENDING_MESSAGE: Say content → "hello", "Arijit Singh", "ML tutorial"
```

---

## 🔑 Key Phrases

### App Names (be specific)
```
✅ "WhatsApp"    ✅ "YouTube"    ✅ "Google"
✅ "Chrome"      ✅ "Notepad"    ✅ "Camera"
```

### Action Words (intent triggers)
```
Message:    "message", "bhejo", "send", "text"
Play:       "play", "sun", "baja", "music"
Open:       "open", "kholo", "launch", "start"
Search:     "search", "dhundo", "find", "lookup"
```

### Contact Keywords
```
├─ Use exact names from CONTACTS:
├─ "Mikku"
├─ "Sameer Goswami"  or  "Sameer"
└─ Add more: Edit CONTACTS in e.py
```

---

## 📝 Common Patterns

### Pattern 1: Full Info in One Line
```
Structure: App + Contact + Message
Example: "WhatsApp Mikku ko 'hi' bhejo"
Result: ✅ Immediate action
```

### Pattern 2: Partial Info Needs Prompts
```
Structure: Intent only
Example: "Message bhejo"
Nova Asks: "Who?"  →  You: "Mikku"  →  "What?"  →  You: "Hi"
Result: ✅ Proceeds after info collected
```

### Pattern 3: Multiple Steps
```
Structure: One piece at a time
Step 1: App → "WhatsApp kholo"
Step 2: Contact → "Mikku ko"  
Step 3: Content → "Hello brother"
Result: ✅ Remembers each step automatically
```

---

## ⚡ Pro Tips

### Tip 1: Be Specific
```
❌ "Message someone"
✅ "Message Mikku"  (name specified)

❌ "Open something"
✅ "Open WhatsApp"  (app specified)
```

### Tip 2: Use Keywords
```
Memory works best with these keywords:
├─ "kholo" (open)
├─ "bhejo" (send)
├─ "play" (YouTube)
├─ "dhundo" (search)
└─ "ko" (to/whom)
```

### Tip 3: Match Contact Names Exactly
```
If CONTACTS has "Sameer Goswami":
✅ "Sameer Goswami ko message karo"
✅ "Sameer ko message karo"  (partial also works)
❌ "Sam ko message karo"  (too short/different)
```

---

## 🎤 Voice Tips for Better Recognition

### Do's ✅
```
✅ Speak clearly and slowly
✅ Use natural pauses
✅ Say complete words
✅ Wait for prompts
✅ One action per command
```

### Don'ts ❌
```
❌ Don't rush words together
❌ Don't use slang/abbreviations
❌ Don't mumble or whisper
❌ Don't interrupt Nova's responses
❌ Don't send multiple commands quickly
```

---

## 🔄 Memory Lifecycle

### Execution Cycle
```
1. Listen to user input
        ↓
2. Detect app, intent, contact, message
        ↓
3. Check if complete
        ├─ YES → Execute task ✅
        └─ NO → Ask for missing info → Go to Step 2
        
4. Task complete → Clear some memory
             ├─ "pending_message" = NULL (ready for next)
             ├─ "contact" = Keep (for next message)
             └─ "app" = Keep (unless switched)
```

### Memory Persistence
```
Multi-Step Example:
Step 1: "WhatsApp kholo"
  Memory: app=whatsapp, contact=null, message=null
  
Step 2: "Mikku ko"
  Memory: app=whatsapp ✓, contact=mikku ✓, message=null
  
Step 3: "Hi"
  Memory: app=whatsapp ✓, contact=mikku ✓, message=hi ✓
  EXECUTE! ✅
```

---

## 🛠️ Customization Quick Guide

### Add New Contact
In `e.py`, find `CONTACTS = {`:
```python
CONTACTS = {
    "mikku": "+918085055261",
    "your_name": "+919876543210",  ← Add here
}
```

### Add New App Keyword
In `detect_app()` function:
```python
"whatsapp": ["whatsapp", "wa", "message"],
"instagram": ["insta", "ig"],  ← Add new app
```

### Add New Intent Keyword
In `detect_intent()` function:
```python
"send_message": ["message", "bhejo"],
"call": ["call", "ring"],  ← Add new intent
```

---

## 🚨 Quick Troubleshooting

### Problem: Contact Not Found
```
Error: "I don't have a contact named..."
Fix: Check CONTACTS dict, use exact spelling
```

### Problem: Intent Not Recognized
```
Error: Nothing happens
Fix: Use standard keywords: "message", "play", "open"
```

### Problem: App Takes Time to Load
```
Issue: Message sent before app opens
Fix: System waits 5 seconds. If slow net, wait more.
```

### Problem: Speech Not Recognized
```
Error: "None" returned
Fix: Speak more clearly, not too fast
```

---

## 📱 Complete Voice Command Examples

### Example Set 1: Messaging
```
1. "WhatsApp kholo Mikku ko 'hi' bhejo"
2. "Message Sameer 'good morning'"
3. "Priya ko text kar 'see you soon'"
```

### Example Set 2: YouTube
```
1. "YouTube par Arijit Singh play kar"
2. "Sun 'Blinding Lights' YouTube pe"
3. "Play some Bollywood hits"
```

### Example Set 3: Multi-Step
```
Step 1: "WhatsApp"
Step 2: "Mikku"
Step 3: "I'll be late"
→ Message sent!
```

### Example Set 4: System Commands
```
1. "Volume up" → Increase 25%
2. "Brightness down" → Decrease 25%
3. "Screenshot" → Save to file
4. "Close window" → Alt+F4
5. "Minimize" → Show desktop
```

---

## 📊 Memory Visualization

### Single Command Flow
```
Input: "WhatsApp Mikku 'hi' bhejo"
         ↓
      App: whatsapp ✓
      Intent: send_message ✓
      Contact: mikku ✓
      Message: hi ✓
         ↓
       EXECUTE ✅
```

### Multi-Step Flow
```
Step 1: "WhatsApp"
  app: whatsapp ✓ | intent: - | contact: - | message: -

Step 2: "Mikku ko"
  app: whatsapp ✓ | intent: send_message ✓ | contact: mikku ✓ | message: -

Step 3: "Hi bro"
  app: whatsapp ✓ | intent: send_message ✓ | contact: mikku ✓ | message: hi bro ✓
         ↓
       EXECUTE ✅
```

---

## 🎯 Command Categories

| Category | Keywords | Example |
|----------|----------|---------|
| **Messaging** | message, bhejo, send | "Message Mikku 'hello'" |
| **Media** | play, sun, baja | "Play Arijit Singh" |
| **Search** | search, dhundo, find | "Search 'Python'" |
| **Apps** | open, kholo, launch | "Open WhatsApp" |
| **System** | volume, brightness, close | "Volume up" |
| **Camera** | camera, photo, click | "Click photo" |

---

**📌 Save this for quick reference while using Nova!**
