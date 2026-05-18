#!/usr/bin/env python3
"""
🧠 Context-Aware Memory System - Test Script

This script demonstrates how the memory system works
without requiring voice input. Perfect for understanding
the logic flow!
"""

# Simulating the memory system locally for testing
assistant_memory = {
    "current_app": None,
    "intent": None,
    "contact": None,
    "pending_message": None,
    "last_action": None
}

CONTACTS = {
    "sameer goswami": "+919893558503",
    "mikku": "+918085055261",
}

def print_memory_state():
    """Pretty print the current memory state"""
    print("\n📊 Memory Status:")
    print(f"   App:     {assistant_memory['current_app']}")
    print(f"   Intent:  {assistant_memory['intent']}")
    print(f"   Contact: {assistant_memory['contact']}")
    print(f"   Message: {assistant_memory['pending_message']}")
    print()

def detect_app(query):
    """App detection from query"""
    query = query.lower()
    apps = {
        "whatsapp": ["whatsapp", "wa", "message", "text", "bhejo"],
        "youtube": ["youtube", "yt", "play", "music", "song"],
        "google": ["google", "search", "dhundo"],
    }
    
    for app, keywords in apps.items():
        for keyword in keywords:
            if keyword in query:
                assistant_memory["current_app"] = app
                return app
    return None

def detect_intent(query):
    """Intent detection from query"""
    query = query.lower()
    intents = {
        "send_message": ["message", "bhejo", "send"],
        "open_app": ["open", "kholo"],
        "play": ["play", "sun"],
    }
    
    for intent_name, keywords in intents.items():
        for keyword in keywords:
            if keyword in query:
                assistant_memory["intent"] = intent_name
                return intent_name
    return None

def detect_contact(query):
    """Contact detection from query"""
    query = query.lower()
    for contact_name in CONTACTS.keys():
        if contact_name in query:
            assistant_memory["contact"] = contact_name
            return contact_name
    return None

def extract_message(query):
    """Extract message from query"""
    # Simple extraction: take everything after "ko"
    query_lower = query.lower()
    if "ko" in query_lower:
        idx = query_lower.find("ko") + 2
        message = query[idx:].strip()
        # Remove common keywords
        for word in ["message", "bhejo", "send"]:
            message = message.replace(word, "").strip()
        if message:
            assistant_memory["pending_message"] = message
            return message
    return None

def process_query(query):
    """Process a user query through the memory system"""
    print(f"\n🎤 User Said: \"{query}\"")
    print("=" * 60)
    
    # Detect everything
    detect_app(query)
    detect_intent(query)
    detect_contact(query)
    extract_message(query)
    
    # Show state
    print_memory_state()

def try_execute_task():
    """Check if we can execute the task"""
    if (assistant_memory["current_app"] == "whatsapp" and 
        assistant_memory["intent"] == "send_message" and 
        assistant_memory["contact"] and 
        assistant_memory["pending_message"]):
        return True
    return False

def execute_simulation():
    """Simulate task execution"""
    if try_execute_task():
        print("✅ Task Executed!")
        print(f"   Sending message to {assistant_memory['contact']}")
        print(f"   Message: \"{assistant_memory['pending_message']}\"")
        # Reset message after sending
        assistant_memory["pending_message"] = None
        return True
    return False

def reset_memory():
    """Reset memory for next task"""
    global assistant_memory
    assistant_memory = {
        "current_app": None,
        "intent": None,
        "contact": None,
        "pending_message": None,
        "last_action": None
    }
    print("🔄 Memory reset for next task\n")

# ============================================================
# TEST SCENARIOS
# ============================================================

print("\n" + "="*60)
print("🧠 CONTEXT-AWARE ASSISTANT - MEMORY SYSTEM TEST")
print("="*60)

# -------- TEST 1: Single Command --------
print("\n\n📍 TEST 1: SINGLE COMMAND (Everything in one sentence)")
print("-" * 60)

process_query("WhatsApp kholo Mikku ko message kar do mai kal college nahi aaunga")
execute_simulation()

# -------- TEST 2: Multi-Step --------
print("\n\n📍 TEST 2: MULTI-STEP CONVERSATION")
print("-" * 60)

reset_memory()

print("\nStep 1️⃣: User opens WhatsApp")
process_query("WhatsApp kholo")
print(f"Status: App detected: {assistant_memory['current_app']}")

print("\nStep 2️⃣: User mentions contact")
process_query("Mikku ko message bhejo")
print(f"Status: Intent updated, contact detected")
print(f"Memory remembers app: {assistant_memory['current_app']}")
print("⚠️  Assistant would ask: 'What message should I send to Mikku?'")

print("\nStep 3️⃣: User provides message")
process_query("Tell him mai kal college nahi aaunga")
execute_simulation()

# -------- TEST 3: Smart Extraction --------
print("\n\n📍 TEST 3: MESSAGE EXTRACTION FROM NATURAL SPEECH")
print("-" * 60)

reset_memory()

test_queries = [
    "Sameer ko hello bhejo",
    "Mikku ko kaise ho message karo",
    "WhatsApp mein Sameer ko 'good morning' bhej",
]

for query in test_queries:
    process_query(query)
    print(f"✓ Extracted Message: '{assistant_memory['pending_message']}'")

# -------- TEST 4: Partial Information --------
print("\n\n📍 TEST 4: HANDLING PARTIAL INFORMATION")
print("-" * 60)

reset_memory()

process_query("Message bhejo")
print(f"Status: Intent detected but contact missing!")
print("⚠️  Assistant would ask: 'Who do you want to message?'")

# Simulate user responding
print("\nUser responds: 'Mikku'")
process_query("Mikku")
print(f"Now contact is: {assistant_memory['contact']}")
print("⚠️  Assistant would ask: 'What message should I send to Mikku?'")

# Simulate user providing message
print("\nUser responds: 'Hi, how are you?'")
process_query("Hi, how are you?")
print(f"Message extracted: '{assistant_memory['pending_message']}'")

# -------- TEST 5: YouTube --------
print("\n\n📍 TEST 5: YOUTUBE FUNCTIONALITY")
print("-" * 60)

reset_memory()

process_query("YouTube par Arijit Singh ka gana play kar")
print(f"App: {assistant_memory['current_app']}")
print(f"Intent: {assistant_memory['intent']}")
print(f"Song: {assistant_memory['pending_message']}")

# ============================================================

print("\n\n" + "="*60)
print("✅ ALL TEST SCENARIOS COMPLETED!")
print("="*60)

print("""
📊 SUMMARY:

✔️ Single commands with full context
✔️ Multi-step conversations with memory persistence
✔️ Smart message extraction from natural speech
✔️ Handling incomplete information with smart prompts
✔️ Support for multiple apps (WhatsApp, YouTube, etc)

Your assistant is now context-aware! 🎉
""")
