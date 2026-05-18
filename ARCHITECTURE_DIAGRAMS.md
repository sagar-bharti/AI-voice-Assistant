# 🎨 Context-Aware Voice Assistant - Visual Architecture Guide

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    NOVA VOICE ASSISTANT                      │
│                  (Context-Aware Edition)                     │
└──────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
           ┌────────▼────────┐   ┌──────▼──────────┐
           │  Voice Input    │   │  Text Input     │
           │  (Microphone)   │   │  (Test Mode)    │
           └────────┬────────┘   └──────┬──────────┘
                    │                    │
                    └────────┬───────────┘
                             │
                    ┌────────▼───────────┐
                    │ Main Loop          │
                    │ take_command()     │
                    └────────┬───────────┘
                             │
                    ┌────────▼────────────────────────┐
                    │ try_execute_with_prompts()      │
                    │ (NEW Memory System Pipeline)    │
                    └────────┬────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
      ┌───────▼─────────┐        ┌────────▼──────────┐
      │ process_with_   │        │ try_execute_      │
      │ memory()        │────┐   │ task()            │
      │                 │    │   │                   │
      │ • detect_app    │    │   │ (Check if all     │
      │ • detect_intent │    └──►│  data ready)      │
      │ • detect_contact│        │                   │
      │ • extract_msg   │        └────────┬──────────┘
      │ • print state   │                 │
      └─────────────────┘    ┌────────────┴────────────┐
                             │                         │
                      ┌──────▼────────┐      ┌────────▼──────┐
                      │ Task Ready?   │      │ Missing Info? │
                      │               │      │               │
                      │ YES ✓         │      │ YES ❓        │
                      └──────┬────────┘      └────────┬──────┘
                             │                       │
                      ┌──────▼──────────┐    ┌──────▼────────────┐
                      │ EXECUTE         │    │ ask_for_missing   │
                      │                 │    │ _info()           │
                      │ • Send WhatsApp │    │                   │
                      │ • Play YouTube  │    │ • Ask smartly     │
                      │ • Open App      │    │ • Collect input   │
                      │ • Other tasks   │    │ • Update memory   │
                      └────────┬────────┘    └──────┬────────────┘
                               │                    │
                               │              ┌─────▼────────┐
                               │              │ Retry        │
                               │              │ try_execute_ │
                               │              │ task()       │
                               │              └──────┬───────┘
                               │                     │
                               └──────┬──────────────┘
                                      │
                             ┌────────▼─────────┐
                             │ ✅ Task Complete │
                             │ or ❌ Failed     │
                             │ (Fallback to AI) │
                             └──────────────────┘
```

---

## Memory State Machine

```
                    MEMORY STATE TRANSITIONS

┌─────────────────────────────────────────────────────────────┐
│ INITIAL STATE: All fields NULL                              │
│ {app: null, intent: null, contact: null, message: null}    │
└──────────────────────┬──────────────────────────────────────┘
                       │ User says something
                       │
        ┌──────────────┴───────────────────┐
        │                                  │
   ┌────▼──────────┐              ┌───────▼─────────┐
   │ Has App?      │              │ Has Intent?     │
   │ DETECT_APP    │              │ DETECT_INTENT   │
   └────┬──────────┘              └───────┬─────────┘
        │                                 │
   ┌────▼────────────────┐        ┌──────▼──────┐
   │ app: whatsapp ✓     │        │ intent: send │
   │ intent: null        │        │ _message ✓  │
   │ contact: null       │        │ contact: null
   │ message: null       │        │ message: null
   └────┬────────────────┘        └──────┬───────┘
        │                                │
        └──────────────┬─────────────────┘
                       │
                   ┌───▼─────────────┐
                   │ Next input from │
                   │ user?           │
                   └───┬─────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼────────────────┐   ┌───────▼──────────┐
   │ Has Contact?        │   │ Extracting       │
   │ DETECT_CONTACT      │   │ message?         │
   └────┬────────────────┘   │ EXTRACT_MESSAGE  │
        │                    └───────┬──────────┘
   ┌────▼──────────────────┐         │
   │ app: whatsapp ✓       │    ┌────▼─────────┐
   │ intent: send ✓        │    │ All fields   │
   │ contact: mikku ✓      │    │ filled? ✓    │
   │ message: null         │    │             │
   └────┬─────────────────┘    └────┬────────┘
        │                           │
        │   ┌───────────────────────┘
        │   │
   ┌────▼───▼──────────────────────┐
   │ EXECUTION STATE                │
   │ All data ready!                │
   │ {app: whatsapp ✓               │
   │  intent: send ✓                │
   │  contact: mikku ✓              │
   │  message: hello ✓}             │
   └────┬──────────────────────────┘
        │
        │ EXECUTE TASK
        │ send_whatsapp_by_name()
        │
   ┌────▼──────────────────────────┐
   │ POST-EXECUTION CLEANUP         │
   │ Reset message field            │
   │ Keep app & contact for next    │
   │ {app: whatsapp ✓               │
   │  intent: null (cleared)        │
   │  contact: mikku ✓ (kept)       │
   │  message: null (cleared)}      │
   └────────────────────────────────┘
