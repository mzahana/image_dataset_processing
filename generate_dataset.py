import os
import shutil
import random
import sys

def split_data(source_dir, train_pct, valid_pct, test_pct):
    if train_pct + valid_pct + test_pct != 100:
        raise ValueError("The sum of percentages must be 100.")

    images_dir = os.path.join(source_dir, 'images')
    labels_dir = os.path.join(source_dir, 'labels')

    # Create train, valid, test directories
    for folder in ['train', 'valid', 'test']:
        for subfolder in ['images', 'labels']:
            os.makedirs(os.path.join(source_dir, folder, subfolder), exist_ok=True)

    # List all image files (both JPEG and PNG formats)
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png')]

    # Shuffle files
    random.shuffle(image_files)

    # Calculate split indices
    total_images = len(image_files)
    train_end = int(total_images * train_pct / 100)
    valid_end = train_end + int(total_images * valid_pct / 100)

    # Function to copy files
    def copy_files(files, dest_folder):
        for file in files:
            # Copy image
            shutil.copy(os.path.join(images_dir, file), os.path.join(source_dir, dest_folder, 'images', file))
            # Copy corresponding label file (assuming .txt extension)
            label_file = os.path.splitext(file)[0] + '.txt'
            if os.path.exists(os.path.join(labels_dir, label_file)):
                shutil.copy(os.path.join(labels_dir, label_file), os.path.join(source_dir, dest_folder, 'labels', label_file))

    # Split files
    copy_files(image_files[:train_end], 'train')
    copy_files(image_files[train_end:valid_end], 'valid')
    copy_files(image_files[valid_end:], 'test')

    print("Data split complete.")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python script.py <source_directory> <train_percentage> <valid_percentage> <test_percentage>")
        sys.exit(1)

    source_dir = sys.argv[1]
    train_pct = int(sys.argv[2])
    valid_pct = int(sys.argv[3])
    test_pct = int(sys.argv[4])

    split_data(source_dir, train_pct, valid_pct, test_pct)

