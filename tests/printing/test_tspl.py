"""Label printers on TSPL: the bytes of a label, sent to a device file and over
the network, and printing and status through the label designer."""
import json
import random
import socket
import threading

import pytest
from PIL import Image

from app.labeldesigner.drivers import devices, tspl
from app.labeldesigner.drivers.tspl import protocol
from tests.helpers import make_client, outcome, without_status

DEVICE = 'file:///dev/usb/lp_nelko'
TEXT = json.dumps([{'font': 'DejaVu Sans,Book', 'text': 'OK', 'size': '40'}])
HEAD = (b'SIZE 50 mm,30 mm\r\nGAP 2 mm,0 mm\r\nDIRECTION 1\r\nREFERENCE 0,0\r\nSPEED 4\r\nDENSITY 10\r\nCLS\r\n')


@pytest.fixture
def client(tmp_path):
    return make_client(tmp_path, model='Nelko/PM220', printer=DEVICE)


@pytest.fixture
def sent(monkeypatch):
    out = []
    monkeypatch.setattr(protocol, 'write', lambda device, data: out.append((device, data)))
    return out


def test_label_as_a_bitmap():
    # TSPL prints the dots of a BITMAP that are 0: 1 of the rows is the other way round
    job = protocol.label([b'\x80\x00', b'\x00\x01'], 2, (50, 30), (16, 1), density=10, speed=4, gap=2, direction=1)
    assert job == HEAD + b'BITMAP 16,1,2,2,0,\x7f\xff\xff\xfe\r\nPRINT 1\r\n'


def test_the_label_sizes():
    sizes = {label.identifier: (label.dots_total, label.dots_printable) for label in tspl.LABELS}
    # Calibrated on a real printer: the printhead has 384 dots of the 400 of the label,
    # 29 dots of its top are fed before it prints, the margins are those of labelprint
    assert sizes['tspl50x30'] == ((400, 240), (368, 200))
    assert sizes['tspl40x30'] == ((320, 240), (288, 200))
    assert sizes['tspl40x20'] == ((320, 160), (288, 120))
    assert tspl.NAMES['tspl50x30'] == '50 x 30 mm die-cut (Nelko)'
    assert tspl.NAMES['tspl40x20'].endswith('not calibrated')


def test_same_dots_as_labelprint_printed_the_calibrated_50x30_labels():
    """The calibration of labelprint: the label drawn as 400 x 240 dots, art within 2 mm of its left and
    of the printhead's end and at least 30 dots from its top, all moved up 29 dots and sent as one BITMAP 0,0.
    What this driver sends as a smaller BITMAP must print at the same dots."""
    rng = random.Random(1)
    printable = Image.new('1', (368, 200), 1)
    printable.putdata([rng.randint(0, 1) for _ in range(368 * 200)])

    class _Label:
        label_content = None

        def generate(self):
            return printable.convert('RGB')
    _, rows, width = tspl.label_rows(_Label(), 'tspl50x30')
    job = protocol.label(rows, width, (50, 30), (tspl.MARGIN_X, tspl.MARGIN_TOP), density=10, speed=4, gap=2, direction=1)
    assert job.startswith(HEAD + b'BITMAP 16,1,46,200,0,')

    # What labelprint made of the label, its design as 400 x 240 dots, 1 white, as its packMonochrome does
    design = Image.new('1', (400, 240), 1)
    design.paste(printable, (16, 30))
    moved_up = Image.new('1', (400, 240), 1)
    moved_up.paste(design.crop((0, 29, 400, 240)), (0, 0))

    # What this driver sent, laid on the same dots
    data = job.split(b'BITMAP 16,1,46,200,0,', 1)[1][:46 * 200]
    sent_dots = Image.new('1', (400, 240), 1)
    sent_dots.paste(Image.frombytes('1', (368, 200), data), (16, 1))
    assert sent_dots.tobytes() == moved_up.tobytes()


def test_label_is_printed_as_large_as_it_is(client, sent):
    response = client.post('/labeldesigner/api/print', data={'label_size': 'tspl50x30', 'print_type': 'text', 'text': TEXT})
    assert outcome(client, response) == ('printed', '')
    (device, data), = sent
    assert device == DEVICE
    assert data.startswith(HEAD + b'BITMAP 16,1,46,200,0,') and data.endswith(b'\r\nPRINT 1\r\n')
    assert len(data) == len(HEAD) + len(b'BITMAP 16,1,46,200,0,') + 46 * 200 + len(b'\r\nPRINT 1\r\n')
    # Black is printed: 0
    assert b'\x00' in data


def test_smaller_labels_are_their_size(client, sent):
    client.post('/labeldesigner/api/print', data={'label_size': 'tspl40x20', 'print_type': 'text', 'text': TEXT})
    assert sent[0][1].startswith(b'SIZE 40 mm,20 mm\r\n') and b'BITMAP 16,1,36,120,0,' in sent[0][1]


