# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIView.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget, QCheckBox, QDoubleSpinBox, QSpacerItem)
import assets_rc

import os
import sys

def to_abs_path(*args):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, *args)
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), *args)

class Ui_UIView(object):
    def setupUi(self, UIView):
        if not UIView.objectName():
            UIView.setObjectName(u"UIView")
        UIView.resize(1050, 820)
        icon = QIcon()
        icon.addFile(to_abs_path("assets", "Mondrian.ico"))
        UIView.setWindowIcon(icon)
        
        self.centralwidget = QWidget(UIView)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Main horizontal layout (left + right)
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        
        # ========== LEFT PANEL ==========
        self.leftPanel = QWidget(self.centralwidget)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftLayout = QVBoxLayout(self.leftPanel)
        self.leftLayout.setSpacing(8)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        
        # --- Script Config GroupBox ---
        self.groupBox_2 = QGroupBox(self.leftPanel)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(12, 24, 12, 16)
        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setVerticalSpacing(16)
        self.gridLayout_4.setColumnStretch(0, 0)
        self.gridLayout_4.setColumnStretch(1, 1)
        
        # Script label
        self.label_script = QLabel(self.groupBox_2)
        self.label_script.setObjectName(u"label_script")
        self.label_script.setMinimumWidth(60)
        self.gridLayout_4.addWidget(self.label_script, 0, 0, 1, 1)
        
        # Script dropdown with external file selector
        self.scriptSelectLayout = QHBoxLayout()
        self.scriptSelectLayout.setSpacing(6)

        self.choice_script = QComboBox(self.groupBox_2)
        self.choice_script.setObjectName(u"choice_script")
        sizePolicy.setHeightForWidth(self.choice_script.sizePolicy().hasHeightForWidth())
        self.choice_script.setSizePolicy(sizePolicy)
        self.choice_script.setMinimumWidth(220)
        self.scriptSelectLayout.addWidget(self.choice_script, 1)

        self.bt_select_script = QPushButton(self.groupBox_2)
        self.bt_select_script.setObjectName(u"bt_select_script")
        self.bt_select_script.setMinimumWidth(100)
        self.scriptSelectLayout.addWidget(self.bt_select_script)

        self.gridLayout_4.addLayout(self.scriptSelectLayout, 0, 1, 1, 1)
        
        # Script buttons row
        self.scriptBtnLayout = QHBoxLayout()
        self.scriptBtnLayout.setSpacing(6)
        self.scriptBtnLayout.setContentsMargins(60, 0, 0, 0)  # Indent to align with dropdown
        
        self.bt_choice_file = QPushButton(self.groupBox_2)
        self.bt_choice_file.setObjectName(u"bt_choice_file")
        self.scriptBtnLayout.addWidget(self.bt_choice_file)
        
        self.bt_edit_file = QPushButton(self.groupBox_2)
        self.bt_edit_file.setObjectName(u"bt_edit_file")
        self.scriptBtnLayout.addWidget(self.bt_edit_file)
        
        self.bt_rename_file = QPushButton(self.groupBox_2)
        self.bt_rename_file.setObjectName(u"bt_rename_file")
        self.scriptBtnLayout.addWidget(self.bt_rename_file)
        
        self.bt_clear_files = QPushButton(self.groupBox_2)
        self.bt_clear_files.setObjectName(u"bt_clear_files")
        self.scriptBtnLayout.addWidget(self.bt_clear_files)
        
        spacer_script = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.scriptBtnLayout.addItem(spacer_script)
        
        self.gridLayout_4.addLayout(self.scriptBtnLayout, 1, 0, 1, 2)
        
        # Run times
        self.label_run_times = QLabel(self.groupBox_2)
        self.label_run_times.setObjectName(u"label_run_times")
        self.label_run_times.setMinimumWidth(60)
        self.gridLayout_4.addWidget(self.label_run_times, 2, 0, 1, 1)

        self.stimes_layout = QHBoxLayout()
        self.stimes_layout.setSpacing(6)
        self.stimes = QSpinBox(self.groupBox_2)
        self.stimes.setObjectName(u"stimes")
        self.stimes.setMaximum(99999)
        self.stimes.setValue(1)
        self.stimes_layout.addWidget(self.stimes)
        self.btn_loop_88 = QPushButton(self.groupBox_2)
        self.btn_loop_88.setObjectName(u"btn_loop_88")
        self.btn_loop_88.setMinimumWidth(60)
        self.stimes_layout.addWidget(self.btn_loop_88)
        self.btn_loop_8888 = QPushButton(self.groupBox_2)
        self.btn_loop_8888.setObjectName(u"btn_loop_8888")
        self.btn_loop_8888.setMinimumWidth(60)
        self.stimes_layout.addWidget(self.btn_loop_8888)
        self.btn_loop_88888 = QPushButton(self.groupBox_2)
        self.btn_loop_88888.setObjectName(u"btn_loop_88888")
        self.btn_loop_88888.setMinimumWidth(60)
        self.stimes_layout.addWidget(self.btn_loop_88888)
        spacer_stimes = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.stimes_layout.addItem(spacer_stimes)
        self.gridLayout_4.addLayout(self.stimes_layout, 2, 1, 1, 1)

        # Mouse precision
        self.label_execute_interval = QLabel(self.groupBox_2)
        self.label_execute_interval.setObjectName(u"label_execute_interval")
        self.label_execute_interval.setMinimumWidth(60)
        self.gridLayout_4.addWidget(self.label_execute_interval, 3, 0, 1, 1)

        self.prec_layout = QHBoxLayout()
        self.prec_layout.setSpacing(6)
        self.mouse_move_interval_ms = QSpinBox(self.groupBox_2)
        self.mouse_move_interval_ms.setObjectName(u"mouse_move_interval_ms")
        self.mouse_move_interval_ms.setMinimum(1)
        self.mouse_move_interval_ms.setMaximum(1000)
        self.mouse_move_interval_ms.setValue(100)
        self.prec_layout.addWidget(self.mouse_move_interval_ms)
        self.btn_prec_100 = QPushButton(self.groupBox_2)
        self.btn_prec_100.setObjectName(u"btn_prec_100")
        self.btn_prec_100.setMinimumWidth(60)
        self.prec_layout.addWidget(self.btn_prec_100)
        self.btn_prec_200 = QPushButton(self.groupBox_2)
        self.btn_prec_200.setObjectName(u"btn_prec_200")
        self.btn_prec_200.setMinimumWidth(60)
        self.prec_layout.addWidget(self.btn_prec_200)
        self.btn_prec_500 = QPushButton(self.groupBox_2)
        self.btn_prec_500.setObjectName(u"btn_prec_500")
        self.btn_prec_500.setMinimumWidth(60)
        self.prec_layout.addWidget(self.btn_prec_500)
        spacer_prec = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.prec_layout.addItem(spacer_prec)
        self.gridLayout_4.addLayout(self.prec_layout, 3, 1, 1, 1)
        
        # Pre-delay with random option
        self.label_pre_delay = QLabel(self.groupBox_2)
        self.label_pre_delay.setObjectName(u"label_pre_delay")
        self.label_pre_delay.setMinimumWidth(80)
        self.gridLayout_4.addWidget(self.label_pre_delay, 5, 0, 1, 1)
        
        self.pre_delay_layout = QHBoxLayout()
        self.pre_delay_layout.setSpacing(6)
        
        self.pre_delay_spin = QSpinBox(self.groupBox_2)
        self.pre_delay_spin.setObjectName(u"pre_delay_spin")
        self.pre_delay_spin.setMinimum(0)
        self.pre_delay_spin.setMaximum(9999)
        self.pre_delay_spin.setValue(5)
        self.pre_delay_spin.setSuffix(u" s")
        self.pre_delay_layout.addWidget(self.pre_delay_spin)
        
        self.pre_random_chk = QCheckBox(self.groupBox_2)
        self.pre_random_chk.setObjectName(u"pre_random_chk")
        self.pre_random_chk.setText(u"随机")
        self.pre_delay_layout.addWidget(self.pre_random_chk)
        
        self.pre_random_min = QSpinBox(self.groupBox_2)
        self.pre_random_min.setObjectName(u"pre_random_min")
        self.pre_random_min.setMinimum(0)
        self.pre_random_min.setMaximum(9999)
        self.pre_random_min.setValue(1)
        self.pre_random_min.setSuffix(u" s")
        self.pre_delay_layout.addWidget(self.pre_random_min)
        
        self.pre_random_tilde = QLabel(self.groupBox_2)
        self.pre_random_tilde.setObjectName(u"pre_random_tilde")
        self.pre_random_tilde.setText(u"~")
        self.pre_random_tilde.setEnabled(False)
        self.pre_delay_layout.addWidget(self.pre_random_tilde)
        
        self.pre_random_max = QSpinBox(self.groupBox_2)
        self.pre_random_max.setObjectName(u"pre_random_max")
        self.pre_random_max.setMinimum(0)
        self.pre_random_max.setMaximum(9999)
        self.pre_random_max.setValue(5)
        self.pre_random_max.setSuffix(u" s")
        self.pre_delay_layout.addWidget(self.pre_random_max)
        
        spacer_pre = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.pre_delay_layout.addItem(spacer_pre)
        
        self.gridLayout_4.addLayout(self.pre_delay_layout, 5, 1, 1, 1)
        
        # Post-delay with random option
        self.label_post_delay = QLabel(self.groupBox_2)
        self.label_post_delay.setObjectName(u"label_post_delay")
        self.label_post_delay.setMinimumWidth(80)
        self.gridLayout_4.addWidget(self.label_post_delay, 6, 0, 1, 1)
        
        self.post_delay_layout = QHBoxLayout()
        self.post_delay_layout.setSpacing(6)
        
        self.post_delay_spin = QSpinBox(self.groupBox_2)
        self.post_delay_spin.setObjectName(u"post_delay_spin")
        self.post_delay_spin.setMinimum(0)
        self.post_delay_spin.setMaximum(9999)
        self.post_delay_spin.setValue(10)
        self.post_delay_spin.setSuffix(u" s")
        self.post_delay_layout.addWidget(self.post_delay_spin)
        
        self.post_random_chk = QCheckBox(self.groupBox_2)
        self.post_random_chk.setObjectName(u"post_random_chk")
        self.post_random_chk.setText(u"随机")
        self.post_delay_layout.addWidget(self.post_random_chk)
        
        self.post_random_min = QSpinBox(self.groupBox_2)
        self.post_random_min.setObjectName(u"post_random_min")
        self.post_random_min.setMinimum(0)
        self.post_random_min.setMaximum(9999)
        self.post_random_min.setValue(1)
        self.post_random_min.setSuffix(u" s")
        self.post_delay_layout.addWidget(self.post_random_min)
        
        self.post_random_tilde = QLabel(self.groupBox_2)
        self.post_random_tilde.setObjectName(u"post_random_tilde")
        self.post_random_tilde.setText(u"~")
        self.post_random_tilde.setEnabled(False)
        self.post_delay_layout.addWidget(self.post_random_tilde)
        
        self.post_random_max = QSpinBox(self.groupBox_2)
        self.post_random_max.setObjectName(u"post_random_max")
        self.post_random_max.setMinimum(0)
        self.post_random_max.setMaximum(9999)
        self.post_random_max.setValue(5)
        self.post_random_max.setSuffix(u" s")
        self.post_delay_layout.addWidget(self.post_random_max)
        
        spacer_post = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.post_delay_layout.addItem(spacer_post)
        
        self.gridLayout_4.addLayout(self.post_delay_layout, 6, 1, 1, 1)
        
        # Exec speed
        self.label_exec_speed = QLabel(self.groupBox_2)
        self.label_exec_speed.setObjectName(u"label_exec_speed")
        self.label_exec_speed.setMinimumWidth(60)
        self.gridLayout_4.addWidget(self.label_exec_speed, 8, 0, 1, 1)
        
        self.exec_speed_spin = QDoubleSpinBox(self.groupBox_2)
        self.exec_speed_spin.setObjectName(u"exec_speed_spin")
        self.exec_speed_spin.setMinimum(0.1)
        self.exec_speed_spin.setMaximum(3.0)
        self.exec_speed_spin.setSingleStep(0.1)
        self.exec_speed_spin.setDecimals(1)
        self.exec_speed_spin.setValue(1.0)
        self.exec_speed_spin.setSuffix(u" x")
        self.gridLayout_4.addWidget(self.exec_speed_spin, 8, 1, 1, 1, Qt.AlignLeft)
        
        # Block options
        self.label_block_options = QLabel(self.groupBox_2)
        self.label_block_options.setObjectName(u"label_block_options")
        self.label_block_options.setMinimumWidth(60)
        self.gridLayout_4.addWidget(self.label_block_options, 9, 0, 1, 1)
        
        self.block_options_layout = QHBoxLayout()
        self.block_options_layout.setSpacing(12)
        
        self.chk_block_mouse = QCheckBox(self.groupBox_2)
        self.chk_block_mouse.setObjectName(u"chk_block_mouse")
        self.block_options_layout.addWidget(self.chk_block_mouse)
        
        self.label_block_mouse = QLabel(self.groupBox_2)
        self.label_block_mouse.setObjectName(u"label_block_mouse")
        self.block_options_layout.addWidget(self.label_block_mouse)
        
        self.chk_block_keyboard = QCheckBox(self.groupBox_2)
        self.chk_block_keyboard.setObjectName(u"chk_block_keyboard")
        self.block_options_layout.addWidget(self.chk_block_keyboard)
        
        self.label_block_keyboard = QLabel(self.groupBox_2)
        self.label_block_keyboard.setObjectName(u"label_block_keyboard")
        self.block_options_layout.addWidget(self.label_block_keyboard)
        
        spacer_block = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.block_options_layout.addItem(spacer_block)

        self.bt_default_config = QPushButton(self.groupBox_2)
        self.bt_default_config.setObjectName(u"bt_default_config")
        self.bt_default_config.setMinimumWidth(100)
        self.block_options_layout.addWidget(self.bt_default_config)
        
        self.gridLayout_4.addLayout(self.block_options_layout, 9, 1, 1, 1)
        
        self.leftLayout.addWidget(self.groupBox_2)
        
        # --- Controls GroupBox ---
        self.groupBox_controls = QGroupBox(self.leftPanel)
        self.groupBox_controls.setObjectName(u"groupBox_controls")
        self.groupBox_controls.setMaximumHeight(100)
        self.controlsLayout = QHBoxLayout(self.groupBox_controls)
        self.controlsLayout.setSpacing(10)
        self.controlsLayout.setContentsMargins(12, 16, 12, 12)
        self.controlsLayout.setAlignment(Qt.AlignCenter)
        
        self.btrecord = QPushButton(self.groupBox_controls)
        self.btrecord.setObjectName(u"btrecord")
        sizePolicy1.setHeightForWidth(self.btrecord.sizePolicy().hasHeightForWidth())
        self.btrecord.setSizePolicy(sizePolicy1)
        self.btrecord.setProperty("class", "btn-success")
        self.controlsLayout.addWidget(self.btrecord)
        
        self.btpauserecord = QPushButton(self.groupBox_controls)
        self.btpauserecord.setObjectName(u"btpauserecord")
        self.btpauserecord.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.btpauserecord.sizePolicy().hasHeightForWidth())
        self.btpauserecord.setSizePolicy(sizePolicy1)
        self.btpauserecord.setProperty("class", "btn-warning")
        self.controlsLayout.addWidget(self.btpauserecord)
        
        self.btrun = QPushButton(self.groupBox_controls)
        self.btrun.setObjectName(u"btrun")
        sizePolicy1.setHeightForWidth(self.btrun.sizePolicy().hasHeightForWidth())
        self.btrun.setSizePolicy(sizePolicy1)
        self.btrun.setProperty("class", "btn-info")
        self.controlsLayout.addWidget(self.btrun)
        
        self.btstop = QPushButton(self.groupBox_controls)
        self.btstop.setObjectName(u"btstop")
        self.btstop.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.btstop.sizePolicy().hasHeightForWidth())
        self.btstop.setSizePolicy(sizePolicy1)
        self.btstop.setProperty("class", "btn-danger")
        self.controlsLayout.addWidget(self.btstop)
        
        self.leftLayout.addWidget(self.groupBox_controls)
        
        # --- Hotkeys GroupBox ---
        self.groupBox = QGroupBox(self.leftPanel)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setSpacing(8)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(12, 16, 12, 12)
        
        self.label_start_key = QLabel(self.groupBox)
        self.label_start_key.setObjectName(u"label_start_key")
        self.label_start_key.setMinimumWidth(80)
        self.gridLayout_3.addWidget(self.label_start_key, 0, 0, 1, 1)
        
        self.hotkey_start = QPushButton(self.groupBox)
        self.hotkey_start.setObjectName(u"hotkey_start")
        sizePolicy1.setHeightForWidth(self.hotkey_start.sizePolicy().hasHeightForWidth())
        self.hotkey_start.setSizePolicy(sizePolicy1)
        self.gridLayout_3.addWidget(self.hotkey_start, 0, 1, 1, 1)
        
        self.bt_change_start = QPushButton(self.groupBox)
        self.bt_change_start.setObjectName(u"bt_change_start")
        self.gridLayout_3.addWidget(self.bt_change_start, 0, 2, 1, 1)
        
        self.label_record = QLabel(self.groupBox)
        self.label_record.setObjectName(u"label_record")
        self.label_record.setMinimumWidth(80)
        self.gridLayout_3.addWidget(self.label_record, 1, 0, 1, 1)
        
        self.hotkey_record = QPushButton(self.groupBox)
        self.hotkey_record.setObjectName(u"hotkey_record")
        sizePolicy1.setHeightForWidth(self.hotkey_record.sizePolicy().hasHeightForWidth())
        self.hotkey_record.setSizePolicy(sizePolicy1)
        self.gridLayout_3.addWidget(self.hotkey_record, 1, 1, 1, 1)
        
        self.bt_change_record = QPushButton(self.groupBox)
        self.bt_change_record.setObjectName(u"bt_change_record")
        self.gridLayout_3.addWidget(self.bt_change_record, 1, 2, 1, 1)
        
        self.label_stop = QLabel(self.groupBox)
        self.label_stop.setObjectName(u"label_stop")
        self.label_stop.setMinimumWidth(80)
        self.gridLayout_3.addWidget(self.label_stop, 2, 0, 1, 1)
        
        self.hotkey_stop = QPushButton(self.groupBox)
        self.hotkey_stop.setObjectName(u"hotkey_stop")
        sizePolicy1.setHeightForWidth(self.hotkey_stop.sizePolicy().hasHeightForWidth())
        self.hotkey_stop.setSizePolicy(sizePolicy1)
        self.gridLayout_3.addWidget(self.hotkey_stop, 2, 1, 1, 1)
        
        self.bt_change_stop = QPushButton(self.groupBox)
        self.bt_change_stop.setObjectName(u"bt_change_stop")
        self.gridLayout_3.addWidget(self.bt_change_stop, 2, 2, 1, 1)
        
        self.bt_default_hotkey = QPushButton(self.groupBox)
        self.bt_default_hotkey.setObjectName(u"bt_default_hotkey")
        self.gridLayout_3.addWidget(self.bt_default_hotkey, 2, 3, 1, 1)
        
        self.label_language = QLabel(self.groupBox)
        self.label_language.setObjectName(u"label_language")
        self.label_language.setMinimumWidth(80)
        self.gridLayout_3.addWidget(self.label_language, 3, 0, 1, 1)
        
        self.choice_language = QComboBox(self.groupBox)
        self.choice_language.setObjectName(u"choice_language")
        sizePolicy1.setHeightForWidth(self.choice_language.sizePolicy().hasHeightForWidth())
        self.choice_language.setSizePolicy(sizePolicy1)
        self.gridLayout_3.addWidget(self.choice_language, 3, 1, 1, 2)
        
        # Theme selector
        self.label_theme = QLabel(self.groupBox)
        self.label_theme.setObjectName(u"label_theme")
        self.label_theme.setMinimumWidth(80)
        self.gridLayout_3.addWidget(self.label_theme, 4, 0, 1, 1)
        
        self.choice_theme = QComboBox(self.groupBox)
        self.choice_theme.setObjectName(u"choice_theme")
        sizePolicy1.setHeightForWidth(self.choice_theme.sizePolicy().hasHeightForWidth())
        self.choice_theme.setSizePolicy(sizePolicy1)
        self.gridLayout_3.addWidget(self.choice_theme, 4, 1, 1, 2)
        
        self.leftLayout.addWidget(self.groupBox)
        
        # Add left panel to main layout
        self.mainLayout.addWidget(self.leftPanel, 4)
        
        # ========== RIGHT PANEL (Log) ==========
        self.rightPanel = QWidget(self.centralwidget)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightLayout = QVBoxLayout(self.rightPanel)
        self.rightLayout.setSpacing(6)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        
        self.logHeader = QHBoxLayout()
        self.logHeader.setSpacing(6)
        
        self.tnumrd = QLabel(self.rightPanel)
        self.tnumrd.setObjectName(u"tnumrd")
        self.logHeader.addWidget(self.tnumrd)
        
        self.label_cursor_pos = QLabel(self.rightPanel)
        self.label_cursor_pos.setObjectName(u"label_cursor_pos")
        self.label_cursor_pos.setLayoutDirection(Qt.RightToLeft)
        self.label_cursor_pos.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.logHeader.addWidget(self.label_cursor_pos)
        
        self.rightLayout.addLayout(self.logHeader)
        
        self.textlog = QTextEdit(self.rightPanel)
        self.textlog.setObjectName(u"textlog")
        self.textlog.setEnabled(True)
        self.textlog.setReadOnly(True)
        # Dark background for log
        self.textlog.setStyleSheet("QTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; }")
        self.rightLayout.addWidget(self.textlog)
        
        self.mainLayout.addWidget(self.rightPanel, 5)
        
        UIView.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(UIView)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1050, 24))
        UIView.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(UIView)
        self.statusbar.setObjectName(u"statusbar")
        UIView.setStatusBar(self.statusbar)
        
        self.retranslateUi(UIView)
        QMetaObject.connectSlotsByName(UIView)
    
    def retranslateUi(self, UIView):
        UIView.setWindowTitle(QCoreApplication.translate("UIView", u"AKA-Yomi（Automated Key Action Yield Operation Monitor Input 基于 KeymouseGo v5.2.1）", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("UIView", u"自动化配置", None))
        self.label_script.setText(QCoreApplication.translate("UIView", u"脚本", None))
        self.bt_select_script.setText(QCoreApplication.translate("UIView", u"选择脚本", None))
        self.bt_choice_file.setText(QCoreApplication.translate("UIView", u"默认路径", None))
        self.bt_edit_file.setText(QCoreApplication.translate("UIView", u"编辑文件", None))
        self.bt_rename_file.setText(QCoreApplication.translate("UIView", u"重命名", None))
        self.bt_clear_files.setText(QCoreApplication.translate("UIView", u"清除", None))
        self.label_run_times.setText(QCoreApplication.translate("UIView", u"执行次数", None))
        self.label_execute_interval.setText(QCoreApplication.translate("UIView", u"鼠标精度", None))
        self.groupBox_controls.setTitle(QCoreApplication.translate("UIView", u"执行控制", None))
        self.btrecord.setText(QCoreApplication.translate("UIView", u"开始录制", None))
        self.btpauserecord.setText(QCoreApplication.translate("UIView", u"暂停录制", None))
        self.btrun.setText(QCoreApplication.translate("UIView", u"启动", None))
        self.btstop.setText(QCoreApplication.translate("UIView", u"停止", None))
        self.groupBox.setTitle(QCoreApplication.translate("UIView", u"设置", None))
        self.label_start_key.setText(QCoreApplication.translate("UIView", u"开始/暂停执行", None))
        self.hotkey_start.setText("")
        self.bt_change_start.setText(QCoreApplication.translate("UIView", u"更改", None))
        self.label_record.setText(QCoreApplication.translate("UIView", u"开始/暂停录制", None))
        self.hotkey_record.setText("")
        self.bt_change_record.setText(QCoreApplication.translate("UIView", u"更改", None))
        self.label_stop.setText(QCoreApplication.translate("UIView", u"终止录制/执行", None))
        self.hotkey_stop.setText("")
        self.bt_change_stop.setText(QCoreApplication.translate("UIView", u"更改", None))
        self.bt_default_hotkey.setText(QCoreApplication.translate("UIView", u"默认", None))
        self.label_language.setText(QCoreApplication.translate("UIView", u"语言", None))
        self.label_theme.setText(QCoreApplication.translate("UIView", u"主题", None))
        self.label_pre_delay.setText(QCoreApplication.translate("UIView", u"运行前延迟", None))
        self.label_post_delay.setText(QCoreApplication.translate("UIView", u"运行后延迟", None))
        self.label_exec_speed.setText(QCoreApplication.translate("UIView", u"执行速度", None))
        self.label_block_options.setText(QCoreApplication.translate("UIView", u"屏蔽选项", None))
        self.label_block_mouse.setText(QCoreApplication.translate("UIView", u"鼠标", None))
        self.label_block_keyboard.setText(QCoreApplication.translate("UIView", u"键盘", None))
        self.bt_default_config.setText(QCoreApplication.translate("UIView", u"默认配置", None))
        self.tnumrd.setText(QCoreApplication.translate("UIView", u"完成", None))
        self.label_cursor_pos.setText(QCoreApplication.translate("UIView", u"光标位置: (0, 0)", None))
