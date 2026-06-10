import random
import threading
import time
import traceback
from dataclasses import dataclass
from typing import List

from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition, QDeadlineTimer, Qt, Slot
from PySide6.QtWidgets import QWidget
from loguru import logger

from Util.Global import State
from Event import ScriptEvent
from Plugin.Manager import PluginManager
from Util.Parser import LegacyParser, ScriptParser, JsonObject

mutex = QMutex()
cond = QWaitCondition()


class RunScriptMeta:
    def pause(self):
        mutex.lock()
        cond.wait(mutex)
        mutex.unlock()

    def sleep(self, msecs: int):
        mutex.lock()
        cond.wait(mutex, QDeadlineTimer(int(msecs)))
        mutex.unlock()

    def resume(self):
        mutex.lock()
        cond.wakeAll()
        mutex.unlock()


class RunScriptClass(QThread, RunScriptMeta):
    logSignal: Signal = Signal(str)
    tnumrdSignal: Signal = Signal(str)
    btnSignal: Signal = Signal(bool)
    statusSignal: Signal = Signal(bool)

    # 国际化文本映射
    I18N = {
        '简体中文': {
            'script_not_found': '未找到脚本，请先录制！',
            'running': '运行中',
            'looptimes': '循环次数',
            'finished': '执行完成',
            'pre_delay': '运行前延迟',
            'post_delay': '运行后延迟',
            'delay_countdown': '倒计时',
            'parse_error': '解析脚本时发生错误',
            'runtime_error': '执行时发生错误',
            'run_failed': '脚本运行失败，请检查日志文件',
            'call_error': '调用时发生错误，请检查日志文件',
        },
        'English': {
            'script_not_found': 'Script not found, please record first!',
            'running': 'Running',
            'looptimes': 'Looptimes',
            'finished': 'Finished',
            'pre_delay': 'Pre-run delay',
            'post_delay': 'Post-run delay',
            'delay_countdown': 'Countdown',
            'parse_error': 'An error occurred while parsing script',
            'runtime_error': 'An error occurred during runtime',
            'run_failed': 'Script run failed, please check your log file',
            'call_error': 'An error occurred while calling, please check log file',
        },
        '繁體中文': {
            'script_not_found': '未找到腳本，請先錄製！',
            'running': '執行中',
            'looptimes': '循環次數',
            'finished': '執行完成',
            'pre_delay': '執行前延遲',
            'post_delay': '執行後延遲',
            'delay_countdown': '倒數計時',
            'parse_error': '解析腳本時發生錯誤',
            'runtime_error': '執行時發生錯誤',
            'run_failed': '腳本執行失敗，請檢查日誌檔案',
            'call_error': '呼叫時發生錯誤，請檢查日誌檔案',
        },
    }

    def __init__(self, frame: QWidget):
        super().__init__()
        logger.debug('Thread created at thread' + str(threading.currentThread()))
        self.eventPause = False
        self.state = State.RUNNING
        self.script_path = frame.get_script_path()
        self.runtimes = frame.stimes.value()
        self.lang = getattr(frame, 'choice_language', None)
        self.lang = self.lang.currentText() if self.lang else '简体中文'

        # 读取延迟配置
        self.pre_delay = frame.pre_delay_spin.value() * 1000  # 转换为毫秒
        self.post_delay = frame.post_delay_spin.value() * 1000
        self.pre_random = frame.pre_random_chk.isChecked()
        self.post_random = frame.post_random_chk.isChecked()
        self.pre_random_min = frame.pre_random_min.value() * 1000
        self.pre_random_max = frame.pre_random_max.value() * 1000
        self.post_random_min = frame.post_random_min.value() * 1000
        self.post_random_max = frame.post_random_max.value() * 1000

        # 更新控件的槽函数
        self.logSignal.connect(frame.textlog.append)
        self.tnumrdSignal.connect(frame.tnumrd.setText)
        self.btnSignal.connect(frame.btrun.setEnabled)
        self.btnSignal.connect(frame.btrecord.setEnabled)
        frame.updateStateSignal.connect(self.update_state, Qt.DirectConnection)
        self.statusSignal.connect(frame.handle_runscript_status)

    def _tr(self, key: str) -> str:
        """根据当前语言获取国际化文本。"""
        return self.I18N.get(self.lang, self.I18N['简体中文']).get(key, key)

    @Slot(str)
    def update_language(self, lang: str):
        """运行过程中同步界面语言。"""
        self.lang = lang

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def sleep_with_countdown(self, msecs: int, prefix_key: str):
        """带倒计时显示的 sleep，每 100ms 更新一次状态文本。"""
        remaining = msecs
        interval = 100  # 每 100ms 更新一次
        while remaining > 0 and self.state != State.IDLE:
            seconds = remaining / 1000.0
            countdown_text = f'{self._tr(prefix_key)} {self._tr("delay_countdown")}: {seconds:.1f}s'
            self.tnumrdSignal.emit(countdown_text)
            sleep_ms = min(interval, remaining)
            mutex.lock()
            cond.wait(mutex, QDeadlineTimer(int(sleep_ms)))
            mutex.unlock()
            remaining -= sleep_ms

    def _get_delay_ms(self, base_delay: int, is_random: bool, random_min: int, random_max: int) -> int:
        """计算实际延迟时间（毫秒）。"""
        if is_random:
            return random.randint(random_min, random_max)
        return base_delay

    def resume(self):
        self.eventPause = False
        super().resume()

    def set_pause(self):
        self.eventPause = True

    @Slot(State)
    def update_state(self, state):
        self.state = state

    def wait_if_pause(self):
        if self.eventPause:
            self.pause()
        else:
            self.resume()

    def run(self):
        logger.debug('Run script at thread' + str(QThread.currentThread()))

        if not self.script_path:
            self.tnumrdSignal.emit(self._tr('script_not_found'))
            logger.warning('Script not found, please record first!')
            return

        self.btnSignal.emit(False)
        try:
            self.run_script_from_path(self.script_path)
        except Exception as e:
            logger.error(e)
            self.logSignal.emit(self._tr('runtime_error'))
        self.statusSignal.emit(True)

    @logger.catch
    def run_script_from_path(self, script_path: str):
        try:
            script_name = script_path.split('/')[-1].split('\\')[-1]
            self.tnumrdSignal.emit(self._running_text(script_name))
            logger.info('%s running..' % script_name)

            # 解析脚本，返回事件集合与扩展类对象
            logger.debug('Parse script..')
            try:
                head_object = ScriptParser.parse(script_path)
            except Exception as e:
                logger.warning('Failed to parse script, maybe it is using legacy grammar')
                try:
                    head_object = LegacyParser.parse(script_path)
                except Exception as e:
                    logger.error(e)
                    self.logSignal.emit('==============\n' + self._tr('parse_error'))
                    self.logSignal.emit(str(e))
                    self.logSignal.emit('==============')

            j = 0
            nointerrupt = True
            logger.debug('Run script..')

            while (j < self.runtimes or self.runtimes == 0) and nointerrupt:
                logger.debug('===========%d==============' % j)
                if self.state == State.IDLE:
                    break

                # 运行前延迟
                pre_delay_ms = self._get_delay_ms(
                    self.pre_delay, self.pre_random,
                    self.pre_random_min, self.pre_random_max
                )
                if pre_delay_ms > 0:
                    logger.info(f'Pre-run delay: {pre_delay_ms}ms')
                    self.sleep_with_countdown(pre_delay_ms, 'pre_delay')

                looptimes_text = f'{self._tr("looptimes")} [{j + 1}/{self.runtimes}]'
                self.tnumrdSignal.emit(f'{self._running_text(script_name)}... {looptimes_text}')
                nointerrupt = nointerrupt and self.run_script_from_objects(head_object)

                # 运行后延迟
                post_delay_ms = self._get_delay_ms(
                    self.post_delay, self.post_random,
                    self.post_random_min, self.post_random_max
                )
                if post_delay_ms > 0:
                    logger.info(f'Post-run delay: {post_delay_ms}ms')
                    self.sleep_with_countdown(post_delay_ms, 'post_delay')

                j += 1
            if nointerrupt:
                self.tnumrdSignal.emit(self._tr('finished'))
                logger.info('Script run finish')
            else:
                logger.info('Script run interrupted')

        except Exception as e:
            logger.error('Run error: {0}'.format(e))
            traceback.print_exc()
            self.logSignal.emit('==============\n' + self._tr('runtime_error'))
            self.logSignal.emit(str(e))
            self.logSignal.emit('==============')
            self.logSignal.emit(self._tr('run_failed'))
        finally:
            self.btnSignal.emit(True)

    def _running_text(self, script_name: str) -> str:
        return f'{script_name} {self._tr("running")}..'

    # 执行集合中的ScriptEvent
    @logger.catch
    def run_script_from_objects(self, head_object: JsonObject, attach: List[str] = None):
        current_object = head_object
        while current_object is not None:
            self.wait_if_pause()
            if self.state == State.IDLE:
                return False
            if attach:
                try:
                    PluginManager.call_group(attach, current_object)
                except Exception as e:
                    logger.error(e)
                    self.logSignal.emit(self._tr('call_error'))
                    self.logSignal.emit(f'调用{attach}时发生错误，请检查程序日志')
            current_object = self.run_object(current_object)
        return True

    # Only return next object when 'goto' is indicated
    @logger.catch
    def run_object(self, json_object: JsonObject):
        object_type: str = json_object.content.get('type', None)
        call_group: List[str] = json_object.content.get('call', None)
        if call_group:
            PluginManager.call_group(call_group, json_object)
        if object_type == 'event':
            event = ScriptEvent(json_object.content)
            self.logSignal.emit(str(event))
            logger.debug(str(event))
            event.execute(self)
        elif object_type == 'sequence':
            self.run_script_from_objects(json_object.content['events'], json_object.content['attach'])
        elif object_type == 'if':
            result = PluginManager.call(json_object.content['judge'], json_object)
            if result:
                return json_object.next_object
            else:
                return json_object.next_object_if_false
        elif object_type == 'goto' or object_type == 'custom':
            pass
        elif object_type == 'subroutine':
            for path in json_object.content['path']:
                self.run_script_from_path(path)
        else:
            # Not supposed to happen
            logger.error(f'Unexpected event type when running {json_object.content}')
        return json_object.next_object