```

---

## Data Flow Diagram

```
                        DATA FLOW THROUGH SYSTEM

User Input (Voice/Text)
         │
         │ speech_recognition / take_command()
         │
         ▼
    "WhatsApp kholo Mikku ko 'hi' bhejo"
         │
         │
    ┌────┴──────────────────────────────────────┐
    │ DETECTION PIPELINE                        │
    │                                           │
    │  query: "WhatsApp kholo Mikku ko 'hi' ..." │
    │                                           │
    │  ├─► detect_app(query)                    │
    │  │   └─► Searches keywords in APPS dict   │
    │  │       → "whatsapp" found!              │
    │  │       ✓ app = "whatsapp"               │
    │  │                                        │
    │  ├─► detect_intent(query)                 │
    │  │   └─► Searches keywords in INTENTS     │
    │  │       → "bhejo" found!                 │
    │  │       ✓ intent = "send_message"        │
    │  │                                        │
    │  ├─► detect_contact(query)                │
    │  │   └─► Loops through CONTACTS dict      │
    │  │       → "mikku" found!                 │
    │  │       ✓ contact = "mikku"              │
    │  │                                        │
    │  └─► extract_message(query)               │
    │      └─► Uses extract_name_message()      │
    │          → Gets text after "ko"           │
    │          ✓ message = "'hi'"               │
    │                                           │
    └────┬──────────────────────────────────────┘
         │
         ▼
    MEMORY STATE UPDATED
    ┌──────────────────────┐
    │ app: whatsapp ✓      │
    │ intent: send_msg ✓   │
    │ contact: mikku ✓     │
    │ message: 'hi' ✓      │
    └──────┬───────────────┘
           │
           │ ALL REQUIRED FIELDS PRESENT
           │
           ▼
    try_execute_task()
    └─► Check: Is it WhatsApp send_message?  YES ✓
        └─► send_whatsapp_by_name("mikku", "'hi'")
            └─► Opens WhatsApp
            └─► Searches contact "mikku"
            └─► Types message "'hi'"
            └─► Sends message
            └─► Returns TRUE
           │
           ▼
    ✅ TASK COMPLETE
    speak("Message sent successfully!")
```

---

## Intent & Context Recognition

```
                MULTI-STEP INTENT RECOGNITION

Turn 1: User: "WhatsApp kholo"
        Query Analysis:
        ├─ "whatsapp" → App detected
        ├─ "kholo" (open) → Intent: open_app
        ├─ [no contact name] → No contact
        └─ [no message] → No message
        
        Memory After:
        ┌──────────────────────────┐
        │ app: whatsapp            │  ◄─ REMEMBERED
        │ intent: open_app         │
        │ contact: null            │
        │ message: null            │
        └──────────────────────────┘
        
        Action: ✅ Opens WhatsApp
        
───────────────────────────────────────────────────────

Turn 2: User: "Mikku ko message bhejo"
        Query Analysis:
        ├─ [no app mentioned]
        │  BUT >>> APP REMEMBERED FROM TURN 1! ◄─ KEY
        ├─ "bhejo" → Intent: send_message (UPDATED)
        ├─ "mikku" → Contact detected
        └─ [no message content]
        
        Memory After:
        ┌──────────────────────────┐
        │ app: whatsapp ✓          │  ◄─ KEPT FROM BEFORE
        │ intent: send_message ✓   │  ◄─ UPDATED
        │ contact: mikku ✓         │  ◄─ NEW
        │ message: null            │
        └──────────────────────────┘
        
        Validation: Missing message field
        Action: ❓ Ask "What message should I send to Mikku?"
        
───────────────────────────────────────────────────────

