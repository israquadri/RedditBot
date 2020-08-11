from imageai.Prediction import ImagePrediction


prediction = ImagePrediction()
prediction.setModelTypeAsDenseNet()
prediction.setModelPath("./models/DenseNet-BC-121-32.h5")
prediction.loadModel()



predictions, probabilities = prediction.predictImage("./input/test.jpg", result_count=10)
for eachPrediction, eachProbability in zip(predictions, probabilities):
	print("-----------------------------------------------")
	print(eachPrediction, ": ", eachProbability)
	print("-----------------------------------------------")
