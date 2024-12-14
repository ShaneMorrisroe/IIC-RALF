import re

# Helper function to parse device positions and components from the .sch file
def parse_schematic(file_path):
    devices = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Regex patterns for both device positions (N) and component definitions (C)
    device_regex = r'N\s*(-?\d+)\s*(-?\d+)\s*(-?\d+)\s*(-?\d+)\s*\{.*?lab=(.*?)\}'
    component_regex = r'C\s*\{.*?name=([^ ]+).*?lab=([^\}]+)\}.*?(-?\d+)\s*(-?\d+)\s*'

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        print(f"Processing line: {line}")  # Debugging line

        # Check for device position matches (N line)
        match = re.match(device_regex, line)
        if match:
            x1 = int(match.group(1))
            y1 = int(match.group(2))
            x2 = int(match.group(3))
            y2 = int(match.group(4))
            label = match.group(5)
            devices.append(((x1, y1), (x2, y2), label))
            print(f"Device found: {label}, Coordinates: {x1}, {y1}, {x2}, {y2}")  # Debugging device match

        # Check for component matches (C line)
        match = re.match(component_regex, line)
        if match:
            name = match.group(1)
            label = match.group(2)
            x = int(match.group(3))
            y = int(match.group(4))
            devices.append(((x, y), (x, y), label))  # Use same point for both x and y for components
            print(f"Component found: {name}, Label: {label}, Position: {x}, {y}")  # Debugging component match

    return devices

# Function to calculate bounding box
def calculate_bounding_box(devices):
    min_x = min(min(dev[0][0], dev[1][0]) for dev in devices)
    max_x = max(max(dev[0][0], dev[1][0]) for dev in devices)
    min_y = min(min(dev[0][1], dev[1][1]) for dev in devices)
    max_y = max(max(dev[0][1], dev[1][1]) for dev in devices)

    return min_x, min_y, max_x, max_y

# Function to insert a rectangle into the schematic file
def insert_rectangle(file_path, bounding_box):
    min_x, min_y, max_x, max_y = bounding_box
    # Rectangle format: 'Rect {min_x} {min_y} {max_x} {max_y}'
    rectangle = f"N {min_x} {min_y} {max_x} {max_y} {{lab=Rect}}  \n"
    with open(file_path, 'a') as f:
        f.write(rectangle)
    print(f"Rectangle drawn: {min_x}, {min_y} to {max_x}, {max_y}")

# Main function to automate the process
def draw_rectangle_around_devices(schematic_file_path):
    devices = parse_schematic(schematic_file_path)
    if devices:
        bounding_box = calculate_bounding_box(devices)
        insert_rectangle(schematic_file_path, bounding_box)
    else:
        print("No devices found in the schematic.")

# Example usage
schematic_file = 'Circuits/Examples/InvAmp/InvAmp.sch'  # Path to your .sch file
draw_rectangle_around_devices(schematic_file)
