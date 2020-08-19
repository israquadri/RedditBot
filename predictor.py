from imageai.Prediction import ImagePrediction


prediction = ImagePrediction()
prediction.setModelTypeAsInceptionV3()
prediction.setModelPath("./models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()



predictions, probabilities = prediction.predictImage("./input/test.jpg", result_count=2)
# for eachPrediction, eachProbability in zip(predictions, probabilities):
# 	print("-----------------------------------------------")
# 	print(eachPrediction, ": ", eachProbability)
# 	print("-----------------------------------------------")
print(predictions)
print(probabilities)