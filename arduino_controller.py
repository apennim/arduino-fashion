from serial import Serial, SerialException
import time
import threading
import logging
from typing import Optional, Callable
import queue

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArduinoController:
    def __init__(self, port: str = 'COM3', baudrate: int = 9600):
        """
        初始化 Arduino 控制器
        
        Args:
            port: 串口名稱，Windows 通常是 'COM3'，Linux 通常是 '/dev/ttyUSB0'
            baudrate: 串口速率，需要與 Arduino 程式碼匹配
        """
        self.port = port
        self.baudrate = baudrate
        self.serial: Optional[Serial] = None
        self.is_connected = False
        self.running = False
        self.receive_thread: Optional[threading.Thread] = None
        self.command_queue = queue.Queue()
        
        # 回調函數
        self.style_callback: Optional[Callable[[int], None]] = None
        self.confirm_callback: Optional[Callable[[], None]] = None
        self.connection_callback: Optional[Callable[[bool], None]] = None

        # 重試參數
        self.max_retries = 3
        self.retry_delay = 1.0  # 秒
        self.command_timeout = 2.0  # 命令超時時間
        self.auto_reconnect = True
        self.reconnect_interval = 5.0  # 自動重連間隔

    def connect(self) -> bool:
        """
        連接到 Arduino 設備
        
        Returns:
            bool: 連接是否成功
        """
        if self.is_connected:
            return True

        for attempt in range(self.max_retries):
            try:
                self.serial = Serial(self.port, self.baudrate, timeout=1)
                self.is_connected = True
                self.running = True
                
                # 啟動接收線程
                self.receive_thread = threading.Thread(target=self._receive_data)
                self.receive_thread.daemon = True
                self.receive_thread.start()
                
                # 啟動命令處理線程
                self.command_thread = threading.Thread(target=self._process_commands)
                self.command_thread.daemon = True
                self.command_thread.start()
                
                # 啟動監控線程
                self.monitor_thread = threading.Thread(target=self._monitor_connection)
                self.monitor_thread.daemon = True
                self.monitor_thread.start()
                
                logger.info(f"已連接到 Arduino ({self.port})")
                if self.connection_callback:
                    self.connection_callback(True)
                return True
                
            except SerialException as e:
                logger.error(f"連接嘗試 {attempt + 1} 失敗: {str(e)}")
                time.sleep(self.retry_delay)
        
        logger.error(f"無法連接到 Arduino，已重試 {self.max_retries} 次")
        if self.connection_callback:
            self.connection_callback(False)
        return False

    def _monitor_connection(self) -> None:
        """監控連接狀態並自動重連"""
        while self.running:
            if self.auto_reconnect and not self.is_connected:
                logger.info("嘗試重新連接...")
                if self.connect():
                    logger.info("重新連接成功")
                else:
                    logger.error("重新連接失敗")
                    time.sleep(self.reconnect_interval)
            time.sleep(1.0)

    def disconnect(self) -> None:
        """安全斷開與 Arduino 的連接"""
        self.running = False
        if self.serial and self.serial.is_open:
            try:
                self.serial.close()
            except Exception as e:
                logger.error(f"關閉串口時發生錯誤: {str(e)}")
        self.is_connected = False
        if self.connection_callback:
            self.connection_callback(False)
        logger.info("已斷開 Arduino 連接")

    def _receive_data(self) -> None:
        """接收來自 Arduino 的數據"""
        while self.running:
            if not self.serial or not self.serial.is_open:
                self._handle_disconnection()
                time.sleep(0.1)
                continue

            try:
                if self.serial.in_waiting:
                    data = self.serial.readline().decode('utf-8').strip()
                    self._process_data(data)
            except SerialException as e:
                logger.error(f"串口錯誤: {str(e)}")
                self._handle_disconnection()
            except Exception as e:
                logger.error(f"讀取數據時發生錯誤: {str(e)}")
                time.sleep(0.1)

    def _handle_disconnection(self) -> None:
        """處理設備斷線"""
        if self.is_connected:
            self.is_connected = False
            logger.warning("Arduino 連接已斷開")
            if self.connection_callback:
                self.connection_callback(False)

    def _process_commands(self) -> None:
        """處理發送命令的佇列"""
        while self.running:
            try:
                command = self.command_queue.get(timeout=1.0)
                start_time = time.time()
                
                while time.time() - start_time < self.command_timeout:
                    if self.serial and self.serial.is_open:
                        self.serial.write(command.encode('utf-8'))
                        self.serial.flush()
                        break
                    time.sleep(0.1)
                else:
                    logger.warning(f"命令發送超時: {command.strip()}")
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"發送命令時發生錯誤: {str(e)}")
            finally:
                if not self.command_queue.empty():
                    self.command_queue.task_done()

    def set_confidence(self, confidence: float) -> None:
        """
        設置信心度 LED
        
        Args:
            confidence: 0-100 之間的信心度值
        """
        if not self.is_connected:
            logger.warning("Arduino 未連接，無法設置信心度")
            return

        try:
            confidence = max(0, min(100, float(confidence)))
            self.command_queue.put(f"CONF:{int(confidence)}\n")
        except Exception as e:
            logger.error(f"設置信心度時發生錯誤: {str(e)}")

    def set_status(self, is_busy: bool) -> None:
        """
        設置狀態 LED
        
        Args:
            is_busy: True 表示忙碌，False 表示就緒
        """
        if not self.is_connected:
            logger.warning("Arduino 未連接，無法設置狀態")
            return

        try:
            status = "BUSY\n" if is_busy else "READY\n"
            self.command_queue.put(status)
        except Exception as e:
            logger.error(f"設置狀態時發生錯誤: {str(e)}")

    def register_callbacks(self, 
                         style_cb: Optional[Callable[[int], None]] = None,
                         confirm_cb: Optional[Callable[[], None]] = None,
                         connection_cb: Optional[Callable[[bool], None]] = None) -> None:
        """
        註冊回調函數
        
        Args:
            style_cb: 風格改變時的回調函數
            confirm_cb: 確認按鈕按下時的回調函數
            connection_cb: 連接狀態改變時的回調函數
        """
        self.style_callback = style_cb
        self.confirm_callback = confirm_cb
        self.connection_callback = connection_cb

    def __enter__(self):
        """支持 with 語句"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持 with 語句"""
        self.disconnect()
