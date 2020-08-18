from imageai.Detection import ObjectDetection
from PIL import Image
from numpy import asarray

model_path = "./models/yolo-tiny.h5"
input_path = "./input/test.jpg"
output_path = "./output/newimage.jpg"

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()
custom = detector.CustomObjects(pizza=True)

# image = Image.open(input_path)
# data = asarray(image)
# print(type(data))

detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image=input_path, output_image_path=output_path, minimum_percentage_probability=20)

print(bool(detections))
print(detections)

# if "pizza" in detections:
# 	print("true")

# for eachItem in detections:
# 	print(eachItem["name"], ": ", eachItem["percentage_probability"])

# if not detections:
# 	print("no objects detected")