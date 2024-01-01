import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import yaml

def load_class_names(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        return data.get('names', [])

def display_random_image_with_boxes(base_dir):
    images_dir = os.path.join(base_dir, 'images')
    labels_dir = os.path.join(base_dir, 'labels')
    yaml_file = os.path.join(base_dir, 'data.yaml')

    class_names = []
    if os.path.exists(yaml_file):
        class_names = load_class_names(yaml_file)

    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        print("Both 'images' and 'labels' directories must exist.")
        return

    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    if not image_files:
        print("No images found in the 'images' directory.")
        return

    selected_image = random.choice(image_files)
    image_path = os.path.join(images_dir, selected_image)
    label_path = os.path.join(labels_dir, os.path.splitext(selected_image)[0] + '.txt')

    if not os.path.exists(label_path):
        print(f"No corresponding label file found for {selected_image}.")
        return

    # Open the image
    image = Image.open(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Read and plot bounding boxes from the label file
    with open(label_path, 'r') as file:
        for line in file:
            class_id, x_center, y_center, width, height = map(float, line.split())

            class_label = class_names[int(class_id)] if class_names else str(int(class_id))

            # Convert from YOLO format to matplotlib format
            image_width, image_height = image.size
            x_center *= image_width
            y_center *= image_height
            width *= image_width
            height *= image_height
            x_min = x_center - width / 2
            y_min = y_center - height / 2

            # Create a Rectangle patch
            rect = patches.Rectangle((x_min, y_min), width, height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.text(x_min, y_min, class_label, color='white', fontsize=12, backgroundcolor='red')

    plt.show()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
        sys.exit(1)

    base_dir = sys.argv[1]
    display_random_image_with_boxes(base_dir)

