import asyncio
import logging

from .parse import parse_protocol_packet, route

_LOGGER = logging.getLogger(__name__)


class AsyncSocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._reader = None
        self._writer = None
        self._lock = asyncio.Lock()
        self._connected = False
        self.data = {
            'scenes': [],
            'rooms': [],
            'devices': []
        }

    async def start(self):
        asyncio.create_task(self._connect_loop())

    async def _connect_loop(self):
        while True:
            try:
                await self._connect_once()
            except Exception as e:
                _LOGGER.info(f"[异常] {e}")
            _LOGGER.info("连接断开，2秒后重连...")
            self._connected = False
            await asyncio.sleep(2)

    async def _connect_once(self):
        _LOGGER.info(f"尝试连接 {self.host}:{self.port}")
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        self._connected = True
        _LOGGER.info("连接服务器成功")
        await self._read_loop()
        self._writer.close()
        await self._writer.wait_closed()
        _LOGGER.info("连接关闭")

    async def _read_loop(self):
        buf = b''
        while True:
            data = await self._reader.read(4096)
            if not data:
                raise ConnectionError("服务器已关闭")
            buf += data
            while len(buf) > 3:
                pkt_len = buf[1] + (buf[2] << 8)
                full_len = pkt_len + 3
                if len(buf) < full_len:
                    break
                pkt = buf[:full_len]
                try:
                    data_packet = parse_protocol_packet(pkt)
                except Exception as e:
                    _LOGGER.info(f"[包解析异常] {e}")

                try:
                    route(data_packet, self.data)
                except Exception as e:
                    _LOGGER.info(f"[包路由异常] {e}")

                buf = buf[full_len:]

    async def send_command(self, data: bytes):
        """
        发送指定bytes数据
        """
        # 避免并发冲突
        async with self._lock:
            if not self._connected or not self._writer:
                _LOGGER.info('[发] 当前未连接，无法发送')
                return
            try:
                self._writer.write(data)
                await self._writer.drain()
                _LOGGER.info(f"[发] 发送: {data.hex()}")
            except Exception as e:
                _LOGGER.info(f"[发] 发送失败: {e}")
