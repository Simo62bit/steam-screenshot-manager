# Steam Screenshot Subscription Manager

A Python script that helps you view Steam profile screenshots, check your subscription status on each screenshot's comment section, and subscribe/unsubscribe directly from a GUI interface.

---

## Features

- Automatically scrolls through a Steam profile’s screenshots to load all items.
- Checks subscription status for each screenshot's comment section.
- Saves results in a CSV file (steam_screenshots_subscribe_status.csv) with:
  - Screenshot ID
  - Screenshot link
  - Subscription status
  - Image URL
- Interactive GUI to view screenshots and manage subscriptions.
- Select individual or all screenshots for batch subscribe/unsubscribe actions.

---

## Requirements

- Python 3.8+
- Google Chrome browser installed
- Python packages:

pip install selenium pillow requests

---

## Usage

1. Run the script:

py steam_screenshot_manager.py

2. Enter the Steam profile screenshot URL when prompted, for example:

https://steamcommunity.com/profiles/76561198382122884/screenshots/

3. Log in to Steam in the Chrome browser that opens, then press ENTER in the terminal.

4. The script will scroll through the page to load all screenshots and check their subscription status.

5. Results will be saved in steam_screenshots_subscribe_status.csv.

6. A GUI window will open, displaying all screenshots with subscription status icons:
   - ✅ Subscribed
   - ❌ Not subscribed

7. You can:
   - Click a screenshot to select/deselect it.
   - Use the Select all button to select or deselect all.
   - Click Subscribe or Unsubscribe to perform the action on selected screenshots.

8. Close the GUI when finished—the Chrome browser will also close automatically.

---

## Notes

- Infinite scrolling may take a few seconds depending on the number of screenshots.
- The GUI uses Tkinter and Pillow for image display.
- Actions (subscribe/unsubscribe) interact with Steam directly—use responsibly to avoid triggering Steam limits.

---

## File Output

After running the script, a CSV file steam_screenshots_subscribe_status.csv will be generated with the following columns:

| screenshot_id | link | status | img_url |
|---------------|------|--------|---------|
| 1234567890    | https://steam... | ✅ Subscribed | https://steamcdn... |

---

## License

Copyright (c) 2025 Simo62bit

All rights reserved.

This software is proprietary and may not be copied, modified, distributed, or used without the explicit permission of the author.

For usage requests, contact: Simo62bit or simo62bit@gmail.com