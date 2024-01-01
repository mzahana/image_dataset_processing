from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('/home/user/shared_volume/bundle_images/runs/detect/train3/weights/best.pt')

# Define path to directory containing images and videos for inference
#source = '/home/user/shared_volume/bundle_images/images'
source='/home/user/shared_volume/bundle_images/video.mp4'
# Run inference on the source
results = model(source, conf=0.6, stream=False, save=True, project="/home/user/shared_volume/bundle_images/images", name="prediction")  # generator of Results objects
