#!/usr/bin/env python3
"""
⚡ CLOUD ARCHITECT DAEMON — 24/7 AUTONOMOUS CLOUD WORKER ⚡
Runs continuously in GitHub Codespaces without requiring any physical laptop.
Catches incoming prompts from Hugging Face & Vercel, synthesizes production-grade
code via Groq 120B / Qwen, and broadcasts direct delivery to user sandboxes!
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STREAM_TOPIC = "antibot_nexus_stream_vault_2026_x"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL_NAME = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are AntiBot Master Architect — Elite Software Synthesizer.
Synthesize a single-file, production-grade, highly engaging HTML5/CSS/JavaScript application.
CRITICAL STANDARDS:
1. Deliver ONLY the complete executable HTML file code with embedded CSS and JS (inside <style> and <script> tags).
2. NEVER use markdown fences (```html), NO conversational preambles, NO explanations. Start directly with <!DOCTYPE html> and end with </html>.
3. Use Tailwind CSS via CDN (<script src="https://cdn.tailwindcss.com"></script>).
4. Use modern aesthetics: deep dark mode, neon accents, glassmorphism, smooth animations.
5. Provide rich interactive gameplay/features with Web Audio API sound synthesis (no external MP3s).
6. Support both Keyboard (WASD/Arrows) and Mobile On-Screen Touch Controls (Virtual D-Pad/Buttons).
7. Zero placeholders, zero TODOs, 100% complete and working.
"""

def synthesize_application(prompt: str) -> str:
    print(f"[*] Cloud Synthesizing prompt: '{prompt}'...")
    req_data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a complete production-grade application for: {prompt}"}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(req_data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AntiBot/6.0"
        }
    )
    
    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        raw_code = result["choices"][0]["message"]["content"].strip()
        
        # Strip markdown fences if any slipped through
        if raw_code.startswith("```html"):
            raw_code = raw_code[7:]
        elif raw_code.startswith("```"):
            raw_code = raw_code[3:]
        if raw_code.endswith("```"):
            raw_code = raw_code[:-3]
        return raw_code.strip()

def deliver_to_cloud_relay(job_id: str, html_code: str):
    cloud_url = f"https://ntfy.sh/antibot_delivery_{job_id}"
    print(f"[*] Delivering code ({len(html_code)} bytes) to {cloud_url}...")
    
    req = urllib.request.Request(cloud_url, data=html_code.encode("utf-8"), method="PUT")
    req.add_header("Filename", "app.html")
    req.add_header("Title", "AntiBot Delivered App")
    
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=12, context=ssl_ctx) as resp:
                if resp.status == 200:
                    print(f"[✔] Successfully delivered to user sandbox via {cloud_url}!")
                    return True
        except Exception as e:
            print(f"[!] Delivery retry {attempt+1}/4: {e}")
            time.sleep(1)
    return False

def main():
    print("=" * 65)
    print("  ⚡ CLOUD ARCHITECT DAEMON — 24/7 CODESPACE WORKER ACTIVE ⚡")
    print(f"  Stream Topic : {STREAM_TOPIC}")
    print(f"  Cloud Model  : {MODEL_NAME}")
    print("=" * 65)
    
    os.makedirs("deliveries", exist_ok=True)
    stream_url = f"https://ntfy.sh/{STREAM_TOPIC}/json"
    
    while True:
        try:
            print(f"[*] Connecting to live prompt stream: {stream_url}...")
            req = urllib.request.Request(stream_url, headers={"User-Agent": "AntiBot-Cloud-Node/1.0"})
            with urllib.request.urlopen(req, timeout=60, context=ssl_ctx) as resp:
                for line in resp:
                    if not line:
                        continue
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if data.get("event") == "message":
                            msg_str = data.get("message", "{}")
                            job_data = json.loads(msg_str)
                            job_id = job_data.get("job_id")
                            prompt = job_data.get("prompt")
                            
                            if job_id and prompt:
                                print(f"\n[⚡ LIVE PROMPT RECEIVED] Job: {job_id} | Prompt: '{prompt}'")
                                html_code = synthesize_application(prompt)
                                
                                # Save locally in Codespace
                                local_path = os.path.join("deliveries", f"{job_id}.html")
                                with open(local_path, "w", encoding="utf-8") as f:
                                    f.write(html_code)
                                print(f"[✔] Saved in Codespace: {local_path}")
                                
                                # Deliver to user's screen
                                deliver_to_cloud_relay(job_id, html_code)
                    except Exception as parse_err:
                        pass
        except Exception as conn_err:
            print(f"[!] Stream reconnecting in 3s: {conn_err}")
            time.sleep(3)

if __name__ == "__main__":
    main()
