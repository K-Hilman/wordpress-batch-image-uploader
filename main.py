import os
import base64
import requests
import csv
from time import sleep
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# === CONFIGURATION ===
WP_SITE_URL = "<YOUR SITE URL>"
USERNAME = "<YOUR WP USERNAME>"
APP_PASSWORD = "<YOUR APP PASSWORD"
BATCH_SIZE = 50
SLEEP_BETWEEN_BATCHES = 5  # seconds
REPORT_FILE = "upload_report.csv"

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode())
headers = {
    "Authorization": f"Basic {token.decode('utf-8')}",
    "Content-Disposition": "attachment"
}

# === LOGGING ===
report_rows = []

def image_exists(filename):
    # Remove extension from filename for search and comparison
    name_only = os.path.splitext(filename)[0]
    search_url = f"{WP_SITE_URL}/wp-json/wp/v2/media?search={name_only}"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        for item in results:
            wp_title = item.get("title", {}).get("rendered", "").lower()
            # Compare only the base name, not the extension
            if wp_title == name_only.lower():
                print(f"⏩ Skipped (duplicate): {filename}")
                report_rows.append([filename, "Skipped (duplicate)"])
                return True
    return False

def upload_image(file_path):
    filename = os.path.basename(file_path)

    if image_exists(filename):
        return

    for attempt in range(1, 4):  # Try up to 3 times
        with open(file_path, 'rb') as img:
            mime = "image/" + filename.split('.')[-1].lower()
            files = {'file': (filename, img, mime)}
            response = requests.post(f"{WP_SITE_URL}/wp-json/wp/v2/media", headers=headers, files=files)

        if response.status_code == 201:
            print(f"✅ Uploaded: {filename}")
            report_rows.append([filename, "Uploaded"])
            return
        else:
            print(f"⚠️ Attempt {attempt} failed for {filename} – {response.status_code}")
            if attempt < 3:
                print("⏳ Retrying in 5 minutes...")
                sleep(300)  # Wait 5 minutes before next attempt
            else:
                print(f"❌ Failed after 3 attempts: {filename}")
                report_rows.append([filename, f"Failed after 3 attempts ({response.status_code})"])

def upload_images(file_list, progress_bar, status_label, counter_label):
    total = len(file_list)
    progress_bar["maximum"] = total
    progress_bar["value"] = 0
    status_label.config(text="Uploading...")
    root.update_idletasks()

    count = 0
    for i in range(0, total, BATCH_SIZE):
        batch = file_list[i:i + BATCH_SIZE]
        for file in batch:
            upload_image(file)
            count += 1
            progress_bar["value"] = count
            counter_label.config(text=f"{count}/{total}")
            root.update_idletasks()
        sleep(SLEEP_BETWEEN_BATCHES)

    # Write CSV report
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Status"])
        writer.writerows(report_rows)

    status_label.config(text=f"Done! Report saved to {REPORT_FILE}")
    messagebox.showinfo("Upload Complete", f"All images processed.\nReport saved to {REPORT_FILE}")

    # Write CSV report
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Status"])
        writer.writerows(report_rows)

    status_label.config(text=f"Done! Report saved to {REPORT_FILE}")
    messagebox.showinfo("Upload Complete", f"All images processed.\nReport saved to {REPORT_FILE}")
    root.after(2000,root.destroy)  # Close the window after 2 seconds if needed

def start_upload(file_list, progress_bar, status_label, counter_label):
    upload_thread = threading.Thread(target=upload_images, args=(file_list, progress_bar, status_label, counter_label))
    upload_thread.daemon = True  # Allows the thread to close when the GUI exits
    upload_thread.start()

def browse_files():
    files = filedialog.askopenfilenames(
        title="Select Image Files",
        filetypes=[("Image Files", ".jpg .jpeg .png .gif .webp .bmp .tiff")]
    )
    if files:
        start_upload(list(files), progress_bar, status_label, counter_label)

# === GUI SETUP ===
root = tk.Tk()
root.title("WordPress Batch Image Uploader")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Drag and drop images here or click to browse", pady=10)
label.pack()

button = tk.Button(frame, text="Select Images", command=browse_files)
button.pack(pady=5)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(frame, text="")
status_label.pack()

counter_label = tk.Label(frame, text="0/0")
counter_label.pack()

root.mainloop()
