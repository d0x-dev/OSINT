from flask import Flask, request, jsonify
from telethon import TelegramClient, events
import asyncio
import re
import json
import threading

# === Your Telegram API credentials ===
api_id = 27968657
api_hash = "bacad3606f1ce6902f4b761a062e8333"
phone = "+22870771645"

# === Group chat ID where the bot is ===
group_chat_id = -1003093986405

# === Security key for API ===
API_KEY = "dark"

# Flask app
app = Flask(__name__)

# Global loop running in a background thread
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient("darkapi_session", api_id, api_hash, loop=loop)

def run_loop():
    loop.run_forever()

threading.Thread(target=run_loop, daemon=True).start()

# Start Telegram client once in the background
async def init_client():
    await client.start(phone=phone)
loop.create_task(init_client())

@app.route("/index.cpp", methods=["GET"])
def index():
    key = request.args.get("key")
    number = request.args.get("number")
    upi = request.args.get("upi")
    aadhaar = request.args.get("aadhaar")
    vehicle = request.args.get("vehicle")

    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    
    # Handle phone number query
    if number:
        future = asyncio.run_coroutine_threadsafe(query_number(number), loop)
        try:
            result = future.result(timeout=30)
        except Exception as e:
            result = {"error": str(e)}
        return jsonify(result)
    
    # Handle UPI query
    elif upi:
        future = asyncio.run_coroutine_threadsafe(query_upi(upi), loop)
        try:
            result = future.result(timeout=30)
        except Exception as e:
            result = {"error": str(e)}
        return jsonify(result)
    
    # Handle Aadhaar query
    elif aadhaar:
        future = asyncio.run_coroutine_threadsafe(query_aadhaar(aadhaar), loop)
        try:
            result = future.result(timeout=30)
        except Exception as e:
            result = {"error": str(e)}
        return jsonify(result)
    
    # Handle vehicle query
    elif vehicle:
        future = asyncio.run_coroutine_threadsafe(query_vehicle(vehicle), loop)
        try:
            result = future.result(timeout=30)
        except Exception as e:
            result = {"error": str(e)}
        return jsonify(result)
    
    else:
        return jsonify({"error": "Missing query parameter. Use 'number', 'upi', 'aadhaar', or 'vehicle'"}), 400

async def query_number(number):
    future = asyncio.get_event_loop().create_future()

    @client.on(events.NewMessage(chats=group_chat_id))
    async def handler(event):
        text = event.raw_text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match and not future.done():
            json_text = match.group(0)
            try:
                data = json.loads(json_text)
                future.set_result(data)
            except json.JSONDecodeError:
                future.set_result({"error": "Invalid JSON", "raw": json_text})

    # send command
    await client.send_message(group_chat_id, f"/num {number}")

    try:
        result = await asyncio.wait_for(future, timeout=20)
    except asyncio.TimeoutError:
        result = {"error": "Timeout, no response from api"}

    return result

async def query_upi(upi):
    future = asyncio.get_event_loop().create_future()

    @client.on(events.NewMessage(chats=group_chat_id))
    async def handler(event):
        text = event.raw_text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match and not future.done():
            json_text = match.group(0)
            try:
                data = json.loads(json_text)
                future.set_result(data)
            except json.JSONDecodeError:
                future.set_result({"error": "Invalid JSON", "raw": json_text})

    # send command
    await client.send_message(group_chat_id, f"/upiinfo {upi}")

    try:
        result = await asyncio.wait_for(future, timeout=20)
    except asyncio.TimeoutError:
        result = {"error": "Timeout, no response from api"}

    return result

async def query_aadhaar(aadhaar):
    future = asyncio.get_event_loop().create_future()

    @client.on(events.NewMessage(chats=group_chat_id))
    async def handler(event):
        text = event.raw_text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match and not future.done():
            json_text = match.group(0)
            try:
                data = json.loads(json_text)
                future.set_result(data)
            except json.JSONDecodeError:
                future.set_result({"error": "Invalid JSON", "raw": json_text})

    # send command
    await client.send_message(group_chat_id, f"/aadhar {aadhaar}")

    try:
        result = await asyncio.wait_for(future, timeout=20)
    except asyncio.TimeoutError:
        result = {"error": "Timeout, no response from api"}

    return result

async def query_vehicle(vehicle):
    future = asyncio.get_event_loop().create_future()

    @client.on(events.NewMessage(chats=group_chat_id))
    async def handler(event):
        text = event.raw_text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match and not future.done():
            json_text = match.group(0)
            try:
                data = json.loads(json_text)
                future.set_result(data)
            except json.JSONDecodeError:
                future.set_result({"error": "Invalid JSON", "raw": json_text})

    # send command
    await client.send_message(group_chat_id, f"/vehicle {vehicle}")

    try:
        result = await asyncio.wait_for(future, timeout=20)
    except asyncio.TimeoutError:
        result = {"error": "Timeout, no response from api"}

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True)
