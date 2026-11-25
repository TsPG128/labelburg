"""Label printers on TSPL (protocol.py): the Nelko PM220, sold as the P20, a
direct thermal printer for die-cut labels with a 48 mm printhead, on USB or on
the network, e.g. behind p910nd. No cutter, the labels are torn off. The label
is sent as an image, so that it prints as the label designer shows it. The
printer is asked for its status with <ESC>!?: errors, not the labels in it.

Only 50 x 30 mm labels were calibrated, on a real printer: the printhead
reaches 48 of their 50 mm and starts 3.6 mm below their top, as the offsets
below say. The other sizes were made from those, their rolls were not tried."""

import logging
import re

from PIL import Image

from .. import bitmap, devices, progress
from ..base import Driver, network_status, shown
from ..labels import FormFactor, Label
from . import protocol

logger = logging.getLogger(__name__)

MODELS = ('Nelko/PM220',)
DOTS_PER_MM = 8
# The printhead has 384 dots, 48 mm, the labels start at its left: a 50 mm
# label loses 2 mm at its right
HEAD = 384
# Measured with a photo of a printed 50 x 30 mm label: the first 29 dots of a
# label, 3.6 mm, are fed before the printhead prints, the labels are 240 dots
# long and print their last ones short of their end. The image is placed at
# the first dot the printer prints, with the same margin left and right of it
# and at the bottom as of the labels labelprint printed well.
FEED_LOST = 29
MARGIN_X = 2 * DOTS_PER_MM
MARGIN_TOP = 1
MARGIN_BOTTOM = 10
# What the job asks of the printer, as labelprint did
DENSITY = 10
SPEED = 4
GAP = 2
DIRECTION = 1
# No figures of the maker: mm/s and the seconds a label takes besides. Measured
# on a PM220: a 50 x 30 mm label sent to the printer took 2.4 s until it told it
# waits again, 1.6 s of them it told it prints.
PRINT_SPEED = 25
BESIDES = 1.2
# Width x length in mm, whether the roll was tried
SIZES = {(50, 30): True, (40, 30): False, (40, 20): False}


def _label(width: int, length: int) -> Label:
    total = (width * DOTS_PER_MM, length * DOTS_PER_MM)
    # The same margin at the right, but where the printhead ends first
    right = min(total[0] - MARGIN_X, HEAD)
    printable = (right - MARGIN_X, total[1] - FEED_LOST - MARGIN_TOP - MARGIN_BOTTOM)
    return Label(f'tspl{width}x{length}', (width, length), FormFactor.DIE_CUT, total, printable, 0,
                 models=MODELS)


LABELS = tuple(_label(width, length) for width, length in SIZES)
NAMES = {label.identifier: f'{label.tape_size[0]} x {label.tape_size[1]} mm die-cut (Nelko)'
         + ('' if SIZES[label.tape_size] else ', not calibrated') for label in LABELS}


def label_rows(label, label_size: str) -> tuple[Image.Image, list[bytes], int]:
    """A label as the printer prints it: rows of packed dots across the
    printhead, the first one comes out first, and the bytes of each row."""
    img = label.generate()
    # Turned across the printhead: rotated labels, and labels longer than
    # wide, which the label designer draws lying
    across = next(size.dots_printable[0] for size in LABELS if size.identifier == label_size)
    if img.width != across:
        img = img.rotate(90, expand=True)
    img = bitmap.black_and_white(img, label)
    rows, width = bitmap.packed_rows(img)
    return img, rows, width


class Tspl(Driver):
    vendor = 'Nelko'
    models = MODELS
    labels = LABELS
    label_names = NAMES
    # usblp's device, also a name a udev rule gives it, or the printer on the
    # network on the port of raw printing only, as the other drivers
    device_patterns = (re.compile(r'(file://)?/dev/usb/lp\w+'),
                       re.compile(r'usb://0x[0-9a-fA-F]{4}:0x[0-9a-fA-F]{4}(/[A-Za-z0-9_-]+)?'),
                       re.compile(r'tcp://[A-Za-z0-9.-]+(:9100)?'),
                       re.compile(r'tcp://\[[0-9A-Fa-f:.]+\](:9100)?'))
    reports_tape = False

    def fits(self, label, model):
        return label in LABELS

    def dpi(self, high_res):
        return protocol.DPI

    def resolution_problem(self, model, high_res):
        return f'The {shown(model)} printer cannot print at 600 dpi, turn off 600 dpi printing' if high_res else ''

    def capabilities(self, model):
        # The labels are torn off, their top leaves it first
        return dict(super().capabilities(model), qualities=['quality'], cutter=False, leaves_turned=True)

    def status(self, device, model, unconfirmed=False):
        return self.noted_status(device, lambda: self._status(device, model))

    def _status(self, device, model):
        state = dict(network_status(device, model), media_type='Die-cut labels', phase_type='Waiting to receive')
        with devices.device_lock(device, timeout=progress.status_wait(device)) as acquired:
            if not acquired:
                return devices.busy_state(device, state)
            answer = protocol.status_byte(device)
        if answer is None:
            raise TimeoutError('The printer does not answer')
        state['errors'] = protocol.errors(answer)
        state['status_type'] = devices.status_type(state['errors'])
        if answer & protocol.PRINTING:
            state['phase_type'] = 'Printing state'
        devices.status_cache[devices.lock_key(device)] = state
        return state

    def feed_kind(self, model, label_size):
        return ''

    def print_speed(self, model, fast, red):
        return PRINT_SPEED, BESIDES

    def label_lengths(self, job):
        # Each label of the job tells its rows in BITMAP
        return [int(label.split(b'BITMAP ', 1)[1].split(b',', 5)[3]) / DOTS_PER_MM for label in job if b'BITMAP ' in label]

    def render(self, queue, entries, keep=None):
        size = next(label.tape_size for label in LABELS if label.identifier == queue.label_size)
        job = []
        for i, entry in enumerate(entries):
            img, rows, width = label_rows(entry['label'], queue.label_size)
            if keep:
                keep(img, f'tspl_{i}')
            job.append(protocol.label(rows, width, size, (MARGIN_X, MARGIN_TOP), density=DENSITY,
                                      speed=SPEED, gap=GAP, direction=DIRECTION))
        return job

    def send(self, queue, job) -> str:
        device = queue.device_specifier
        try:
            protocol.write(device, b''.join(job))
        except OSError as e:
            logger.warning('Printing on %s failed: %s', device, e)
            return devices.not_sent(e)
        return ''


DRIVER = Tspl()
