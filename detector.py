from imageai.Detection import ObjectDetection

model_path = "./models/yolo-tiny.h5"
input_path = "./input/test.jpg"
output_path = "./output/newimage.jpg"

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path, minimum_percentage_probability=30)

for eachItem in detections:
	print("--------------------------------------------")
	print(eachItem["name"], ": ", eachItem["percentage_probability"])
	print("--------------------------------------------")