import json
import os
import sys

def show_usage():
    print("Usage:")
    print("  python script.py <path_to_json_directory> [<'label_dict'>]")
    print("Arguments:")
    print("  <path_to_json_directory> - Path to the directory containing JSON files.")
    print("  <'label_dict'> - (Optional) A JSON-formatted string mapping label strings to class IDs.")
    print("                    Example: '{\"bundle\": 0, \"item\": 1}'")
    print("Each JSON file should contain bounding box information for an image.")
    print("The script converts JSON files to YOLOv8 compatible TXT files.")

def adjust_coordinates(value, max_size):
    # Ensure the value is within [0, max_size] and then normalize
    return max(0, min(value, max_size)) / max_size

def convert_to_yolo_format(json_file, image_width, image_height, label_dict):
    with open(json_file, 'r') as file:
        data = json.load(file)

    yolo_data = []
    for shape in data['shapes']:
        label = shape['label']
        class_id = label_dict.get(label, -1)  # Default to -1 if label is not in the dictionary
        if class_id == -1:
            continue  # Skip labels not found in the dictionary

        # Assuming the first point is top-right and the second is lower-left
        x1, y1 = shape['points'][0]
        x2, y2 = shape['points'][1]

        # Calculate YOLO format
        x_center = (x1 + x2) / 2.0
        y_center = (y1 + y2) / 2.0
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        # Adjust and normalize coordinates
        x_center_normalized = adjust_coordinates(x_center, image_width)
        y_center_normalized = adjust_coordinates(y_center, image_height)
        width_normalized = adjust_coordinates(width, image_width)
        height_normalized = adjust_coordinates(height, image_height)

        yolo_data.append(f'{class_id} {x_center_normalized} {y_center_normalized} {width_normalized} {height_normalized}')

    return yolo_data

def convert_directory(json_dir, label_dict):
    for file_name in os.listdir(json_dir):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(json_dir, file_name)
            txt_file_path = json_file_path.replace('.json', '.txt')

            # Reading image dimensions from JSON
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                image_width = data['imageWidth']
                image_height = data['imageHeight']

            yolo_data = convert_to_yolo_format(json_file_path, image_width, image_height, label_dict)

            with open(txt_file_path, 'w') as file:
                for line in yolo_data:
                    file.write(line + '\n')

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        show_usage()
        sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        show_usage()
        sys.exit(0)

    json_dir = sys.argv[1]
    label_dict = json.loads(sys.argv[2]) if len(sys.argv) == 3 else {}

    convert_directory(json_dir, label_dict)

