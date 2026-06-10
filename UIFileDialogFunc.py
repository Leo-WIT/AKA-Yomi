import os
import re
import platform
import subprocess

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QIcon

from UIFileDialogView import Ui_Dialog
from UIFunc import scripts, scripts_map

from KeymouseGo import to_abs_path


def _tr(zh, en, tw):
    """Get text based on current language setting."""
    # Read language from config file
    try:
        from PySide6.QtCore import QSettings
        config = QSettings(to_abs_path('config.ini'), QSettings.IniFormat)
        lang = config.value("Config/Language", "简体中文")
    except:
        lang = "简体中文"
    if lang == 'English':
        return en
    elif lang == '繁體中文':
        return tw
    return zh


class FileDialog(Ui_Dialog):
    def __init__(self):
        self.dialog = QDialog()
        self.setupUi(self.dialog)
        self.dialog.setFixedSize(self.dialog.width(), self.dialog.height())
        self.choice.clicked.connect(self.choice_file)
        self.edit.clicked.connect(self.edit_file)
        self.rename.clicked.connect(lambda: self.rename_file(self.lineEdit.text()))

        self.main_window = QMainWindow()
        if scripts and scripts_map.get('current_index', 0) < len(scripts):
            self.filename = scripts[scripts_map['current_index']]
        else:
            self.filename = ''
        self.lineEdit.setText(self.filename)
        self.path = os.path.join(to_abs_path("scripts"))
        
        # Set window icon same as main app
        icon = QIcon()
        icon.addFile(to_abs_path("assets", "Mondrian.ico"))
        self.dialog.setWindowIcon(icon)
        
        self.dialog.setWindowTitle(_tr('文件管理', 'File Manage', '檔案管理'))
        self.file_name.setText(_tr('文件名', 'file name', '檔案名稱'))
        self.choice.setText(_tr('选择', 'choice', '選擇'))
        self.edit.setText(_tr('编辑', 'edit', '編輯'))
        self.rename.setText(_tr('重命名', 'rename', '重新命名'))
    

    def choice_file(self):
        scripts_dir = to_abs_path('scripts')
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
        file = QFileDialog.getOpenFileName(self.main_window, _tr("选择文件", "Select File", "選擇檔案"), scripts_dir, 'Scripts (*.txt *.json5)')[0]
        file_name = re.split(r'\\|\/', file)[-1]
        if file_name != '':
            scripts_map['current_index'] = scripts_map.get(file_name, 0)
            if file_name.strip() != '' and file_name is not None:
                self.lineEdit.setText(file_name)


    def edit_file(self):
        user_platform = platform.system()
        try:
            if user_platform == 'Linux':
                subprocess.call(['xdg-open', os.path.join(self.path, self.lineEdit.text())])
            elif user_platform == 'Darwin':
                # mac
                subprocess.call(['open', os.path.join(self.path, self.lineEdit.text())])
            else:
                os.startfile(os.path.join(self.path, self.lineEdit.text()))
        except FileNotFoundError:
            QMessageBox().warning(self.main_window, _tr("警告", "warning", "警告"), _tr('文件未找到', 'FNF', '檔案未找到'))
            self.lineEdit.setText('')


    def rename_file(self, filename):
        new_file_name = str(QInputDialog.getText(self.main_window, 
                                                 _tr('重命名', 'rename', '重新命名'), 
                                                 _tr('请输入新文件名：', 'PINFN', '請輸入新檔案名稱：'))[0])

        if new_file_name != None and new_file_name.strip() != '':
            if filename.endswith('.txt'):
                if not new_file_name.endswith('.txt'):
                    new_file_name = new_file_name + '.txt'
            elif filename.endswith('.json5'):
                if not new_file_name.endswith('.json5'):
                    new_file_name = new_file_name + '.json5'

            try:
                os.rename(os.path.join(self.path, self.lineEdit.text()), os.path.join(self.path, new_file_name))
                QMessageBox().information(self.main_window, _tr('信息', 'info', '資訊'), _tr('更新成功', 'Success', '更新成功'))
                # 更新
                filename = self.lineEdit.text()
                index = scripts_map.get(filename)
                scripts_map.pop(filename)
                scripts_map[new_file_name] = index
                scripts[index] = new_file_name
                self.lineEdit.setText(new_file_name)
            except FileNotFoundError:
                QMessageBox.warning(self.main_window, _tr('警告', 'warning', '警告'), _tr('文件未找到', 'FNF', '檔案未找到'))
        else:
            QMessageBox.warning(self.main_window, _tr('警告', 'warning', '警告'), _tr('文件名不能为空或空格', 'FNCBEOS', '檔名不能為空或空格'))


    def show(self):
        self.dialog.show()
        self.dialog.exec_()