Turn 3: User: "Tell him I'll be late"
        Query Analysis:
        ├─ [no app mentioned] → app still whatsapp
        ├─ [no intent mentioned] → intent still send_message
        ├─ [no contact mentioned] → contact still mikku
        └─ "I'll be late" → Message detected
        
        Memory After:
        ┌──────────────────────────┐
        │ app: whatsapp ✓          │  ◄─ UNCHANGED
        │ intent: send_message ✓   │  ◄─ UNCHANGED
        │ contact: mikku ✓         │  ◄─ UNCHANGED
        │ message: I'll be late ✓  │  ◄─ COMPLETE NOW!
        └──────────────────────────┘
        
        Validation: ALL FIELDS COMPLETE ✓
        Action: ✅ EXECUTE - send_whatsapp_by_name("mikku", "I'll be late")
        
        Result: Message sent!
        
        Post-Execute Cleanup:
        ┌──────────────────────────┐
        │ app: whatsapp ✓          │  ◄─ KEPT (same app next?)
        │ intent: null             │  ◄─ CLEARED
        │ contact: mikku ✓         │  ◄─ KEPT (send more?)
        │ message: null            │  ◄─ CLEARED
        └──────────────────────────┘
```

---

## Supported Operations Matrix

```
╔═══════════════╦════════════════╦════════════════╦═════════════════╗
║ Current App   ║ Intent         ║ Requirements   ║ Action          ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ whatsapp      ║ send_message   ║ contact       ║ Message sent    ║
║               ║                ║ + message     ║                 ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ whatsapp      ║ open_app       ║ (none)        ║ App opens       ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ youtube       ║ open_app       ║ (none)        ║ App opens       ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ youtube       ║ play           ║ message       ║ Song plays      ║
║               ║                ║ (song name)   ║                 ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ google        ║ open_app       ║ (none)        ║ Page opens      ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ google        ║ search         ║ message       ║ Search results  ║
║               ║                ║ (search term) ║                 ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ [any]         ║ open_app       ║ (none)        ║ App opens       ║
╠═══════════════╬════════════════╬════════════════╬═════════════════╣
║ [any]         ║ close          ║ (none)        ║ Window closes   ║
╚═══════════════╩════════════════╩════════════════╩═════════════════╝
```

---

## Execution Decision Tree

```
                    EXECUTION DECISION TREE

                    ┌─────────────────────┐
                    │ Task Ready to       │
                    │ Execute?            │
                    └───────┬─────────────┘
                            │
                    ┌───────▼──────────┐
                    │ Check conditions │
                    └───────┬──────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐     ┌──────▼─────┐    ┌──────▼──────┐
    │ App: NO  │     │ All fields:│    │ Contact: NO │
    │          │     │ YES (✓)    │    │             │
    │ INCOMPLETE     │            │    │ INCOMPLETE  │
    └──────────┘     └──────┬─────┘    └─────────────┘
                            │
                    ┌───────▼──────────┐
                    │ EXECUTE NOW! ✅   │
                    │                  │
                    │ try_execute_     │
                    │ task()           │
                    │                  │
                    │ Runs appropriate │
                    │ handler:         │
                    │ • WhatsApp send  │
                    │ • YouTube play   │
                    │ • App open       │
                    │ • Etc.           │
                    └───────┬──────────┘
                            │
              ┌─────────────┴──────────────┐
              │                            │
         ┌────▼─────┐            ┌────────▼──────┐
         │ Success? │            │ Task Time:    │
         │ YES ✓    │            │ 1-5 seconds   │
         └────┬─────┘            └───────────────┘
              │
             ✅ DONE!
```

---

## Memory Visualization - Multi-Turn Example

```
CONVERSATION OVER TIME:

Turn 1: "WhatsApp kholo"
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  │ app:     ░░░░░░░░░░░░░░░░░░░░░░ whatsapp │
  │ intent:  ░░░░░░░░░░░░░░░░░░░░░░ open_app │
  │ contact: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (empty) │
  │ message: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (empty) │
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  Action: ✅ WhatsApp opens

Turn 2: "Mikku ko message bhejo"
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  │ app:     ░░░░░░░░░░░░░░░░░░░░░░ whatsapp  │ ◄─ KEPT
  │ intent:  ░░░░░░░░░░░░░░░░░░░░░░ send_msg  │ ◄─ UPDATED
  │ contact: ░░░░░░░░░░░░░░░░░░░░░░ mikku    │ ◄─ NEW
  │ message: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (empty)  │
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  Action: ❓ "What message should I send to Mikku?"

