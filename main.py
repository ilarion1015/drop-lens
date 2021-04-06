import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
	QVBoxLayout, QMainWindow, QTabWidget, QDialogButtonBox, QMessageBox, QAction)
from PySide2.QtGui import QKeySequence

from gui import StreamTab, ProcessingTab


class Window(QMainWindow):

	def __init__(self):
		super(Window, self).__init__()

		self.setWindowTitle('Линза Капля')
		self.resize(800, 600)

		self.tab_widget = QTabWidget(self)
		self.tab_widget.addTab(StreamTab(), 'Видео')
		self.tab_widget.addTab(ProcessingTab(), 'Обработка фото')

		self.create_menu_bar()

		self.setCentralWidget(self.tab_widget)

	def create_menu_bar(self):
		self.menu = self.menuBar()
		self.file_menu = self.menu.addMenu('Файл')
		self.about_menu = self.menu.addMenu('О программе')

		exit_action = QAction('Выйти', self)
		exit_action.setShortcut(QKeySequence.Close)
		exit_action.triggered.connect(self.close)
		self.file_menu.addAction(exit_action)

		about_action = QAction('Справка', self)
		about_action.setShortcut(QKeySequence.HelpContents)
		about_action.triggered.connect(self.show_about)
		self.about_menu.addAction(about_action)

	def show_about(self):
		QMessageBox().information(self, 'Справка', 'Что-то...')


if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = Window()
	window.show()

	sys.exit(app.exec_())
