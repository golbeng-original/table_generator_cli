import threading
import time
import json
import os
from typing import Any

class ProgressWorker(threading.Thread):

    __complete:bool = False
    __progress:int = 0
    __progress_text:str = ''
    __error:Exception = None
    __result = None

    __is_call_progress_yield:bool = False

    __runner = None
    __progress_event = threading.Event()
    __update_prgress_event = threading.Event()

    def __init__(self, runner):
        super().__init__()

        self.__runner = runner

    @property
    def progress(self):
        return self.__progress

    @property
    def progress_text(self):
        return self.__progress_text

    @property
    def error(self):
        return self.__error

    @property
    def result(self):
        return self.__result

    @property
    def progress_yield(self):

        self.__is_call_progress_yield = True

        while self.is_alive():
            self.__progress_event.wait()

            if self.error:
                break

            if self.__complete == True:
                break

            yield (self.progress, self.progress_text)
            
            self.__progress_event.clear()
            self.__update_prgress_event.set()

    def exception(self, error:Exception):
        self.__error = error

    def updateProgress(self, value:int, text:str = ''):

        if self.__is_call_progress_yield:
            self.__update_prgress_event.wait()

        self.__progress = value
        self.__progress_text = text
        self.__progress_event.set()

        if self.__is_call_progress_yield:
            self.__update_prgress_event.clear()

    def run(self):
        try:
            self.__update_prgress_event.set()

            self.__result = self.__runner(self)

            # 마지막 UpdateProgress가 씹힐 수 있다.
            time.sleep(0.01)

            self.__complete = True
        except Exception as e:
            self.exception(e)
        finally:
            self.__progress_event.set()

    def get_progress_conosle_printer(self):
        return ProgressWorkerConsolePrinter(self)

    def get_progress_json_printer(self):
        return ProgressWorkerJsonPrinter(self)

class ProgressWorkerPrinter:

    _progress_worker:ProgressWorker = None

    def __init__(self, progress_worker:ProgressWorker):
        self._progress_worker = progress_worker

    def output(self):
        pass

class ProgressWorkerConsolePrinter(ProgressWorkerPrinter):

    def output(self):
        progress_format = '{0:<3}% [{1:<10}] {2:<20}'

        for progress, progress_text in self._progress_worker.progress_yield:
            progress_ch = '=' * int(progress / 10)

            print(progress_format.format(progress, progress_ch, progress_text), end='\r', flush=True)

        if self._progress_worker.error:
            print('[error] {0:<100}'.format(str(self._progress_worker.error)), flush=True)
        else:
            print('{0:<100}'.format('complete'), flush=True)

class ProgressWorkerJsonPrinter(ProgressWorkerPrinter):

    def output(self):
        for progress, progress_text in self._progress_worker.progress_yield:
            json_info = {
                'state': 'progress',
                'progress': progress,
                'progress_text': progress_text
            }

            print(json.dumps(json_info), flush=True)

        if self._progress_worker.error:
            json_info = {
                'state': 'error',
                'error': str(self._progress_worker.error)
            }

            print(json.dumps(json_info), flush=True)
            return;
