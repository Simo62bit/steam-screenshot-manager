import os
import sys
import time
import csv
import requests
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# URL of the screenshot page
SCREENSHOTS_URL = input("Enter the link to the Steam profile screenshots (example: https://steamcommunity.com/profiles/76561198382122884/screenshots/): ")

# Chrome setup to mute logs
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--silent")

# Launch Chrome with STDERR redirected
with open(os.devnull, "w") as fnull:
    sys.stderr = fnull
    driver = webdriver.Chrome(options=chrome_options)

# Restore stderr to avoid GUI crashes
sys.stderr = sys.__stderr__

driver.get(SCREENSHOTS_URL)
input("Log in to the opened browser, then press ENTER here to continue...")

# Infinite scroll to load all screenshots
print("⬇️ Scrolling the page to load all screenshots...")
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("✅ All screenshots loaded.")

# Get all detail links
links = driver.find_elements(By.CSS_SELECTOR, "a.profile_media_item")
screenshot_links = [(a.get_attribute("data-publishedfileid"), a.get_attribute("href")) for a in links]

print(f"🔗 {len(screenshot_links)} screenshots found.")

# Visibility color mapping
VISIBILITY_COLORS = {
    "Public": "#b3ffb3",        # light green
    "Friends-only": "#ffff99",  # light yellow
    "Hidden": "#ff9999",        # light red
    "Unlisted": "#cccccc",      # light grey
}

results = []

# Loop through each screenshot
for screenshot_id, detail_url in screenshot_links:
    print(f"\n➡️ Opening screenshot {screenshot_id}...")
    try:
        driver.get(detail_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.commentthread_subscribe_ctn"))
        )

        # Check subscription status
        subscribe_box = driver.find_element(By.CSS_SELECTOR, "div.commentthread_subscribe_ctn")
        subscribed = "checked" in subscribe_box.get_attribute("class")
        status = "✅ Subscribed" if subscribed else "❌ Not subscribed"

        # Extract image URL
        try:
            img_elem = driver.find_element(By.CSS_SELECTOR, "img#ActualMedia")
            img_url = img_elem.get_attribute("src")
        except:
            img_url = None

        # Extract visibility
        try:
            # Open the visibility menu
            menu_button = driver.find_element(By.ID, "visibilityselect_activevisibility")
            driver.execute_script("arguments[0].click();", menu_button)
            time.sleep(0.5)  # Short pause to let the options appear

            # Now find all the options
            visibility_options = driver.find_elements(By.CSS_SELECTOR, "div.visibilityselect_options > div.option")
            visibility_text = "Public"

            for opt in visibility_options:
                check_img = opt.find_element(By.TAG_NAME, "img")
                style = check_img.get_attribute("style")
                if "visibility: visible" in style:
                    visibility_text = opt.text.strip()
                    break

            # Close the menu by clicking again
            driver.execute_script("arguments[0].click();", menu_button)

        except Exception as e:
            print(f"⚠️ Could not get visibility for {screenshot_id}: {e}")
            visibility_text = "Public"

        # Append results
        results.append({
            "screenshot_id": screenshot_id,
            "link": detail_url,
            "status": status,
            "img_url": img_url,
            "visibility": visibility_text
        })

        # Print current status
        print(f"{status} - Visibility: {visibility_text} - {detail_url}")

    except Exception as e:
        print(f"⚠️ Error on {screenshot_id}: {e}")

