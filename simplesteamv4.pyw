import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox, QTabWidget, QLineEdit
from PyQt5.QtCore import QUrl

class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.removeTab(index)

    def add_tab(self, widget, title):
        self.addTab(widget, title)

class CustomBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab_widget = TabWidget()
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate_to_url)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.address_bar)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.history = []

        # Добавляем начальную вкладку с Google
        self.add_new_tab(QUrl("https://www.google.com"), "Google")

    def add_new_tab(self, url, title):
        new_tab = QtWebEngineWidgets.QWebEngineView()
        new_tab.load(url)
        self.tab_widget.add_tab(new_tab, title)

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.add_new_tab(QUrl(url), url)

        # Добавляем URL в историю
        self.history.append(url)

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(300, 150)

        layout = QtWidgets.QVBoxLayout()

        self.launch_steam_button = QtWidgets.QPushButton("Открыть Steam")
        self.launch_steam_button.setStyleSheet("background-color: #2ecc71; color: #FFFFFF;")
        self.launch_steam_button.clicked.connect(self.launch_steam)
        layout.addWidget(self.launch_steam_button)

        self.setLayout(layout)

    def launch_steam(self):
        steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
        if os.path.exists(steam_path):
            os.startfile(steam_path)
        else:
            QMessageBox.critical(self, "Ошибка", "Steam не найден.")

class SteamGamePorter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam Library Mini")
        self.setGeometry(100, 100, 1024, 600)
        self.setStyleSheet("background-color: #212121; color: #FFFFFF;")

        self.font_style = QtGui.QFont("Roboto", 14, QtGui.QFont.Bold)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.installed_games_label = QtWidgets.QLabel("Установленные игры:")
        self.installed_games_label.setFont(self.font_style)
        self.main_layout.addWidget(self.installed_games_label)

        self.installed_games_list = QtWidgets.QListWidget(self)
        self.installed_games_list.setFont(self.font_style)
        self.installed_games_list.setStyleSheet("background-color: #212121; color: #FFFFFF;")
        self.installed_games_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.installed_games_list.itemClicked.connect(self.on_game_select)
        self.main_layout.addWidget(self.installed_games_list)

        self.options_layout = QtWidgets.QHBoxLayout()
        self.launch_options_label = QtWidgets.QLabel("Параметры запуска:")
        self.launch_options_label.setFont(self.font_style)
        self.options_layout.addWidget(self.launch_options_label)

        self.launch_options_entry = QtWidgets.QLineEdit()
        self.launch_options_entry.setFont(self.font_style)
        self.options_layout.addWidget(self.launch_options_entry)
        self.options_layout.addStretch()

        self.main_layout.addLayout(self.options_layout)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.launch_button = QtWidgets.QPushButton("Запустить")
        self.launch_button.setStyleSheet("background-color: #2ecc71; color: #FFFFFF;")
        self.launch_button.setFont(self.font_style)
        self.launch_button.clicked.connect(self.launch_game)
        self.launch_button.setFixedSize(200, 50)
        self.button_layout.addWidget(self.launch_button)

        self.remove_button = QtWidgets.QPushButton("Удалить")
        self.remove_button.setStyleSheet("background-color: #e74c3c; color: #FFFFFF;")
        self.remove_button.setFont(self.font_style)
        self.remove_button.clicked.connect(self.remove_game)
        self.remove_button.setFixedSize(200, 50)
        self.button_layout.addWidget(self.remove_button)

        self.refresh_button = QtWidgets.QPushButton("Обновить")
        self.refresh_button.setStyleSheet("background-color: #9300ff; color: #FFFFFF;")
        self.refresh_button.setFont(self.font_style)
        self.refresh_button.clicked.connect(self.scan_games)
        self.refresh_button.setFixedSize(200, 50)
        self.button_layout.addWidget(self.refresh_button)

        self.open_location_button = QtWidgets.QPushButton("Расположение")
        self.open_location_button.setStyleSheet("background-color: #3498db; color: #FFFFFF;")
        self.open_location_button.setFont(self.font_style)
        self.open_location_button.clicked.connect(self.open_game_location)
        self.open_location_button.setFixedSize(200, 50)
        self.button_layout.addWidget(self.open_location_button)

        self.main_layout.addLayout(self.button_layout)

        self.author_label = QtWidgets.QLabel("By Frimedox")
        self.author_label.setFont(self.font_style)
        self.author_label.setStyleSheet("background-color: #212121; color: #FFFFFF;")
        self.author_label.setAlignment(QtCore.Qt.AlignRight)
        self.main_layout.addWidget(self.author_label)

        self.browser_window = CustomBrowser()  # Инициализация встроенного браузера

        self.scan_games()

    def scan_games(self):
        self.installed_games_list.clear()  # Очистка списка перед обновлением
        steam_path = r"C:\Program Files (x86)\Steam\steamapps\common"
        if os.path.exists(steam_path):
            installed_games = os.listdir(steam_path)
            for game in installed_games:
                item = QtWidgets.QListWidgetItem(game)
                self.installed_games_list.addItem(item)

    def launch_game(self):
        selected_item = self.installed_games_list.currentItem()
        if selected_item:
            selected_game = selected_item.text()
            steam_id = self.get_steam_id(selected_game)
            if steam_id:
                steam_url = f"steam://run/{steam_id}"
                if self.launch_options_entry.text():
                    steam_url += " " + self.launch_options_entry.text()
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(steam_url))
            else:
                print("ID игры Steam не найден.")

    def remove_game(self):
        selected_item = self.installed_games_list.currentItem()
        if selected_item:
            selected_game = selected_item.text()
            confirmation = QMessageBox.question(self, "Подтверждение", f"Вы уверены, что хотите удалить игру '{selected_game}'?",
                                                 QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                game_path = os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common", selected_game)
                try:
                    os.system(f'rd /s /q "{game_path}"')
                    self.installed_games_list.takeItem(self.installed_games_list.row(selected_item))
                    QMessageBox.information(self, "Успех", f"Игра '{selected_game}' успешно удалена.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить игру '{selected_game}': {str(e)}")

    def open_game_location(self):
        selected_item = self.installed_games_list.currentItem()
        if selected_item:
            selected_game = selected_item.text()
            game_path = os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common", selected_game)
            os.startfile(game_path)  # Открытие расположения игры

    def get_steam_id(self, game_name):
        steam_apps_path = r"C:\Program Files (x86)\Steam\steamapps"
        if os.path.exists(steam_apps_path):
            for foldername in os.listdir(steam_apps_path):
                if foldername.startswith("appmanifest"):
                    file_path = os.path.join(steam_apps_path, foldername)
                    with open(file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        if game_name.lower() in content.lower():
                            return foldername.split("_")[1]

    def on_game_select(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SteamGamePorter()
    window.show()
    sys.exit(app.exec_())
