"""TSPL of label printers such as the Nelko PM220 (P20), as in the TSPL/TSPL2
programming manual of TSC: the label as one BITMAP, the status byte a printer
tells to <ESC>!? at once. The way labelprint printed labels on a PM220, which
printed them as the label designer shows them."""

import os
import select
import time

from .. import backends, devices, reach, usbip

DPI = 203
# Port of raw printing on the network, and how long connecting may take
PORT = 9100
CONNECT_WAIT = 10
# How long the printer may take to answer <ESC>!?
ANSWER_WAIT = 2
# <ESC>!? is answered with one byte, bits as in ERRORS
STATUS_REQUEST = b'\x1b!?'
# A label goes to a printer on PyUSB in pieces: PyUSB gives up on a single
# write after 15 s
WRITE_CHUNK = 16384
CRLF = b'\r\n'
# The bytes of a 1 bit image packed with 1 printed as TSPL takes them, 0 printed
_INVERTED = bytes(range(255, -1, -1))


def label(rows: list[bytes], width: int, size: tuple[int, int], at: tuple[int, int], *,
          density: int, speed: int, gap: int, direction: int) -> bytes:
    """One label of rows of packed dots, width bytes each, MSB left, 1
    printed, lying at (x, y) dots of a label of the size in mm, which has
    gaps of gap mm between labels."""
    data = b''.join(rows).translate(_INVERTED)
    head = (f'SIZE {size[0]} mm,{size[1]} mm\r\n'
            f'GAP {gap} mm,0 mm\r\n'
            f'DIRECTION {direction}\r\n'
            'REFERENCE 0,0\r\n'
            f'SPEED {speed}\r\n'
            f'DENSITY {density}\r\n'
            'CLS\r\n'
            f'BITMAP {at[0]},{at[1]},{width},{len(rows)},0,').encode()
    return head + data + CRLF + b'PRINT 1' + CRLF


def _usb_write(printer, data: bytes):
    for start in range(0, len(data), WRITE_CHUNK):
        printer.write(data[start:start + WRITE_CHUNK])


def write(device: str, data: bytes):
    """Send to tcp://<host>[:<port>], to usb://<vendor>:<product>[/<serial>]
    through PyUSB, to usbip://<host> shared by another device or to a device
    file, e.g. usblp's."""
    if device.startswith('usb://') or usbip.is_address(device):
        printer = backends.open_printer(device)
        try:
            _usb_write(printer, data)
        finally:
            printer.dispose()
    elif device.startswith('tcp://'):
        with reach.create_connection(devices.tcp_address(device, PORT), timeout=CONNECT_WAIT) as s:
            s.sendall(data)
    else:
        with open(device.removeprefix('file://'), 'wb') as f:
            f.write(data)


def status_byte(device: str) -> int | None:
    """The answer of the printer to <ESC>!?, None if it gave none."""
    if device.startswith('tcp://'):
        with reach.create_connection(devices.tcp_address(device, PORT), timeout=CONNECT_WAIT) as s:
            s.sendall(STATUS_REQUEST)
            s.settimeout(ANSWER_WAIT)
            try:
                answer = s.recv(1)
            except TimeoutError:
                return None
            return answer[0] if answer else None
    if device.startswith('usb://') or usbip.is_address(device):
        printer = backends.open_printer(device)
        try:
            backends.discard(lambda: printer.read(256))
            printer.write(STATUS_REQUEST)
            return _first_byte(lambda left: printer.read(1))
        finally:
            printer.dispose()
    fd = os.open(device.removeprefix('file://'), os.O_RDWR)
    try:
        # An answer from before is not taken for this one
        backends.discard(lambda: select.select([fd], [], [], 0)[0] and os.read(fd, 256))
        os.write(fd, STATUS_REQUEST)

        # usblp also tells empty USB packets
        def read(left):
            return os.read(fd, 1) if select.select([fd], [], [], left)[0] else None
        return _first_byte(read)
    finally:
        os.close(fd)


def _first_byte(read) -> int | None:
    deadline = time.monotonic() + ANSWER_WAIT
    while (left := deadline - time.monotonic()) > 0:
        try:
            part = read(left)
        except OSError:
            return None
        if part is None:
            return None
        if part:
            return part[0]
    return None


# What the bits of the status byte tell, 0 is a printer that waits for a job
ERRORS = ((0x01, 'The printhead is open'),
          (0x02, 'The paper is jammed'),
          (0x04, 'No labels are in the printer'),
          (0x08, 'The ribbon has run out'),
          (0x10, 'The printer is paused'),
          (0x80, 'The printer reports an error'))
PRINTING = 0x20


def errors(status: int) -> list[str]:
    return [text for bit, text in ERRORS if status & bit]