# Save results to CSV after all screenshots are processed
with open("steam_screenshots_subscribe_status.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["screenshot_id", "link", "status", "img_url", "visibility"])
    writer.writeheader()
    writer.writerows(results)

print("\n✅ Check completed. Results saved in steam_screenshots_subscribe_status.csv")
print("📷 Opening GUI with screenshots, please wait...")

# Interactive GUI
class ScreenshotGUI:
    def __init__(self, master, results, driver):
        self.master = master
        self.results = results
        self.driver = driver
        self.selected = set()
        self.canvas = tk.Canvas(master)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.img_labels = []
        self.load_images()
        self.create_buttons()

    def load_images(self):
        self.visibility_labels = []
        self.img_labels = []
        for idx, res in enumerate(self.results):
            try:
                if not res["img_url"]:
                    continue
                response = requests.get(res["img_url"])
                img = Image.open(BytesIO(response.content))
                img.thumbnail((150, 150))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(
                    self.frame,
                    image=img_tk,
                    borderwidth=2,
                    relief="solid",
                    highlightthickness=6,
                    highlightbackground="white"
                )
                lbl.image = img_tk
                lbl.grid(row=idx//5, column=idx%5, padx=5, pady=5)
                lbl.bind("<Button-1>", self.make_toggle_callback(idx))
                icon = "✅" if "Subscribed" in res["status"] else "❌"
                tk.Label(self.frame, text=icon, bg="white").grid(row=idx//5, column=idx%5, sticky="ne")
                visibility = res.get("visibility", "Public")
                bg_color = VISIBILITY_COLORS.get(visibility, "white")
                vis_lbl = tk.Label(
                    self.frame,
                    text=visibility,
                    bg=bg_color,
                    fg="black",
                    font=("Arial", 8)
                )
                vis_lbl.grid(row=idx//5, column=idx%5, sticky="ne")
                self.visibility_labels.append(vis_lbl)
                self.img_labels.append(lbl)
            except Exception as e:
                print(f"⚠️ Error loading image {res['img_url']}: {e}")

    def toggle_selection(self, idx):
        lbl = self.img_labels[idx]
        if idx in self.selected:
            # Deselect → white border
            lbl.config(highlightbackground="white")
            self.selected.remove(idx)
        else:
            # Select → red border
            lbl.config(highlightbackground="red")
            self.selected.add(idx)
        self.update_counter()
        self.update_action_buttons()

    def select_all(self):
        if len(self.selected) == len(self.img_labels):
            # All selected → deselect all
            for lbl in self.img_labels:
                lbl.config(highlightbackground="white")
            self.selected.clear()
        else:
            # Select all
            for lbl in self.img_labels:
                lbl.config(highlightbackground="red")
            self.selected = set(range(len(self.img_labels)))
        self.update_counter()
        self.update_action_buttons()
            
    def update_counter(self):
        self.counter_label.config(text=f"Selected: {len(self.selected)}")
        
    def update_action_buttons(self):
        # Enable buttons if there is at least 1 selection
        state = "normal" if len(self.selected) > 0 else "disabled"
        self.btn_subscribe.config(state=state)
        self.btn_unsubscribe.config(state=state)
        self.btn_visibility.config(state=state)
        self.btn_delete.config(state=state)

    def make_toggle_callback(self, idx):
        return lambda e: self.toggle_selection(idx)

    def create_buttons(self):
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(side="bottom", fill="x", pady=5)

        # Counter on the left
        self.counter_label = tk.Label(btn_frame, text="Selected: 0")
        self.counter_label.pack(side="left", padx=10)

        # Select all button
        tk.Button(btn_frame, text="Select all", command=self.select_all).pack(side="left", padx=5)

        # Subscribe / Unsubscribe buttons
        self.btn_subscribe = tk.Button(btn_frame, text="Subscribe", command=lambda: self.confirm_action("subscribe"), state="disabled")
        self.btn_subscribe.pack(side="left", padx=5)

        self.btn_unsubscribe = tk.Button(btn_frame, text="Unsubscribe", command=lambda: self.confirm_action("unsubscribe"), state="disabled")
        self.btn_unsubscribe.pack(side="left", padx=5)

        # VISIBILITY FEATURE
        visibility_frame = tk.Frame(btn_frame)
        visibility_frame.pack(side="left", padx=5)

        self.visibility_var = tk.StringVar(value="Public")
        visibility_options = ["Public", "Friends-only", "Hidden", "Unlisted"]
        self.visibility_menu = tk.OptionMenu(visibility_frame, self.visibility_var, *visibility_options)
        self.visibility_menu.pack(side="left")

        self.btn_visibility = tk.Button(
            visibility_frame,
            text="Change Visibility",
            command=self.confirm_visibility_change,
            state="disabled"
        )
        self.btn_visibility.pack(side="left", padx=5)

        # DELETE BUTTON
        self.btn_delete = tk.Button(btn_frame, text="Delete", command=self.confirm_delete, state="disabled")
        self.btn_delete.pack(side="left", padx=5)

    # SUBSCRIBE / UNSUBSCRIBE
    def confirm_action(self, action_type):
        action_text = "Subscribe" if action_type=="subscribe" else "Unsubscribe"
        if messagebox.askyesno("Confirm", f"Are you sure you want to {action_text} from the comment section of the selected images?"):
            self.perform_action(action_type)

    def perform_action(self, action_type):
        for idx in self.selected:
            res = self.results[idx]
            try:
                self.driver.get(res["link"])
                
                subscribe_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.commentthread_subscribe_ctn"))
                )
                
                subscribed = "checked" in subscribe_container.get_attribute("class")
                
                if action_type == "subscribe":
                    if not subscribed:
                        subscribe_button = subscribe_container.find_element(By.CSS_SELECTOR, "span.commentthread_subscribe_checkbox")
                        self.driver.execute_script("arguments[0].click();", subscribe_button)
                        time.sleep(1)
                        self.results[idx]["status"] = "✅ Subscribed"
                        print(f"{res['screenshot_id']}: ✅ Successfully subscribed")
                    else:
                        print(f"{res['screenshot_id']}: ⏩ Already subscribed, skipping")
                        
                elif action_type == "unsubscribe":
                    if subscribed:
                        subscribe_button = subscribe_container.find_element(By.CSS_SELECTOR, "span.commentthread_subscribe_checkbox")
                        self.driver.execute_script("arguments[0].click();", subscribe_button)
                        time.sleep(1)
                        self.results[idx]["status"] = "❌ Not subscribed"
                        print(f"{res['screenshot_id']}: ✅ Successfully unsubscribed")
                    else:
                        print(f"{res['screenshot_id']}: ⏩ Already unsubscribed, skipping")

                # Update icon in the GUI
                icon = "✅" if "Subscribed" in self.results[idx]["status"] else "❌"
                tk.Label(self.frame, text=icon).grid(row=idx//5, column=idx%5, sticky="ne")

            except Exception as e:
                print(f"{res['screenshot_id']}: ⚠️ Error - {e}")

        messagebox.showinfo("Done", f"Action {action_type} completed!")

    # VISIBILITY CHANGE
    def confirm_visibility_change(self):
        vis_type = self.visibility_var.get()
        if messagebox.askyesno("Confirm", f"Are you sure you want to set visibility to '{vis_type}' for the selected screenshots?"):
            self.perform_visibility_change(vis_type)

    def perform_visibility_change(self, vis_type):
        visibility_map = {
            "Public": "visibilityselect_option_0",
            "Friends-only": "visibilityselect_option_1",
            "Hidden": "visibilityselect_option_2",
            "Unlisted": "visibilityselect_option_3",
        }

        for idx in self.selected:
            res = self.results[idx]
            try:
                self.driver.get(res["link"])

                visibility_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.visibilityselectcontainer"))
                )

                menu_button = visibility_container.find_element(By.ID, "visibilityselect")
                self.driver.execute_script("arguments[0].click();", menu_button)
                time.sleep(1)

                option_id = visibility_map.get(vis_type)
                option_elem = self.driver.find_element(By.ID, option_id)
                self.driver.execute_script("arguments[0].click();", option_elem)
                time.sleep(1)

                print(f"{res['screenshot_id']}: ✅ Visibility changed to {vis_type}")
                self.results[idx]["visibility"] = vis_type

                if hasattr(self, "visibility_labels") and idx < len(self.visibility_labels):
                    self.visibility_labels[idx].config(
                        text=vis_type,
                        bg=VISIBILITY_COLORS.get(vis_type, "white"),
                        fg="black"
                    )

            except Exception as e:
                print(f"{res['screenshot_id']}: ⚠️ Error changing visibility - {e}")

        messagebox.showinfo("Done", f"Visibility changed to {vis_type} for selected screenshots.")

    # DELETE
    def confirm_delete(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to DELETE the selected screenshots? This action cannot be undone!"):
            self.perform_delete()

    def perform_delete(self):
        for idx in self.selected:
            res = self.results[idx]
            try:
                self.driver.get(res["link"])

                # Find the Delete button
                delete_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))
                )
                self.driver.execute_script("arguments[0].click();", delete_btn)
                time.sleep(1)

                # Wait for the confirmation modal and click OK
                ok_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'btn_green_steamui')]/span[text()='OK']"))
                )
                self.driver.execute_script("arguments[0].click();", ok_btn)
                time.sleep(1)

                print(f"{res['screenshot_id']}: ✅ Successfully deleted")

            except Exception as e:
                print(f"{res['screenshot_id']}: ⚠️ Error deleting - {e}")

        messagebox.showinfo("Done", "Selected screenshots have been deleted.")

# Launching GUI
root = tk.Tk()
root.title("Steam screenshot subscription management")
app = ScreenshotGUI(root, results, driver)
root.mainloop()

# Close browser after GUI is closed
driver.quit()
