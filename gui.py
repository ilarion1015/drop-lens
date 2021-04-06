from PySide2.QtWidgets import QDialog, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QMessageBox
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl, Qt
from PySide2.QtGui import QFont, QPixmap, QPainter
from PySide2.QtCharts import QtCharts

from detection import detect


SIMPLE_FONT = QFont()
SIMPLE_FONT.setPixelSize(13)

BOLD_FONT = QFont()
BOLD_FONT.setPixelSize(13)
BOLD_FONT.setBold(True)


class StreamTab(QWidget):

	def __init__(self):
		super(StreamTab, self).__init__()

		self.web_view = QWebEngineView()
		self.web_view.load(QUrl('https://i.ibb.co/8bDzXkH/1.jpg'))

		self.save_photo_but = QPushButton('Сохранить изображение')
		self.save_photo_but.setFont(SIMPLE_FONT)
		self.save_photo_but.clicked.connect(self.save_photo_click)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.web_view)
		main_layout.addWidget(self.save_photo_but)
		self.setLayout(main_layout)

	def save_photo_click(self):
		direc = QFileDialog.getExistingDirectory()
		#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  save to     {{{{direc}}}}      !!!!!
		print('Saved!')


class ProcessingTab(QWidget):

	def __init__(self):
		super(ProcessingTab, self).__init__()

		self.ll = []

		self.pixmap = QPixmap('extra-files/test-img.png')
		self.img_label = QLabel(self)
		self.img_label.setPixmap(self.pixmap)
		self.img_label.setAlignment(Qt.AlignCenter)

		self.path_edit = QLineEdit('///путь к изображению///', readOnly=True)
		self.path_edit.setFont(SIMPLE_FONT)

		self.path_but = QPushButton('Выбрать изображение')
		self.path_but.setFont(SIMPLE_FONT)
		self.path_but.clicked.connect(self.path_click)

		self.detect_but = QPushButton('Обработать')
		self.detect_but.setFont(BOLD_FONT)
		self.detect_but.clicked.connect(self.detect_click)

		self.info = 'Noneee'

		self.info_but = QPushButton('Информация')
		self.info_but.setFont(BOLD_FONT)
		self.info_but.setEnabled(False)
		self.info_but.clicked.connect(self.info_click)

		path_layout = QHBoxLayout()
		path_layout.addWidget(self.path_edit)
		path_layout.addWidget(self.path_but)
		path_layout.addWidget(self.detect_but)
		path_layout.addWidget(self.info_but)

		main_layout = QVBoxLayout()
		main_layout.addWidget(self.img_label)
		main_layout.addLayout(path_layout)

		self.setLayout(main_layout)

	def path_click(self):
		self.path_edit.setText(QFileDialog.getOpenFileName()[0])
		self.info_but.setEnabled(False)

		self.pixmap.load(self.path_edit.text())
		self.img_label.setPixmap(self.pixmap)

	def detect_click(self):
		detectionsss = detect(self.path_edit.text())
		self.ll = detectionsss[1]

		self.pixmap.load(detectionsss[0])
		self.img_label.setPixmap(self.pixmap)

		self.info_but.setEnabled(True)



	def info_click(self):
		chart = ChartWindow(self.ll)
		chart.setModal(True)
		chart.exec()


class ChartWindow(QDialog):

	def __init__(self, ll):
		super(ChartWindow, self).__init__()

		self.ll = ll

		self.setWindowTitle('Информация о объектах')
		self.resize(600, 600)

		self.create_linechart()

	def create_linechart(self):
		line = QtCharts.QLineSeries(self)

		for obj in self.ll:
			line.append(obj[0], obj[1])

		'''axis_x = QtCharts.QValueAxis()
		axis_x.setTitleText('d, м')
		axis_x.setRange(0, 1)
		axis_y = QtCharts.QValueAxis()
		axis_y.setTitleText('Q, %')
		axis_y.setRange(0, 1)'''

		chart = QtCharts.QChart()

		chart.addSeries(line)
		chart.createDefaultAxes()
		chart.axisX().setTitleText('d, м')
		chart.axisY().setTitleText('Q, %')

		chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
		chart.setTitle('Line')
		chart.legend().setVisible(False)

		chart_view = QtCharts.QChartView(chart)
		chart_view.setRenderHint(QPainter.Antialiasing)

		layout = QVBoxLayout()
		layout.addWidget(chart_view)

		self.setLayout(layout)
