# -*- encoding:utf-8 -*-
import datetime
from typing import List

import json5
import os
import sys
import subprocess
import threading
import platform
import locale
import Recorder

from PySide6.QtGui import QTextCursor
from PySide6.QtCore import *
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox
from loguru import logger

from Event import ScriptEvent, flag_multiplemonitor
from Plugin.Manager import PluginManager
from UIView import Ui_UIView

from KeymouseGo import to_abs_path
from Util.RunScriptClass import RunScriptClass
from Util.Global import State
from Util.ClickedLabel import Label


os.environ['QT_ENABLE_HIGHDPI_SCALING'] = "1"
# if platform.system() == 'Windows':
#     HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#                 'XButton1', 'XButton2', 'Middle']
# else:
#     HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#                 'Middle']

logger.remove()
if sys.stdout is not None:
    logger.add(sys.stdout, backtrace=True, diagnose=True,
               level='DEBUG')
logger.add(to_abs_path('logs', '{time}.log'), rotation='20MB', backtrace=True, diagnose=True,
           level='INFO')


def get_assets_path(*paths):
    # pyinstaller -F --add-data ./assets;assets KeymouseGo.py
    try:
        root = sys._MEIPASS
    except:
        root = os.getcwd()
    return os.path.join(root, 'assets', *paths)


scripts = []
scripts_map = {'current_index': 0, 'choice_language': '简体中文'}


def get_script_list_from_dir():
    global scripts

    if not os.path.exists(to_abs_path('scripts')):
        os.mkdir(to_abs_path('scripts'))
    scripts = os.listdir(to_abs_path('scripts'))[::-1]
    scripts = list(filter(lambda s: s.endswith('.txt') or s.endswith('.json5'), scripts))


def update_script_map():
    global scripts_map
    
    for (i, item) in enumerate(scripts):
        scripts_map[item] = i

def get_script_dir():
    return to_abs_path('scripts')

