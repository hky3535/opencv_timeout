import cv2
import threading
import time

def capture(source, timeout): # capture with timeout (s)

    class CaptureTimeout(threading.Thread):
        def __init__(self, _source):
            super(CaptureTimeout, self).__init__()
            self._source = _source
            self._stream = False
            
        def run(self):
            self._stream = self._capture_timeout()

        def _capture_timeout(self):
            _stream = cv2.VideoCapture(self._source)
            if _stream.isOpened():
                return _stream
            else:
                _stream.release()
                return False

    capture_timeout_thread = CaptureTimeout(source)
    capture_timeout_thread.daemon = True
    capture_timeout_thread.start()
    capture_timeout_thread.join(timeout)
    return capture_timeout_thread._stream

def read(capture, timeout, event): # read with timeout (s) if event is True --> return frame; if False --> return False

    class ReadTimeout(threading.Thread):
        def __init__(self, _capture):
            super(ReadTimeout, self).__init__()
            self._capture = _capture
            self._frame = False, False
            
        def run(self):
            self._frame = self._read_timeout()

        def _read_timeout(self):
            grab_ret = self._capture.grab()
            if not grab_ret: # 检查帧失败
                return False, False

            retrieve_ret, frame = self._capture.retrieve()
            if not retrieve_ret or frame is None: # 获取帧失败
                return False, False
            
            return True, frame

    read_timeout_thread = ReadTimeout(capture)
    read_timeout_thread.daemon = True
    read_timeout_thread.start()
    read_timeout_thread.join(timeout)
    return read_timeout_thread._frame

stream = capture("rtsp://...", 5)
while True:
    frame = read(stream, 1)
    cv2.imshow("", frame)
    cv2.waitKey(1)