Turn 3: "I'll be late"
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  │ app:     ░░░░░░░░░░░░░░░░░░░░░░ whatsapp       │ ◄─ UNCHANGED
  │ intent:  ░░░░░░░░░░░░░░░░░░░░░░ send_msg      │ ◄─ UNCHANGED
  │ contact: ░░░░░░░░░░░░░░░░░░░░░░ mikku        │ ◄─ UNCHANGED
  │ message: ░░░░░░░░░░░░░░░░░░░░░░ I'll be late │ ◄─ COMPLETE!
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  Action: ✅ Message sent!

After Execution (Reset):
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
  │ app:     ░░░░░░░░░░░░░░░░░░░░░░ whatsapp │ ◄─ KEPT
  │ intent:  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (cleared)│
  │ contact: ░░░░░░░░░░░░░░░░░░░░░░ mikku    │ ◄─ KEPT
  │ message: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (cleared)│
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
  Ready for next command! Can say "Send another" or
  switch to different app.

Legend:
  ░░░░ = Filled (has value)
  ▓▓▓▓ = Empty (null)
```

---

## Function Call Hierarchy

```
main loop
    │
    └─► try_execute_with_prompts(query)
        │
        ├─► process_with_memory(query)
        │   ├─► detect_app(query)
        │   ├─► detect_intent(query)
        │   ├─► detect_contact(query)
        │   ├─► extract_message(query)
        │   │   └─► extract_name_message(query)  [existing]
        │   └─► print_memory_state()
        │
        ├─► try_execute_task()
        │   ├─► [Check WhatsApp conditions]
        │   │   └─► send_whatsapp_by_name()  [existing]
        │   ├─► [Check YouTube conditions]
        │   │   └─► pywhatkit.playonyt()  [existing]
        │   ├─► [Check other apps]
        │   └─► return success/failure
        │
        ├─ If not executed:
        │   ├─► ask_for_missing_info()
        │   │   ├─► speak()
        │   │   ├─► take_command()
        │   │   ├─► detect_contact() [again]
        │   │   └─► extract_message() [again]
        │   │
        │   └─► try_execute_task() [retry]
        │
        └─► return execution result

    If memory system returns False:
    └─► fallback to original execute_single_command()
        └─► [existing command handling]
```

---

## Response Time Breakdown

```
TYPICAL SINGLE COMMAND TIMING:

User speaks: "WhatsApp kholo Mikku ko 'hi' bhejo"
     │
     ├─ Speech Recognition: 2-3 sec
     │
     ├─ process_with_memory():
     │  ├─ detect_app(): 1 ms
     │  ├─ detect_intent(): 1 ms
     │  ├─ detect_contact(): 1 ms
     │  └─ extract_message(): 5 ms
     │     Total: ~10 ms
     │
     ├─ try_execute_task(): 
     │  └─ Condition checks: 1 ms
     │     Total: 1 ms
     │
     ├─ send_whatsapp_by_name():
     │  ├─ Open WhatsApp: 3-5 sec
     │  ├─ Search contact: 1-2 sec
     │  ├─ Type message: 1 sec
     │  └─ Send: 1 sec
     │     Total: 6-9 sec
     │
     └─ Total end-to-end: 8-12 seconds

BREAKDOWN:
  • Detection: <100ms (negligible)
  • WhatsApp automation: 6-9 sec (main bottleneck)
  • Speech recognition: 2-3 sec
```

---

## Error Handling Flow

```
                    ERROR HANDLING FLOW

try_execute_with_prompts(query)
        │
        ├─► process_with_memory(query)
        │   │
        │   └─► [Detections happen]
        │       Returns: has_info (True/False)
        │
        ├─► If has_info is False
        │   └─► return False (nothing to do)
        │
        ├─► try_execute_task()
        │   │
        │   ├─ Success ✓
        │   │  └─► return True
        │   │
        │   └─ Failure (missing fields)
        │      └─► continue to prompt
        │
        ├─► ask_for_missing_info()
        │   │
        │   ├─► Detect what's missing
        │   ├─► speak(question)
        │   ├─► take_command()
        │   │
        │   └─► Update memory with new input
        │
        ├─► try_execute_task() [RETRY]
        │   │
        │   ├─ Success ✓
        │   │  └─► return True
        │   │
        │   └─ Still Failing
        │      └─► return False
        │
        └─► Fallback to AI if returns False
            └─► get_ai_response(query)
```

---

**Visual diagrams help understand the flow. Refer back to these while reading the code!**
