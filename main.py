import os
import yaml
from calendar import month_name

# Mapping for country-specific color codes
COUNTRY_COLORS = {
    "Norway": "&9",  # Blue
    "Sweden": "&e",  # Yellow
    "Finland": "&3",  # Turquoise
    "Denmark": "&c",  # Red
    "Estonia": "&1",  # Dark Blue
    "Latvia": "&6",   # Yellow
    "Lithuania": "&2",  # Green
    "Iceland": "&b"   # Light Turquoise
}

# Helper function to get color for location
def get_location_color(location):
    for country, color in COUNTRY_COLORS.items():
        if country in location:
            return color
    return "&7"  # Default: Gray

# Function to generate GUI YAML
def generate_gui(input_yaml_path, output_directory):
    with open(input_yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Access the `botm` section
    botm_data = data.get("botm", {})

    # Initialize GUI configuration
    slot_positions = [18, 27, 36]  # Slots for each place
    space_slots = [0, 1, 2, 3, 4, 5, 6, 7, 8, 45, 46, 47, 48, 49, 50, 51, 52, 53]
    file_counter = 0
    column_counter = 0
    heads = ["basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZTM0YTU5MmE3OTM5N2E4ZGYzOTk3YzQzMDkxNjk0ZmMyZmI3NmM4ODNhNzZjY2U4OWYwMjI3ZTVjOWYxZGZlIn19fQ",
             "basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvYTllMGExYmM2ZWIwYzZmMjcxZDMyM2ExOGUwMTQwY2U0M2Q5NTQ1OGI2YjViNmU4NDhkZjE3NDI1ZGJhOTZhZCJ9fX0",
             "basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMjQxMWMyOGVlZTVkNThkMWI4NjNiNTRlNWNjNjJjMzA3MjM0ZDQzN2MxN2YxZmY3NjMzOGRmZWNjM2NjNjhkNSJ9fX0"]
    arrows = {
        "previous": "basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZjg0ZjU5NzEzMWJiZTI1ZGMwNThhZjg4OGNiMjk4MzFmNzk1OTliYzY3Yzk1YzgwMjkyNWNlNGFmYmEzMzJmYyJ9fX0",
        "next": "basehead-eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZmNmZTg4NDVhOGQ1ZTYzNWZiODc3MjhjY2M5Mzg5NWQ0MmI0ZmMyZTZhNTNmMWJhNzhjODQ1MjI1ODIyIn19fQ"

    }
    current_file = {
        "menu_title": f"BOTM - Page {file_counter+1}",
        "size": 54,
        "register_command": True,
        "open_command": ["botm", "botm0"],
        "items": {}
    }

    # Iterate through `botm` data
    for idYear, (year, months) in enumerate(sorted(botm_data.items(), reverse=True)):
        for idMonth, (month, builds) in enumerate(sorted(months.items(), reverse=True)):

            # Ensure the month is valid
            try:
                month_int = int(month)
                month_name_str = month_name[month_int]
            except (ValueError, IndexError):
                print(f"Skipping invalid month: {month}")
                continue

            # Add the paper representing the month
            month_label_key = f"{month}/{str(year)[-2:]} 0"
            current_file["items"][month_label_key] = {
                'amount': month,
                'priority': 1,
                'material': 'PAPER',
                'display_name': f"&f{month_name_str} {year}",
                'slot': column_counter+9-(file_counter*9)
            }

            # Add builds for the month
            for idx, (build_key, details) in enumerate(builds.items(), 1):
                location_color = get_location_color(details['location'])
                display_name = f"&{['e', '7', '6'][(idx - 1)]}#{idx} {details['name']}"
                lore = [
                    f"{location_color}{details['location']}",
                    f"&7by {details['builder']}"
                ]
                # Properly handle Unicode strings for the display name and lore
                display_name = display_name.encode('utf-8').decode('utf-8')
                lore = [line.encode('utf-8').decode('utf-8') for line in lore]
                material = heads[idx-1]

                if details["coordinates"] != "":
                    command = ['[player] tp ' + details["coordinates"]]
                else:
                    command = ['[message] This location is not available']

                build_item_key = f"{month}/{str(year)[-2:]} {idx}"
                current_file['items'][build_item_key] = {
                    'amount': 1,
                    'priority': 1,
                    'material': material,
                    'display_name': display_name,
                    'lore': lore,
                    'slot': slot_positions[(idx - 1) % len(slot_positions)]+column_counter-(file_counter*9),
                    'left_click_commands': command
                }

            # Add one to column_counter
            column_counter += 1

            # Save file when getting to end of menu
            if (column_counter+1) % 10 == 0:
                # Add next arrow

                next_button_command = [
                    f"[player] botm{file_counter + 1}"
                ]

                current_file["items"]["nextPage"] = {
                    'display_name': 'Next',
                    "amount": 1,
                    "priority": 1,
                    "material": arrows["next"],
                    "slot": 53,
                    "left_click_commands": [line.encode('utf-8').decode('utf-8') for line in next_button_command]
                }

                if file_counter > 0:
                    # Add previous arrow
                    previous_button_command = [
                        f"[player] botm{file_counter-1}"
                    ]

                    current_file["items"]["previousPage"] = {
                        'display_name': 'Previous',
                        "amount": 1,
                        "priority": 1,
                        "material": arrows["previous"],
                        "slot": 45,
                        "left_click_commands": [line.encode('utf-8').decode('utf-8') for line in previous_button_command]
                    }

                current_file["items"]["space"] = {
                    "amount": 1,
                    "priority": 2,
                    "material": "GRAY_STAINED_GLASS_PANE",
                    "slots": space_slots
                }

                # Save the final YAML file
                output_path = os.path.join(output_directory, f"botm-{file_counter}.yml")
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    yaml.dump(current_file, output_file, allow_unicode=True, sort_keys=False)

                print(f"GUI YAML file saved: {output_path}")

                file_counter += 1

                current_file = {
                    "menu_title": f"BOTM - Page {file_counter+1}",
                    "size": 54,
                    "register_command": True,
                    "open_command": f"botm{file_counter}",
                    "items": {}
                }

    # Add spacing items
    current_file["items"]["space"] = {
        "amount": 1,
        "priority": 2,
        "material": "GRAY_STAINED_GLASS_PANE",
        "slots": space_slots
    }

    # Add previous arrow
    previous_button_command = [
        f"[player] botm{file_counter - 1}"
    ]

    current_file["items"]["previousPage"] = {
        'display_name': 'Previous',
        "amount": 1,
        "priority": 1,
        "material": arrows["previous"],
        "slot": 45,
        "left_click_commands": [line.encode('utf-8').decode('utf-8') for line in previous_button_command]
    }

    # Save the final YAML file
    output_path = os.path.join(output_directory, f"botm-{file_counter}.yml")
    with open(output_path, 'w', encoding='utf-8') as output_file:
        yaml.dump(current_file, output_file, allow_unicode=True, sort_keys=False)

    print(f"GUI YAML file saved: {output_path}")


if __name__ == "__main__":
    input_yaml_path = "config.yml"
    output_directory = "generated_botm"
    generate_gui(input_yaml_path, output_directory)