def test_copies_are_one_label_each(client, sent):
    client.post('/labeldesigner/api/print', data={'label_size': 'tspl50x30', 'print_type': 'text', 'text': TEXT, 'print_count': '2'})
    assert sent[0][1].count(b'SIZE 50 mm') == 2 and sent[0][1].count(b'PRINT 1\r\n') == 2


def test_rows_top_of_a_label_first():
    class _Label:
        label_content = None

        def generate(self):
            # A 50 x 30 mm label, its top black
            img = Image.new('RGB', (368, 200), 'white')
            img.paste((0, 0, 0), (0, 0, 368, 10))
            return img
    _, rows, width = tspl.label_rows(_Label(), 'tspl50x30')
    assert (len(rows), width) == (200, 46)
    # Its top leaves the printer first: the first row is black, 1 in these rows, the last is white
    assert all(byte == 0xff for byte in rows[0]) and not any(rows[-1])


def test_label_lying_is_turned_across_the_printhead():
    class _Label:
        label_content = None

        def generate(self):
            # Drawn lying, its start black: 200 dots along, 368 across
            img = Image.new('RGB', (200, 368), 'white')
            img.paste((0, 0, 0), (0, 0, 10, 368))
            return img
    img, rows, width = tspl.label_rows(_Label(), 'tspl50x30')
    assert img.size == (368, 200) and (len(rows), width) == (200, 46)


def test_label_over_the_network(client, monkeypatch):
    without_status(monkeypatch)
    server = socket.create_server(('127.0.0.1', 0))
    received = []

    def accept():
        conn, _ = server.accept()
        with conn:
            while data := conn.recv(65536):
                received.append(data)
    thread = threading.Thread(target=accept)
    thread.start()
    monkeypatch.setattr(protocol, 'PORT', server.getsockname()[1])
    response = client.post('/labeldesigner/api/print', data={
        'printer': 'tcp://127.0.0.1', 'label_size': 'tspl50x30', 'print_type': 'text', 'text': TEXT})
    thread.join(5)
    server.close()
    assert outcome(client, response) == ('printed', '')
    assert b''.join(received).startswith(HEAD + b'BITMAP 16,1,46,200,0,')


def test_printer_on_usb_that_is_not_there(client, sent):
    printer_ = client.get('/labeldesigner/api/printer_status').get_json()['printers'][0]
    assert printer_['errors'] == ['The printer is switched off or not connected']
    response = client.post('/labeldesigner/api/print', data={'label_size': 'tspl50x30', 'print_type': 'text', 'text': TEXT})
    # Printing does not ask it
    assert outcome(client, response) == ('printed', '')


def test_600_dpi_is_refused(client, sent):
    response = client.post('/labeldesigner/api/print', data={
        'label_size': 'tspl50x30', 'print_type': 'text', 'text': TEXT, 'high_res': '1'})
    assert response.get_json() == {'success': False, 'message': 'The Nelko PM220 printer cannot print at 600 dpi, turn off 600 dpi printing'}
    assert sent == []


@pytest.mark.parametrize('status, errors', [
    (0x00, []),
    (0x20, []),
    (0x01, ['The printhead is open']),
    (0x04, ['No labels are in the printer']),
    (0x05, ['The printhead is open', 'No labels are in the printer']),
    (0x10, ['The printer is paused']),
    (0x80, ['The printer reports an error']),
])
def test_what_the_status_byte_tells(status, errors):
    assert protocol.errors(status) == errors


def _answering(monkeypatch, answer: bytes):
    """A printer on the network that answers the status request with the bytes."""
    server = socket.create_server(('127.0.0.1', 0))
    asked = []

    def accept():
        conn, _ = server.accept()
        with conn:
            asked.append(conn.recv(16))
            if answer:
                conn.sendall(answer)
            else:
                conn.settimeout(3)
                try:
                    conn.recv(1)
                except OSError:
                    pass
    thread = threading.Thread(target=accept)
    thread.start()
    monkeypatch.setattr(protocol, 'PORT', server.getsockname()[1])
    monkeypatch.setattr(protocol, 'ANSWER_WAIT', 0.5)
    monkeypatch.setattr(devices, 'status_cache', {})
    return thread, server, asked


def test_status_over_the_network(monkeypatch):
    thread, server, asked = _answering(monkeypatch, b'\x04')
    state = tspl.DRIVER.status('tcp://127.0.0.1', 'Nelko/PM220')
    thread.join(5)
    server.close()
    assert asked == [protocol.STATUS_REQUEST]
    assert state['errors'] == ['No labels are in the printer'] and state['status_type'] == 'Error occurred'


def test_status_of_a_printer_that_is_printing(monkeypatch):
    thread, server, _ = _answering(monkeypatch, b'\x20')
    state = tspl.DRIVER.status('tcp://127.0.0.1', 'Nelko/PM220')
    thread.join(5)
    server.close()
    assert state['errors'] == [] and state['phase_type'] == 'Printing state'


def test_status_without_an_answer_is_an_error(monkeypatch):
    thread, server, _ = _answering(monkeypatch, b'')
    with pytest.raises(OSError):
        tspl.DRIVER.status('tcp://127.0.0.1', 'Nelko/PM220')
    thread.join(5)
    server.close()