class UIFunc(QMainWindow, Ui_UIView):
    updateStateSignal: Signal = Signal(State)

    def __init__(self, app):
        global scripts

        super(UIFunc, self).__init__()

        logger.info('assets root:{0}'.format(get_assets_path()))

        self.setupUi(self)

        self.app = app

        self.state = State(State.IDLE)

        self.config = self.loadconfig()

        # Apply MUI theme
        self.apply_mui_theme()

        self.setFocusPolicy(Qt.NoFocus)

        self.trans = QTranslator(self)
        self.choice_language.addItems(['简体中文', 'English', '繁體中文'])
        self.choice_language.currentTextChanged.connect(self.onchangelang)

        # Theme selector
        self.theme_name_map = {
            'Material Light': {'简体中文': 'Material 浅色', 'English': 'Material Light', '繁體中文': 'Material 淺色'},
            'Ant Design Dark': {'简体中文': '暗黑模式', 'English': 'Ant Design Dark', '繁體中文': '暗黑模式'},
            'Cartoon': {'简体中文': '卡通', 'English': 'Cartoon', '繁體中文': '卡通'},
            'Geek': {'简体中文': '极客', 'English': 'Geek', '繁體中文': '極客'},
            'Bootstrap': {'简体中文': 'Bootstrap 风格', 'English': 'Bootstrap', '繁體中文': 'Bootstrap 風格'},
            'Glass': {'简体中文': '玻璃拟态', 'English': 'Glass', '繁體中文': '玻璃擬態'},
        }
        self.choice_theme.addItems(list(self.theme_name_map.keys()))
        theme = self.config.value("Config/Theme", "Material Light")
        self.choice_theme.setCurrentText(theme)
        self.choice_theme.currentTextChanged.connect(self.onchangetheme)
        # Apply localized theme names for current language
        current_lang = self.choice_language.currentText()
        self._update_theme_display_names(current_lang)

        # 获取默认的地区设置并应用翻译
        language = '简体中文' if locale.getdefaultlocale()[0] == 'zh_CN' else 'English'
        self.choice_language.setCurrentText(language)
        self.onchangelang()

        get_script_list_from_dir()
        update_script_map()
        self.scripts = scripts
        self.choice_script.addItems(self.scripts)
        if self.scripts:
            self.choice_script.setCurrentIndex(0)
        else:
            self.btrun.setEnabled(False)

        PluginManager.reload()

        # Config
        self.stimes.setValue(int(self.config.value("Config/LoopTimes")))
        self.mouse_move_interval_ms.setValue(int(self.config.value("Config/Precision")))
        if self.config.value('Config/Script') is not None and self.config.value('Config/Script') in self.scripts:
            self.choice_script.setCurrentText(self.config.value('Config/Script'))
        self.stimes.valueChanged.connect(self.onconfigchange)

        # Quick loop buttons
        self.btn_loop_88.setText("88")
        self.btn_loop_88.setMinimumWidth(60)
        self.btn_loop_88.clicked.connect(lambda: self._set_loop_times(88))
        self.btn_loop_8888.setText("8888")
        self.btn_loop_8888.setMinimumWidth(60)
        self.btn_loop_8888.clicked.connect(lambda: self._set_loop_times(8888))
        self.btn_loop_88888.setText("88888")
        self.btn_loop_88888.setMinimumWidth(60)
        self.btn_loop_88888.clicked.connect(lambda: self._set_loop_times(88888))

        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(Recorder.set_interval)

        # Quick precision buttons
        self.btn_prec_100.setText("100")
        self.btn_prec_100.setMinimumWidth(60)
        self.btn_prec_100.clicked.connect(lambda: self._set_precision(100))
        self.btn_prec_200.setText("200")
        self.btn_prec_200.setMinimumWidth(60)
        self.btn_prec_200.clicked.connect(lambda: self._set_precision(200))
        self.btn_prec_500.setText("500")
        self.btn_prec_500.setMinimumWidth(60)
        self.btn_prec_500.clicked.connect(lambda: self._set_precision(500))

        self.choice_script.currentTextChanged.connect(self.onconfigchange)
        self.hotkey_stop.setText(self.config.value("Config/StopHotKey"))
        self.hotkey_start.setText(self.config.value("Config/StartHotKey"))
        self.hotkey_record.setText(self.config.value("Config/RecordHotKey"))

        self.textlog.textChanged.connect(lambda: self.textlog.moveCursor(QTextCursor.End))

        self.record = []

        self.actioncount = 0

        # For better thread control
        self.runthread = None

        self.btrun.clicked.connect(self.OnBtrunButton)
        self.btrecord.clicked.connect(self.OnBtrecordButton)
        self.btpauserecord.clicked.connect(self.OnPauseRecordButton)
        self.btstop.clicked.connect(self.OnBtStopButton)
        self.bt_choice_file.clicked.connect(self.OnBtOpenScriptFilesButton)
        self.bt_edit_file.clicked.connect(self.OnBtEditFileButton)
        self.bt_rename_file.clicked.connect(self.OnBtRenameFileButton)
        self.bt_clear_files.clicked.connect(self.OnBtClearFilesButton)
        self.choice_language.installEventFilter(self)
        self.choice_script.installEventFilter(self)
        self.btrun.installEventFilter(self)
        self.btrecord.installEventFilter(self)
        self.btpauserecord.installEventFilter(self)
        self.btstop.installEventFilter(self)
        self.bt_choice_file.installEventFilter(self)

        # 组合键缓冲池，[ctrl,shift,alt,cmd/start/win]可用作组合键，但不能单独用作启动热键
        self.keys_pool: List[str] = []
        self.hotkey_set_btn = None
        self.hotkey_stop.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_stop))
        self.hotkey_start.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_start))
        self.hotkey_record.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_record))
        self.bt_change_start.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_start))
        self.bt_change_record.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_record))
        self.bt_change_stop.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_stop))
        self.bt_default_hotkey.clicked.connect(self.OnBtDefaultHotkey)

        # Random delay checkboxes
        self.pre_random_chk.stateChanged.connect(self.OnPreRandomChanged)
        self.post_random_chk.stateChanged.connect(self.OnPostRandomChanged)

        # Uniform component widths
        for combo in self.findChildren(QComboBox):
            combo.setMinimumWidth(120)
        for spin in self.findChildren(QSpinBox):
            spin.setMinimumWidth(80)
        for spin in self.findChildren(QDoubleSpinBox):
            spin.setMinimumWidth(80)
        for btn in self.findChildren(QPushButton):
            if btn not in [self.btn_loop_88, self.btn_loop_8888, self.btn_loop_88888,
                           self.btn_prec_100, self.btn_prec_200, self.btn_prec_500]:
                btn.setMinimumWidth(80)

        # 热键引发状态转移
        def check_hotkeys(key_name):
            if key_name in Recorder.globals.key_combination_trigger:
                if self.state == State.SETTING_HOT_KEYS:
                    self.hotkey_set_btn.setText(self._format_hotkey_display('+'.join(self.keys_pool)))
                return False
            key_name = '+'.join([*self.keys_pool, key_name])

            if self.state == State.SETTING_HOT_KEYS:
                for btn in [self.hotkey_start, self.hotkey_record, self.hotkey_stop]:
                    if btn is not self.hotkey_set_btn and btn.text() != '' and btn.text().lower() == key_name.lower():
                        self.keys_pool.clear()
                        self.hotkey_set_btn.setText('')
                        self.update_state(State.IDLE)
                        return False
                self.hotkey_set_btn.setText(self._format_hotkey_display(key_name))
                self.update_state(State.IDLE)
                self.onconfigchange()
                return False

            start_name = self.hotkey_start.text()
            stop_name = self.hotkey_stop.text()
            record_name = self.hotkey_record.text()

            if key_name.lower() == start_name.lower():
                if self.state == State.IDLE:
                    logger.debug('{0} host start'.format(key_name))
                    self.OnBtrunButton()
                elif self.state == State.RUNNING:
                    logger.info('Script pause')
                    logger.debug('{0} host pause'.format(key_name))
                    self.runthread.set_pause()
                    self.update_state(State.PAUSE_RUNNING)
                elif self.state == State.PAUSE_RUNNING:
                    logger.info('Script resume')
                    self.runthread.resume()
                    logger.debug('{0} host resume'.format(key_name))
                    self.update_state(State.RUNNING)
            elif key_name.lower() == stop_name.lower():
                if self.state == State.RUNNING or self.state == State.PAUSE_RUNNING:
                    logger.info('Script stop')
                    self.tnumrd.setText('broken')
                    self.runthread.resume()
                    logger.debug('{0} host stop'.format(key_name))
                    self.update_state(State.IDLE)
                elif self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
                    self.recordMethod()
                    logger.info('Record stop')
                    logger.debug('{0} host stop record'.format(key_name))
            elif key_name.lower() == record_name.lower():
                if self.state == State.RECORDING:
                    self.pauseRecordMethod()
                    logger.debug('{0} host pause record'.format(key_name))
                elif self.state == State.PAUSE_RECORDING:
                    self.pauseRecordMethod()
                    logger.debug('{0} host resume record'.format(key_name))
                elif self.state == State.IDLE:
                    self.recordMethod()
                    logger.debug('{0} host start record'.format(key_name))
            return key_name in [start_name, stop_name, record_name]

        @Slot(ScriptEvent)
        def on_record_event(event: ScriptEvent):
            # 判断mouse热键
            if event.event_type == "EM":
                name = event.action_type
                if 'mouse x1 down' == name and check_hotkeys('xbutton1'):
                    return
                elif 'mouse x2 down' == name and check_hotkeys('xbutton2'):
                    return
                elif 'mouse middle down' == name and check_hotkeys('middle'):
                    return
            else:
                key_name = event.action[1].lower()
                if event.action_type == 'key down':
                    if key_name in Recorder.globals.key_combination_trigger and len(self.keys_pool) < 3 and key_name not in self.keys_pool:
                        self.keys_pool.append(key_name)
                    # listen for start/stop script
                    # start_name = 'f6'  # as default
                    # stop_name = 'f9'  # as default
                    check_hotkeys(key_name)
                elif event.action_type == 'key up':
                    if key_name in Recorder.globals.key_combination_trigger and key_name in self.keys_pool:
                        self.keys_pool.remove(key_name)
                        check_hotkeys(key_name)
                # 不录制热键
                for btn in [self.hotkey_start, self.hotkey_record, self.hotkey_stop]:
                    if key_name == btn.text().lower():
                        return
            # 录制事件
            if self.state == State.RECORDING:
                if event.event_type == 'EM' and not flag_multiplemonitor:
                    tx, ty = event.action
                    event.action = ['{0}%'.format(tx), '{0}%'.format(ty)]
                event_dict = event.__dict__
                event_dict['type'] = 'event'
                # PluginManager.call_record(event_dict)
                self.record.append(event_dict)
                self.actioncount = self.actioncount + 1
                text = self._tr('已录制 %d 个动作', '%d actions recorded', '已錄製 %d 個動作') % self.actioncount
                logger.debug('Recorded %s' % event)
                self.tnumrd.setText(text)
                self.textlog.append(str(event))
        logger.debug('Initialize at thread ' + str(QThread.currentThread()))
        Recorder.setuphook()
        Recorder.set_callback(on_record_event)
        Recorder.set_cursor_pose_change(self.cursor_pos_change)
        Recorder.set_interval(self.mouse_move_interval_ms.value())

    def eventFilter(self, watched, event: QEvent):
        et: QEvent.Type = event.type()
        # print(event, et)
        if et == QEvent.KeyPress or et == QEvent.KeyRelease:
            return True
        return super(UIFunc, self).eventFilter(watched, event)

    def onconfigchange(self):
        self.config.setValue("Config/LoopTimes", self.stimes.value())
        self.config.setValue("Config/Precision", self.mouse_move_interval_ms.value())
        self.config.setValue("Config/Theme", self.choice_theme.currentText())
        self.config.setValue("Config/Script", self.choice_script.currentText())
        self.config.setValue("Config/StartHotKey", self.hotkey_start.text())
        self.config.setValue("Config/StopHotKey", self.hotkey_stop.text())
        self.config.setValue("Config/RecordHotKey", self.hotkey_record.text())

    def _set_loop_times(self, value):
        self.stimes.setValue(value)
        self.onconfigchange()

    def _set_precision(self, value):
        self.mouse_move_interval_ms.setValue(value)
        self.onconfigchange()

    def onchangelang(self):
        global scripts_map

        logger.info(f'onchangelang called: {self.choice_language.currentText()}')

        lang = self.choice_language.currentText()
        self._apply_translation(lang)

        # Update theme selector display names for current language
        self._update_theme_display_names(lang)

        self.hotkey_stop.setText(self._format_hotkey_display(self.config.value("Config/StopHotKey")))
        self.hotkey_start.setText(self._format_hotkey_display(self.config.value("Config/StartHotKey")))
        self.hotkey_record.setText(self._format_hotkey_display(self.config.value("Config/RecordHotKey")))
        self.config.setValue("Config/Language", lang)

        # Restore hard-coded texts
        self.btn_loop_88.setText("88")
        self.btn_loop_8888.setText("8888")
        self.btn_loop_88888.setText("88888")
        self.btn_prec_100.setText("100")
        self.btn_prec_200.setText("200")
        self.btn_prec_500.setText("500")

    def _apply_translation(self, lang):
        """Directly apply translations based on language name."""
        # GroupBox titles (use setTitle)
        group_titles = {
            'groupBox_2': {'简体中文': '自动化配置', 'English': 'Automation Config', '繁體中文': '自動化配置'},
            'groupBox_controls': {'简体中文': '执行控制', 'English': 'Execution Control', '繁體中文': '執行控制'},
            'groupBox': {'简体中文': '设置', 'English': 'Settings', '繁體中文': '設定'},
        }
        for attr_name, lang_texts in group_titles.items():
            widget = getattr(self, attr_name, None)
            if widget is not None and lang in lang_texts:
                widget.setTitle(lang_texts[lang])
        
        # Label and Button texts (use setText)
        texts = {
            'label_script': {'简体中文': '脚本', 'English': 'Script', '繁體中文': '腳本'},
            'bt_choice_file': {'简体中文': '选择文件', 'English': 'Select File', '繁體中文': '選擇檔案'},
            'bt_edit_file': {'简体中文': '编辑文件', 'English': 'Edit File', '繁體中文': '編輯檔案'},
            'bt_rename_file': {'简体中文': '重命名', 'English': 'Rename', '繁體中文': '重新命名'},
            'bt_clear_files': {'简体中文': '清除脚本', 'English': 'Clear Scripts', '繁體中文': '清除腳本'},
            'label_run_times': {'简体中文': '执行次数', 'English': 'Run Times', '繁體中文': '執行次數'},
            'label_execute_interval': {'简体中文': '鼠标精度', 'English': 'Mouse Precision', '繁體中文': '滑鼠精度'},
            'btrecord': {'简体中文': '开始录制', 'English': 'Record', '繁體中文': '開始錄製'},
            'btpauserecord': {'简体中文': '暂停录制', 'English': 'Pause Record', '繁體中文': '暫停錄製'},
            'btrun': {'简体中文': '启动', 'English': 'Launch', '繁體中文': '啟動'},
            'btstop': {'简体中文': '停止', 'English': 'Stop', '繁體中文': '停止'},
            'label_start_key': {'简体中文': '开始/暂停执行', 'English': 'Start/Pause Execution', '繁體中文': '開始/暫停執行'},
            'label_record': {'简体中文': '开始/暂停录制', 'English': 'Start/Pause Recording', '繁體中文': '開始/暫停錄製'},
            'label_stop': {'简体中文': '终止录制/执行', 'English': 'Stop Recording/Execution', '繁體中文': '終止錄製/執行'},
            'bt_default_hotkey': {'简体中文': '默认', 'English': 'Default', '繁體中文': '預設'},
            'label_language': {'简体中文': '语言', 'English': 'Language', '繁體中文': '語言'},
            'label_theme': {'简体中文': '主题', 'English': 'Theme', '繁體中文': '主題'},
            'label_pre_delay': {'简体中文': '运行前延迟', 'English': 'Pre-run Delay', '繁體中文': '執行前延遲'},
            'label_post_delay': {'简体中文': '运行后延迟', 'English': 'Post-run Delay', '繁體中文': '執行後延遲'},
            'label_exec_speed': {'简体中文': '执行速度', 'English': 'Execution Speed', '繁體中文': '執行速度'},
            'label_block_options': {'简体中文': '屏蔽选项', 'English': 'Block Options', '繁體中文': '遮蔽選項'},
            'label_block_mouse': {'简体中文': '鼠标', 'English': 'Mouse', '繁體中文': '滑鼠'},
            'label_block_keyboard': {'简体中文': '键盘', 'English': 'Keyboard', '繁體中文': '鍵盤'},
            'tnumrd': {'简体中文': '完成', 'English': 'Finished', '繁體中文': '完成'},
        }
        
        # Update cursor position label prefix based on language
        cursor_pos_prefixes = {
            '简体中文': '鼠标坐标',
            'English': 'Mouse Position',
            '繁體中文': '滑鼠座標',
        }
        self.cursor_pos_prefix = cursor_pos_prefixes.get(lang, 'Mouse Position')
        
        for attr_name, lang_texts in texts.items():
            widget = getattr(self, attr_name, None)
            if widget is not None and lang in lang_texts:
                widget.setText(lang_texts[lang])
        
        # Handle multiple widgets with same text
        change_text = {'简体中文': '更改', 'English': 'Change', '繁體中文': '更改'}
        random_text = {'简体中文': '随机', 'English': 'Random', '繁體中文': '隨機'}
        
        t = change_text.get(lang, '更改')
        self.bt_change_start.setText(t)
        self.bt_change_record.setText(t)
        self.bt_change_stop.setText(t)
        
        t = random_text.get(lang, '随机')
        self.pre_random_chk.setText(t)
        self.post_random_chk.setText(t)
        
        logger.info(f'Applied translation for {lang}')

    def closeEvent(self, event):
        self.config.sync()
        Recorder.dispose()
        if self.state == State.PAUSE_RUNNING:
            self.update_state(State.RUNNING)
        elif self.state == State.PAUSE_RECORDING:
            self.update_state(State.RECORDING)
        if self.runthread:
            self.runthread.resume()
        event.accept()

    def loadconfig(self):
        if not os.path.exists(to_abs_path('config.ini')):
            with open(to_abs_path('config.ini'), 'w', encoding='utf-8') as f:
                f.write('[Config]\n'
                        'StartHotKey=F6\n'
                        'StopHotKey=F9\n'
                        'RecordHotKey=F10\n'
                        'LoopTimes=1\n'
                        'Precision=200\n'
                        'Language=zh-cn\n'
                        'Theme=Default\n')
        return QSettings(to_abs_path('config.ini'), QSettings.IniFormat)

    def apply_mui_theme(self):
        theme = self.config.value("Config/Theme", "Material Light")
        self.load_theme(theme)

    def load_theme(self, theme_name):
        if theme_name == "Ant Design Dark":
            qss_path = to_abs_path('assets', 'dark_theme.qss')
        elif theme_name == "Cartoon":
            qss_path = to_abs_path('assets', 'cartoon_theme.qss')
        elif theme_name == "Geek":
            qss_path = to_abs_path('assets', 'geek_theme.qss')
        elif theme_name == "Bootstrap":
            qss_path = to_abs_path('assets', 'bootstrap_theme.qss')
        elif theme_name == "Glass":
            qss_path = to_abs_path('assets', 'glass_theme.qss')
        else:
            qss_path = to_abs_path('assets', 'mui_theme.qss')
        try:
            with open(qss_path, 'r', encoding='utf-8') as f:
                qss_content = f.read()
            assets_dir = to_abs_path('assets').replace('\\', '/')
            qss_content = qss_content.replace('url(:/pic/arrow_down.svg)', f'url({assets_dir}/arrow_down.svg)')
            qss_content = qss_content.replace('url(:/pic/arrow_up.svg)', f'url({assets_dir}/arrow_up.svg)')
            qss_content = qss_content.replace('url(:/pic/arrow_down_white.svg)', f'url({assets_dir}/arrow_down_white.svg)')
            qss_content = qss_content.replace('url(:/pic/arrow_up_white.svg)', f'url({assets_dir}/arrow_up_white.svg)')
            qss_content = qss_content.replace('url(:/pic/arrow_down_cartoon.svg)', f'url({assets_dir}/arrow_down_cartoon.svg)')
            qss_content = qss_content.replace('url(:/pic/arrow_up_cartoon.svg)', f'url({assets_dir}/arrow_up_cartoon.svg)')
            self.app.setStyleSheet(qss_content)
            logger.info(f'Theme "{theme_name}" applied successfully')
        except Exception as e:
            logger.warning(f'Failed to load theme "{theme_name}": {e}')

    def _update_theme_display_names(self, lang):
        """Update theme selector items to show localized names."""
        current_theme_key = self.config.value("Config/Theme", "Material Light")
        self.choice_theme.blockSignals(True)
        current_index = self.choice_theme.currentIndex()
        self.choice_theme.clear()
        for key, lang_map in self.theme_name_map.items():
            display_name = lang_map.get(lang, key)
            self.choice_theme.addItem(display_name, userData=key)
        # Restore selection by key
        for i in range(self.choice_theme.count()):
            if self.choice_theme.itemData(i) == current_theme_key:
                self.choice_theme.setCurrentIndex(i)
                break
        self.choice_theme.blockSignals(False)

    def onchangetheme(self):
        index = self.choice_theme.currentIndex()
        theme_key = self.choice_theme.itemData(index)
        if theme_key:
            self.load_theme(theme_key)
            self.config.setValue("Config/Theme", theme_key)

    def get_script_path(self):
        i = self.choice_script.currentIndex()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(to_abs_path('scripts'), script)
        logger.info('Script path: {0}'.format(path))
        return path

    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.json5' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.json5' % now.strftime('%m%d_%H%M%S')
        self.scripts.insert(0, script)
        update_script_map()
        self.choice_script.clear()
        self.choice_script.addItems(self.scripts)
        self.choice_script.setCurrentIndex(0)
        return self.get_script_path()

    def _tr(self, zh, en, tw):
        """Get text based on current language setting."""
        lang = self.config.value("Config/Language", "简体中文")
        if lang == 'English':
            return en
        elif lang == '繁體中文':
            return tw
        return zh

    def pauseRecordMethod(self):
        if self.state == State.PAUSE_RECORDING:
            logger.info('Record resume')
            self.btpauserecord.setText(self._tr('暂停录制', 'Pause Record', '暫停錄製'))
            self.update_state(State.RECORDING)
        elif self.state == State.RECORDING:
            logger.info('Record pause')
            self.btpauserecord.setText(self._tr('继续录制', 'Continue', '繼續錄製'))
            self.tnumrd.setText(self._tr('录制已暂停', 'Recording paused', '錄製已暫停'))
            self.update_state(State.PAUSE_RECORDING)

    def OnPauseRecordButton(self):
        self.pauseRecordMethod()

    def OnBtOpenScriptFilesButton(self):
        scripts_dir = to_abs_path('scripts')
        if os.path.exists(scripts_dir):
            os.startfile(scripts_dir)
        else:
            QMessageBox.warning(self, self._tr('提示', 'Tip', '提示'), self._tr('脚本目录不存在', 'Script directory does not exist', '腳本目錄不存在'))
        # 重新设置的为点击按钮时, 所处的位置
        self.choice_script.clear()
        self.choice_script.addItems(scripts)
        self.choice_script.setCurrentIndex(scripts_map['current_index'])

    def OnBtEditFileButton(self):
        script_path = self.get_script_path()
        if not script_path or not os.path.exists(script_path):
            QMessageBox.warning(self, self._tr('警告', 'Warning', '警告'), self._tr('请先选择一个脚本文件。', 'Please select a script file first.', '請先選擇一個腳本檔案。'))
            return
        from ScriptEditor import ScriptEditor
        editor = ScriptEditor(script_path, self)
        editor.exec_()

    def OnBtRenameFileButton(self):
        script_path = self.get_script_path()
        if not script_path or not os.path.exists(script_path):
            QMessageBox.warning(self, self._tr('警告', 'Warning', '警告'), self._tr('请先选择一个脚本文件。', 'Please select a script file first.', '請先選擇一個腳本檔案。'))
            return
        old_name = os.path.basename(script_path)
        # Remove extension for display
        base_name = old_name
        if old_name.endswith('.json5'):
            base_name = old_name[:-6]
        elif old_name.endswith('.txt'):
            base_name = old_name[:-4]
        
        new_name, ok = QInputDialog.getText(self, self._tr('重命名', 'Rename', '重新命名'), self._tr('新名称：', 'New name:', '新名稱：'), text=base_name)
        if ok and new_name and new_name != base_name:
            # Add back extension
            if old_name.endswith('.json5'):
                new_name = new_name + '.json5'
            elif old_name.endswith('.txt'):
                new_name = new_name + '.txt'
            dir_path = os.path.dirname(script_path)
            new_path = os.path.join(dir_path, new_name)
            if os.path.exists(new_path):
                QMessageBox.warning(self, self._tr('警告', 'Warning', '警告'), self._tr('该名称的文件已存在。', 'A file with this name already exists.', '該名稱的檔案已存在。'))
                return
            os.rename(script_path, new_path)
            get_script_list_from_dir()
            update_script_map()
            self.choice_script.clear()
            self.choice_script.addItems(self.scripts)
            self.choice_script.setCurrentText(new_name)
            self.config.setValue("Config/Script", new_name)
            logger.info(f'Renamed script: {old_name} -> {new_name}')

    def OnBtClearFilesButton(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self._tr('确认', 'Confirm', '確認'))
        msg_box.setText(self._tr('是否删除所有脚本？', 'Delete all scripts?', '是否刪除所有腳本？'))
        msg_box.setIcon(QMessageBox.Question)
        yes_btn = msg_box.addButton(self._tr('是', 'Yes', '是'), QMessageBox.YesRole)
        no_btn = msg_box.addButton(self._tr('否', 'No', '否'), QMessageBox.NoRole)
        msg_box.setDefaultButton(no_btn)
        msg_box.exec_()
        reply = msg_box.clickedButton() == yes_btn
        if reply:
            script_dir = get_script_dir()
            if not os.path.exists(script_dir):
                QMessageBox.information(self, self._tr('信息', 'Info', '資訊'), self._tr('脚本文件夹不存在，无需清除。', 'Script folder does not exist, nothing to clear.', '腳本文件夾不存在，無需清除。'))
                return
            count = 0
            for f in os.listdir(script_dir):
                if f.endswith('.json5') or f.endswith('.json'):
                    os.remove(os.path.join(script_dir, f))
                    count += 1
            get_script_list_from_dir()
            update_script_map()
            self.scripts = scripts
            self.choice_script.clear()
            self.choice_script.addItems(self.scripts)
            if self.scripts:
                self.choice_script.setCurrentIndex(0)
                self.config.setValue("Config/Script", self.scripts[0])
                self.btrun.setEnabled(True)
            else:
                self.config.setValue("Config/Script", '')
                self.btrun.setEnabled(False)
            QMessageBox.information(self, self._tr('完成', 'Done', '完成'), self._tr(f'已删除 {count} 个脚本。', f'Deleted {count} scripts.', f'已刪除 {count} 個腳本。'))
            logger.info(f'Deleted {count} scripts')

    def recordMethod(self):
        if self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
            logger.info('Record stop')
            with open(self.new_script_path(), 'w', encoding='utf-8') as f:
                json5.dump({"scripts": self.record}, indent=2, ensure_ascii=False, fp=f)
            self.btrecord.setText(self._tr('开始录制', 'Record', '開始錄製'))
            self.tnumrd.setText(self._tr('完成录制', 'Record Finished', '完成錄製'))
            self.record = []
            self.actioncount = 0
            self.choice_script.setCurrentIndex(0)
            self.btpauserecord.setText(self._tr('暂停录制', 'Pause Record', '暫停錄製'))
            self.update_state(State.IDLE)
        elif self.state == State.IDLE:
            logger.info('Record start')
            self.textlog.clear()
            status = self.tnumrd.text()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.setText(self._tr('完成录制', 'Finish Recording', '完成錄製'))
            self.tnumrd.setText(self._tr('已录制 0 个动作', '0 actions recorded', '已錄製 0 個動作'))
            self.record = []
            self.update_state(State.RECORDING)

    def OnBtrecordButton(self):
        if self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
            self.record = self.record[:-2]
        self.recordMethod()

    def OnBtrunButton(self):
        logger.info('Script start')
        self.textlog.clear()
        self.update_state(State.RUNNING)
        if self.runthread:
            self.updateStateSignal.disconnect()
        self.runthread = RunScriptClass(self)
        self.runthread.start()

    def OnBtStopButton(self):
        if self.state == State.RUNNING or self.state == State.PAUSE_RUNNING:
            # 停止脚本执行
            logger.info('Script stop via stop button')
            self.tnumrd.setText(self._tr('已终止', 'Stopped', '已終止'))
            if self.runthread:
                self.runthread.resume()
            self.update_state(State.IDLE)
        elif self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
            # 录制中点击停止，弹窗提示是否放弃录制
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(self._tr('确认', 'Confirm', '確認'))
            msg_box.setText(self._tr('是否放弃本次录制？', 'Abandon current recording?', '是否放棄本次錄製？'))
            msg_box.setInformativeText(self._tr('点击确认将不保存本次录制的脚本。', 'Clicking confirm will not save the recorded script.', '點擊確認將不保存本次錄製的腳本。'))
            msg_box.setIcon(QMessageBox.Question)
            confirm_btn = msg_box.addButton(self._tr('确认', 'Confirm', '確認'), QMessageBox.YesRole)
            cancel_btn = msg_box.addButton(self._tr('取消', 'Cancel', '取消'), QMessageBox.NoRole)
            msg_box.setDefaultButton(cancel_btn)
            msg_box.exec_()
            if msg_box.clickedButton() == confirm_btn:
                # 放弃录制，不保存
                logger.info('Recording abandoned via stop button')
                self.record = []
                self.actioncount = 0
                self.btrecord.setText(self._tr('开始录制', 'Record', '開始錄製'))
                self.btpauserecord.setText(self._tr('暂停录制', 'Pause Record', '暫停錄製'))
                self.tnumrd.setText(self._tr('已取消录制', 'Recording cancelled', '已取消錄製'))
                self.update_state(State.IDLE)
            else:
                # 取消，继续录制
                logger.info('Continue recording after stop button cancel')

    def update_state(self, state):
        self.state = state
        if state != State.SETTING_HOT_KEYS and state != State.RECORDING and state != State.PAUSE_RECORDING:
            self.updateStateSignal.emit(self.state)
        if state == State.IDLE:
            self.hotkey_start.setEnabled(True)
            self.hotkey_stop.setEnabled(True)
            self.hotkey_record.setEnabled(True)
            self.btrun.setEnabled(True if self.scripts else False)
            self.btrecord.setEnabled(True)
            self.btpauserecord.setEnabled(False)
            self.btstop.setEnabled(False)
        elif state == State.SETTING_HOT_KEYS:
            # Only disable hotkey display buttons, keep change buttons enabled
            self.hotkey_start.setEnabled(False)
            self.hotkey_stop.setEnabled(False)
            self.hotkey_record.setEnabled(False)
            self.btrun.setEnabled(False)
            self.btrecord.setEnabled(False)
            self.btpauserecord.setEnabled(False)
            self.btstop.setEnabled(False)
        elif state == State.RUNNING or state == State.PAUSE_RUNNING:
            self.hotkey_start.setEnabled(False)
            self.hotkey_stop.setEnabled(False)
            self.hotkey_record.setEnabled(False)
            self.btrun.setEnabled(False)
            self.btrecord.setEnabled(False)
            self.btpauserecord.setEnabled(False)
            self.btstop.setEnabled(True)
        elif state == State.RECORDING or state == State.PAUSE_RECORDING:
            self.hotkey_start.setEnabled(False)
            self.hotkey_stop.setEnabled(False)
            self.hotkey_record.setEnabled(False)
            self.btrun.setEnabled(False)
            self.btrecord.setEnabled(True)
            self.btpauserecord.setEnabled(True)
            self.btstop.setEnabled(True)

    def OnHotkeyButton(self, btn_obj: QObject):
        logger.debug(f'OnHotkeyButton called for {btn_obj.objectName()}, current text: {btn_obj.text()}')
        self.hotkey_set_btn = btn_obj
        btn_obj.setText('')
        self.keys_pool.clear()
        self.update_state(State.SETTING_HOT_KEYS)

    def _format_hotkey_display(self, key):
        if not key:
            return key
        import re
        return re.sub(r'\bf(\d+)\b', lambda m: f'F{m.group(1)}', str(key), flags=re.IGNORECASE)

    def OnBtDefaultHotkey(self):
        self.hotkey_start.setText('F6')
        self.hotkey_stop.setText('F9')
        self.hotkey_record.setText('F10')
        self.onconfigchange()
        logger.info('Hotkeys reset to defaults')

    def OnPreRandomChanged(self, state):
        is_random = state == Qt.Checked
        # Don't disable any controls, just toggle visual hint
        self.pre_random_tilde.setEnabled(is_random)

    def OnPostRandomChanged(self, state):
        is_random = state == Qt.Checked
        # Don't disable any controls, just toggle visual hint
        self.post_random_tilde.setEnabled(is_random)

    @Slot(bool)
    def handle_runscript_status(self, succeed):
        self.update_state(State.IDLE)

    @Slot(tuple)
    def cursor_pos_change(self, pos):
        prefix = getattr(self, 'cursor_pos_prefix', 'Mouse Position')
        self.label_cursor_pos.setText(f'{prefix}: {pos}')
