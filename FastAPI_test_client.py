# Import the requests library
# - Allows sending HTTP requests (GET, POST, etc.)
# - Commonly used to test APIs
import requests

# Set your server base URL
BASE_URL = "https://ae9fbfa029df.ngrok-free.app"  # ← Replace with your current ngrok URL

try:
# ✅ Step 1: Ping the base URL (usually your "/" route)
# - Confirms the server is running
# - If this fails, skip the rest of the tests
    ping_res = requests.get(f"{BASE_URL}/")
    print("🚀 Server Ping Status:", ping_res.status_code)
    print("📢 Ping Response:", ping_res.text)

    # Check if server returned HTTP 200 OK
    if ping_res.status_code == 200:
        # ✅ Step 2: Run POST test
        post_res = requests.post(
            f"{BASE_URL}/students",
            json={ "id": "1", "name": "Alice", "task": "homework", "status": "NA"}
        )
        """
        print("✅ POST Status:", post_res.status_code)
        print("✅ POST Raw Text:", post_res.text)  # <-- Print raw response
        try:
            print("✅ POST JSON:", post_res.json())  # <-- Parse only if safe
        except ValueError as ve:
            print("❌ JSON decode error:", ve)"""

        print("✅ POST:", post_res.status_code, post_res.json())

        # ✅ Step 3: Run GET test
        get_res = requests.get(f"{BASE_URL}/students")
        print("✅ GET:", get_res.status_code, get_res.json())

        # ✅ Step 4: PUT test - Update student's status
        put_res = requests.put(
            f"{BASE_URL}/students/1",
            #json={"status": "completed"}  # Only update the "status" field
            json={
                "name": "Alice Updated",
                "status": "In progress",
                "task": "Prepare for exam"
               }
        )
        print("✅ PUT:", put_res.status_code, put_res.json())

        # Get status
        get_res = requests.get(f"{BASE_URL}/students")
        print("✅ Update student - GET:", get_res.status_code, get_res.json())

        # ✅ Step 5: DELETE test - Delete students
        delete_res = requests.delete(
            f"{BASE_URL}/students/1"
        )
        print("✅ DELETE:", delete_res.status_code, delete_res.json())

        # Get status
        get_res = requests.get(f"{BASE_URL}/students")
        print("✅ Delete student - GET:", get_res.status_code, get_res.json())
    else:
        print("⚠️ Server responded, but not with 200 OK. Please check your Flask app.")
except requests.exceptions.RequestException as e:
    print("❌ Could not connect to the server:", e)
except ValueError as ve:
    print("❌ Invalid JSON response received:", ve)
