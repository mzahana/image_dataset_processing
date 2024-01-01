import os
import sys

def check_labels(image_dir, label_dir):
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    for image_file in image_files:
        label_file = image_file.rsplit('.', 1)[0] + '.txt'

        if label_file not in label_files:
            print(f"Warning: No label file for image {image_file}")
            continue

        with open(os.path.join(label_dir, label_file), 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Error in {label_file}: Incorrect number of values on line '{line.strip()}'")
                    continue

                class_id, x_center, y_center, width, height = map(float, parts)
                if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
                    print(f"Error in {label_file}: Bounding box values out of bounds on line '{line.strip()}'")

def main(directory):
    image_dir = os.path.join(directory, 'images')
    label_dir = os.path.join(directory, 'labels')

    if not os.path.exists(image_dir) or not os.path.exists(label_dir):
        print("Both 'images' and 'labels' directories must exist.")
        return

    check_labels(image_dir, label_dir)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)

