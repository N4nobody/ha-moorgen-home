import asyncio
import logging
from contextlib import suppress

from .protocol.codec import parse_protocol_packet, route

_LOGGER = logging.getLogger(__name__)


class AsyncSocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._reader = None
        self._writer = None
        self._lock = asyncio.Lock()
        self._connected = False
        self._connect_task = None
        self._stopped = False
        self._connected_event = asyncio.Event()
        self._scene_event = asyncio.Event()
        self._scene_version = 0
        self.data = {"scenes": [], "rooms": [], "devices": []}

    @property
    def scene_version(self):
        return self._scene_version

    async def start(self):
        if self._connect_task and not self._connect_task.done():
            return
        self._stopped = False
        self._connect_task = asyncio.create_task(self._connect_loop())

    async def stop(self):
        self._stopped = True
        self._connected = False
        self._connected_event.clear()

        if self._connect_task:
            self._connect_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._connect_task
            self._connect_task = None

        await self._close_writer()

    async def wait_until_connected(self, timeout=5):
        await asyncio.wait_for(self._connected_event.wait(), timeout=timeout)

    async def wait_for_scene_update(self, previous_version: int, timeout=5):
        if self._scene_version > previous_version:
            return

        self._scene_event.clear()
        if self._scene_version > previous_version:
            return

        await asyncio.wait_for(self._scene_event.wait(), timeout=timeout)

    async def _connect_loop(self):
        while not self._stopped:
            try:
                await self._connect_once()
            except asyncio.CancelledError:
                raise
            except Exception as err:
                _LOGGER.warning("[Connection error] %s", err)
            finally:
                self._connected = False
                self._connected_event.clear()
                await self._close_writer()

            if self._stopped:
                break

            _LOGGER.info("Connection lost, retrying in 2 seconds...")
            await asyncio.sleep(2)

    async def _connect_once(self):
        _LOGGER.info(f"Connecting to {self.host}:{self.port}")
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        self._connected = True
        self._connected_event.set()
        _LOGGER.info("Connected to server")
        await self._read_loop()

    async def _close_writer(self):
        if self._writer is None:
            return

        writer = self._writer
        self._writer = None
        self._reader = None

        writer.close()
        with suppress(Exception):
            await writer.wait_closed()
        _LOGGER.info("Connection closed")

    async def _read_loop(self):
        buf = b""
        while not self._stopped:
            data = await self._reader.read(4096)
            if not data:
                raise ConnectionError("Server closed the connection")

            buf += data
            while len(buf) > 3:
                pkt_len = buf[1] + (buf[2] << 8)
                full_len = pkt_len + 3
                if len(buf) < full_len:
                    break

                pkt = buf[:full_len]
                buf = buf[full_len:]

                try:
                    data_packet = parse_protocol_packet(pkt)
                    updated = route(data_packet, self.data)
                    if updated == "scenes":
                        self._scene_version += 1
                        self._scene_event.set()
                except Exception as err:
                    _LOGGER.warning("[Packet handling error] %s", err)

    async def send_command(self, data: bytes):
        """Send raw bytes to the server."""
        async with self._lock:
            if not self._connected or not self._writer:
                raise ConnectionError("Not connected, cannot send data")
            self._writer.write(data)
            await self._writer.drain()
            _LOGGER.info(f"[TX] Sent: {data.hex()}")
