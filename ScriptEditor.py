# -*- coding: utf-8 -*-
import json5
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                 QTextEdit, QPushButton, QLabel, QMessageBox)

from KeymouseGo import to_abs_path


def _tr(zh, en, tw):
    """Get text based on current language setting."""
    try:
        from PySide6.QtCore import QSettings
        config = QSettings('config.ini', QSettings.IniFormat)
        lang = config.value("Config/Language", "简体中文")
    except:
        lang = "简体中文"
    if lang == 'English':
        return en
    elif lang == '繁體中文':
        return tw
    return zh


class ScriptEditor(QDialog):
    def __init__(self, script_path, parent=None):
        super().__init__(parent)
        self.script_path = script_path
        self.setWindowTitle(_tr('脚本编辑器', 'Script Editor', '腳本編輯器'))
        self.setMinimumSize(600, 400)
        
        # Set icon
        icon = QIcon()
        icon.addFile(to_abs_path("assets", "Mondrian.ico"))
        self.setWindowIcon(icon)
        
        layout = QVBoxLayout(self)
        
        # File path label
        self.path_label = QLabel(os.path.basename(script_path))
        self.path_label.setStyleSheet("color: #666; padding: 4px;")
        layout.addWidget(self.path_label)
        
        # Text editor
        self.editor = QTextEdit()
        font = QFont("Consolas", 10)
        self.editor.setFont(font)
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.editor)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.save_btn = QPushButton(_tr('保存', 'Save', '儲存'))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #449d44; }
        """)
        self.save_btn.clicked.connect(self.save_file)
        
        self.close_btn = QPushButton(_tr('关闭', 'Close', '關閉'))
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0ad4e;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ec971f; }
        """)
        self.close_btn.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)
        
        # Load file content
        self.load_file()
    
    def load_file(self):
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.editor.setPlainText(content)
        except Exception as e:
            QMessageBox.warning(self, _tr('错误', 'Error', '錯誤'), 
                               _tr('无法读取文件：', 'Cannot read file: ', '無法讀取檔案：') + str(e))
    
    def save_file(self):
        try:
            content = self.editor.toPlainText()
            with open(self.script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, _tr('成功', 'Success', '成功'), 
                                   _tr('文件已保存', 'File saved', '檔案已儲存'))
        except Exception as e:
            QMessageBox.warning(self, _tr('错误', 'Error', '錯誤'), 
                               _tr('保存失败：', 'Save failed: ', '儲存失敗：') + str(e))
