from math import tan, pi

import cv2
import numpy as np

from tflite_runtime.interpreter import Interpreter


#V = 2.094 * (10**(-9))
S = 3.142 * (10**(-6))


class ObjectDetector:

	def __init__(self, tflite_model, threshold, frame_res):
		self.interpreter = Interpreter(model_path=tflite_model)
		self.interpreter.allocate_tensors()

		self.input_details = self.interpreter.get_input_details()
		self.output_details = self.interpreter.get_output_details()
		self.height = self.input_details[0]['shape'][1]
		self.width = self.input_details[0]['shape'][2]

		self.floating_model = (self.input_details[0]['dtype'] == np.float32)

		self.input_mean = 127.5
		self.input_std = 127.5

		self.threshold = threshold
		self.res_x, self.res_y = frame_res

	def get_contours(self, frame):
		frame_resized = cv2.resize(frame.copy(), (self.width, self.height))
		input_data = np.expand_dims(frame_resized, axis=0)

		if self.floating_model:
			input_data = (np.float32(input_data) - self.input_mean) / self.input_std

		self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
		self.interpreter.invoke()

		boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
		classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
		scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

		contours = []
		for i in range(len(scores)):
			if ((scores[i] > self.threshold) and (scores[i] <= 1.0)):

				ymin = int(max(1,(boxes[i][0] * self.res_y)))
				xmin = int(max(1,(boxes[i][1] * self.res_x)))
				ymax = int(min(self.res_y,(boxes[i][2] * self.res_y)))
				xmax = int(min(self.res_x,(boxes[i][3] * self.res_x)))

				contours.append([xmin, ymin, xmax, ymax])

		return contours


detector = ObjectDetector('extra-files/obj_detect_last.tflite', 0.3, (640, 480))


def proportions_processing(H, L, R, n1, n2):
	F = (n2*R)/(n1-n2)
	h = (H*F)/(L-R-F)
	return h


V = (4/3)*pi*(proportions_processing((tan(25*pi/180)), 1, 0.001, 1.333, 1))**3


def detect(path):
	img = cv2.imread(path)
	contours = detector.get_contours(img)

	ll = []
	objs = []

	for contour in contours:
		x_1, y_1, x_2, y_2 = contour
		img = cv2.rectangle(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 1)

		objs.append(max(x_2-x_1, y_2-y_1))

	objs.sort()

	for obj in objs:
		L = 1
		alpha = 25

		non_real_size_x = tan(alpha*pi/180)*L*(obj)/320
		#non_real_size_y = tan(alpha*pi/180)*L*(y_2-y_1)/240

		real_size_x = proportions_processing(non_real_size_x, L, 0.001, 1.333, 1)
		#real_size_y = proportions_processing(non_real_size_y, L, 0.001, 1.333, 1)

		#s = real_size_x*real_size_y
		v = (4/3)*pi*(real_size_x**3)
		ll.append([real_size_x, 100*v/V])

	new_path = 'extra-files/temp.jpg'
	cv2.imwrite(new_path, img)

	return new_path, ll
