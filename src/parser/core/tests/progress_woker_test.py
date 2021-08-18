
import os
import sys
import unittest

root_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(root_path, '..', '..')
sys.path.append(root_path)

from core.progress_woker import ProgressWorker


class ProgressWorkerTests(unittest.TestCase):

    def worker_success_run(self):

        def runner(worker:ProgressWorker):
            
            worker.updateProgress(1)
            worker.updateProgress(2)
            worker.updateProgress(3)


        worker = ProgressWorker(runner)
        worker.start()

        it = worker.progress_yield
        self.assertEqual(it, 1)
        self.assertEqual(it, 2)
        self.assertEqual(it, 3)


if __name__ == '__main__':
    unittest.main()