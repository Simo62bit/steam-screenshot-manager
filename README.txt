# Steam Screenshot Subscription Manager

A Python script with a GUI that lets you view Steam profile screenshots, check subscription status for each screenshot’s comment section, manage visibility, and subscribe/unsubscribe or delete screenshots directly.

---

## Features

- Automatic Screenshot Loading: Scrolls through a Steam profile’s screenshots to load all items.
- Subscription Status Check: Determines subscription status for the comment section of each screenshot.
- CSV Export: Saves all results in steam_screenshots_subscribe_status.csv with the following fields:
	Screenshot ID
	Screenshot link
	Subscription status
	Image URL
	Visibility
- Interactive GUI:
	View thumbnails of all screenshots.
	Highlight selected screenshots with a red border.
	Select individual or all screenshots for batch operations.
- Batch Subscription Management:
	Subscribe or unsubscribe to comment sections of selected screenshots.
	Updates the GUI icon to show current subscription status.
- Visibility Management:
	Change the visibility of selected screenshots (Public, Friends-only, Hidden, Unlisted) directly from the GUI.
	Color-coded labels for quick identification:
		Public → Light green
		Friends-only → Light yellow
		Hidden → Light red
		Unlisted → Light grey
- Screenshot Deletion: Delete selected screenshots permanently with confirmation prompts.
- Error Handling: Gracefully handles issues with loading images, changing visibility, or performing subscription actions.
- Cross-Platform: Works with Chrome via Selenium and standard Python GUI libraries (Tkinter + PIL).

---

## Requirements

- Python 3.8+
- Google Chrome browser installed
- Python packages:

python3 -m pip install selenium pillow requests

---

## Usage

1. Run the script:

py steam_screenshot_manager.py

2. Enter the Steam profile screenshot URL when prompted, for example:

https://steamcommunity.com/profiles/76561198382122884/screenshots/

3. Log in to Steam in the Chrome browser that opens, then press ENTER in the terminal.

4. The script will scroll through the page to load all screenshots, check their subscription status, and retrieve visibility information.

5. Results will be saved in steam_screenshots_subscribe_status.csv.

6. A GUI window will open, displaying all screenshots with the following indicators:
   - ✅ Subscribed
   - ❌ Not subscribed
   - Color-coded visibility labels:
		Light green → Public
		Light yellow → Friends-only
		Light red → Hidden
		Light grey → Unlisted

7. GUI interactions:
   - Click a screenshot to select/deselect it.
   - Use the Select all button to select or deselect all screenshots.
   - Use Subscribe or Unsubscribe to perform the action on selected screenshots.
   - Change visibility for selected screenshots using the dropdown menu and Change Visibility button.
   - Permanently delete selected screenshots using the Delete button (with confirmation prompt).

8. Close the GUI when finished—the Chrome browser will also close automatically.

---

## Notes

- Infinite scrolling may take several seconds depending on the number of screenshots.
- The GUI uses Tkinter and Pillow for image display.
- Actions (subscribe/unsubscribe, visibility changes, deletion) interact directly with Steam—use responsibly to avoid triggering Steam limits.
- Deletion changes are irreversible. double-check selections before confirming.

---

## File Output

After running the script, a CSV file steam_screenshots_subscribe_status.csv will be generated with the following columns:

| screenshot\_id | link                              | status       | img\_url                                | visibility |
| -------------- | --------------------------------- | ------------ | --------------------------------------- | ---------- |
| 1234567890     | [https://steam](https://steam)... | ✅ Subscribed | [https://steamcdn](https://steamcdn)... | Public     |

---

## License

Copyright (c) 2025 Simo62bit

All rights reserved.

This software is proprietary and may not be copied, modified, distributed, or used without the explicit permission of the author.

For usage requests, contact: Simo62bit or simo62bit@gmail.com