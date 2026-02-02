import json
from datetime import datetime, timedelta
from uuid import uuid4
import os

def generate_multi_chat_data():
    chats = {}
    
    # 1. Performance Stress Test
    stress_messages = []
    start_time = datetime.now() - timedelta(days=2)
    for i in range(1, 101):
        stress_messages.append({
            "id": str(uuid4()),
            "role": "user" if i % 2 != 0 else "assistant",
            "content": f"Stress message {i}. Testing list virtualization and scroll performance." if i > 10 else "Initial stress test setup.",
            "timestamp": (start_time + timedelta(minutes=i)).isoformat(),
            "total_tokens": 50
        })
    
    chat1_id = str(uuid4())
    chats[chat1_id] = {
        "id": chat1_id,
        "title": "🚀 Performance Stress Test",
        "messages": stress_messages,
        "total_tokens": 5000,
        "created_at": start_time.isoformat(),
        "updated_at": (start_time + timedelta(minutes=100)).isoformat()
    }

    # 2. Product Support Chat
    chat2_id = str(uuid4())
    chats[chat2_id] = {
        "id": chat2_id,
        "title": "📦 Order #12345 Support",
        "messages": [
            {"id": str(uuid4()), "role": "user", "content": "Where is my order?", "timestamp": (datetime.now() - timedelta(hours=5)).isoformat()},
            {"id": str(uuid4()), "role": "assistant", "content": "Your order #12345 is currently in transit. Expected delivery: **Tomorrow by 5 PM**.", "timestamp": (datetime.now() - timedelta(hours=4, minutes=58)).isoformat()}
        ],
        "total_tokens": 150,
        "created_at": (datetime.now() - timedelta(hours=5)).isoformat(),
        "updated_at": (datetime.now() - timedelta(hours=4)).isoformat()
    }

    # 3. Features & Markdown Test
    markdown_content = """### Features Test
- [x] Streaming
- [x] Multi-chat
- [ ] Voice support

```python
def check_status():
    return "All systems go"
```
Check our [docs](https://example.com)."""

    chat3_id = str(uuid4())
    chats[chat3_id] = {
        "id": chat3_id,
        "title": "✨ New Features Feedback",
        "messages": [
            {"id": str(uuid4()), "role": "user", "content": "What features are ready?", "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat()},
            {"id": str(uuid4()), "role": "assistant", "content": markdown_content, "timestamp": (datetime.now() - timedelta(minutes=29)).isoformat()}
        ],
        "total_tokens": 300,
        "created_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    os.makedirs("storage", exist_ok=True)
    with open("storage/chats.json", "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)
    
    print("Successfully generated multiple chat items in storage/chats.json")

if __name__ == "__main__":
    generate_multi_chat_data()
