import os
import sys
import math
import shutil
import tempfile
from PySide6.QtWidgets import QApplication, QWidget, QSpinBox
from PySide6.QtCore import Qt, Slot, QRect

import argparse
from loguru import logger


def get_working_dir():
    work_dir = os.path.join(get_documents_dir(), 'AKA-Yomi')
    old_work_dir = os.path.join(tempfile.gettempdir(), 'KeymouseGo')
    os.makedirs(work_dir, exist_ok=True)
    for subdir in ['scripts', 'logs', 'plugins']:
        subdir_path = os.path.join(work_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
    migrate_old_working_dir(old_work_dir, work_dir)
    return work_dir


def get_documents_dir():
    try:
        import ctypes
        import uuid
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [
                ('Data1', ctypes.c_ulong),
                ('Data2', ctypes.c_ushort),
                ('Data3', ctypes.c_ushort),
                ('Data4', ctypes.c_ubyte * 8),
            ]

        documents_guid = uuid.UUID('{FDD39AD0-238F-46AF-ADB4-6C85480369C7}')
        fid_documents = GUID.from_buffer_copy(documents_guid.bytes_le)
        path_ptr = wintypes.LPWSTR()
        ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(fid_documents), 0, None, ctypes.byref(path_ptr))
        documents_dir = path_ptr.value
        ctypes.windll.ole32.CoTaskMemFree(path_ptr)
        if documents_dir:
            return documents_dir
    except Exception:
        pass
    return os.path.join(os.path.expanduser('~'), 'Documents')


def migrate_old_working_dir(old_work_dir, new_work_dir):
    if not os.path.isdir(old_work_dir):
        return
    for name in ['config.ini', 'scripts', 'logs', 'plugins']:
        old_path = os.path.join(old_work_dir, name)
        new_path = os.path.join(new_work_dir, name)
        if not os.path.exists(old_path):
            continue
        if os.path.isdir(new_path) and os.listdir(new_path):
            continue
        if os.path.isfile(new_path):
            continue
        try:
            if os.path.isdir(old_path):
                shutil.copytree(old_path, new_path, dirs_exist_ok=True)
            else:
                shutil.copy2(old_path, new_path)
        except Exception as e:
            logger.warning(f'Failed to migrate {old_path} to {new_path}: {e}')


def get_resource_dir():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def to_abs_path(*args):
    if args and args[0] in ('assets', 'Mondrian.ico', 'Mondrian.png', 'assets.qrc', 'assets_rc.py'):
        return os.path.join(get_resource_dir(), *args)
    return os.path.join(get_working_dir(), *args)


import UIFunc
import Recorder
from Event import ScriptEvent
from Plugin.Manager import PluginManager
from Util.RunScriptClass import RunScriptCMDClass, StopFlag


def resize_layout(ui, ratio_w, ratio_h):
    ui.resize(ui.width() * ratio_w, ui.height() * ratio_h)

    for q_widget in ui.findChildren(QWidget):
        q_widget.setGeometry(QRect(q_widget.x() * ratio_w,
                                   q_widget.y() * ratio_h,
                                   q_widget.width() * ratio_w,
                                   q_widget.height() * ratio_h))
        q_widget.setStyleSheet('font-size: ' + str(
                                math.ceil(9 * min(ratio_h, ratio_w))) + 'px')
        if isinstance(q_widget, QSpinBox):
            q_widget.setStyleSheet('padding-left: 7px')


def main():

    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    ui = UIFunc.UIFunc(app)

    # Set application icon
    from PySide6.QtGui import QIcon
    icon_path = to_abs_path('assets', 'Mondrian.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        ui.setWindowIcon(QIcon(icon_path))

    ui.setFixedSize(ui.width(), ui.height())
    ui.show()
    sys.exit(app.exec())


@logger.catch
def single_run(script_path, run_times):
    flag = StopFlag(False)
    thread = RunScriptCMDClass(script_path, run_times, flag)

    stop_name = 'f9'

    @Slot(ScriptEvent)
    def on_keyboard_event(event):
        key_name = event.action[1].lower()
        if key_name == stop_name:
            logger.debug('break exit!')
            flag.value = True
            thread.resume()
        return True

    Recorder.setuphook(commandline=True)
    Recorder.set_callback(on_keyboard_event)

    PluginManager.reload()
    eventloop = QApplication()

    thread.finished.connect(eventloop.exit)
    thread.start()

    sys.exit(eventloop.exec_())


if __name__ == '__main__':
    logger.debug(sys.argv)
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('scripts',
                            help='Path for the scripts',
                            type=str,
                            nargs='+'
                            )
        parser.add_argument('-rt', '--runtimes',
                            help='Run times for the script',
                            type=int,
                            default=1
                            )
        args = vars(parser.parse_args())
        logger.debug(args)
        single_run(args['scripts'],
                   run_times=args['runtimes']
                   )
    else:
        main()