@dataclass
class StopFlag:
    value: bool


class RunScriptCMDClass(QThread, RunScriptMeta):
    def __init__(self, script_path: str, run_times: int, flag: StopFlag):
        super().__init__()
        self.script_path = script_path
        self.run_times = run_times
        self.flag = flag

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def run(self) -> None:
        self.run_script_from_path(self.script_path)

    @logger.catch
    def run_script_from_path(self, script_path):
        for path in script_path:
            logger.info('Script path:%s' % path)
            logger.debug('Parse script..')
            try:
                head_object = ScriptParser.parse(path)
            except Exception as e:
                logger.warning('Failed to parse script, maybe it is using legacy grammar')
                try:
                    head_object = LegacyParser.parse(path)
                except Exception as e:
                    logger.error(e)
            j = 0
            while j < self.run_times or self.run_times == 0:
                logger.info('===========%d==============' % j)
                self.run_script_from_objects(head_object)
                if self.flag.value:
                    logger.info('Stop Running thread')
                    break
                j += 1
            logger.info('%s run finish' % path)

    @logger.catch
    def run_script_from_objects(self, head_object: JsonObject, attach: List[str] = None):
        current_object = head_object
        while current_object is not None:
            if self.flag.value:
                break
            if attach:
                PluginManager.call_group(attach, current_object)
            current_object = self.run_object(current_object)

    @logger.catch
    def run_object(self, json_object: JsonObject):
        object_type: str = json_object.content.get('type', None)
        call_group: List[str] = json_object.content.get('call', None)
        if call_group:
            PluginManager.call_group(call_group, json_object)
        if object_type == 'event':
            event = ScriptEvent(json_object.content)
            logger.debug(str(event))
            event.execute(self)
        elif object_type == 'sequence':
            self.run_script_from_objects(json_object.content['events'], json_object.content['attach'])
        elif object_type == 'if':
            result = PluginManager.call(json_object.content['judge'], json_object)
            if result:
                return json_object.next_object
            else:
                return json_object.next_object_if_false
        elif object_type in ['goto', 'custom']:
            pass
        elif object_type == 'subroutine':
            self.run_script_from_path(json_object.content['path'])
        else:
            # Not supposed to happen
            logger.error(f'Unexpected event type when running {json_object.content}')
        return json_object.next_object
