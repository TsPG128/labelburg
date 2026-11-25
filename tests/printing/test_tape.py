import importlib
import pkgutil

import pytest

from app.labeldesigner import drivers
from app.labeldesigner import tape
from app.labeldesigner.tape import Tape


def reported(model, width, length=0, **more):
    return {'model': model, 'media_width': width, 'media_length': length, **more}


def test_dk_and_tze_tape_of_one_size_are_told_apart_by_the_model():
    assert tape.detect(reported('PT-P750W', 12), '', '62').id == 'pt12'
    assert tape.detect(reported('QL-800', 62, red_roll=False), '', '62') == Tape('62', assumed=False)
    # Without red_roll a QL-800 cannot tell whether its roll has red
    assert tape.detect(reported('QL-800', 62), '', '62').red_unknown


def test_tape_the_printer_reports_wins_over_one_set_by_hand():
    assert tape.detect(reported('QL-800', 29, 90, red_roll=False), '62', '62') == Tape('29x90', assumed=False)


def test_tape_set_by_hand_counts_where_the_printer_reports_none_or_one_not_offered():
    assert tape.detect(reported('QL-800', None), '62', '62') == Tape('62', assumed=False, manual=True)
    t = tape.detect(reported('QL-800', 40), '62', '62')
    assert (t.id, t.manual, t.assumed, t.unknown) == ('62', True, False, '')


def test_tape_set_by_hand_counts_where_the_model_cannot_print_the_reported_one():
    # A QL-500 has no red tape, the status is that of a QL-800 with a red roll
    t = tape.in_printer(reported('QL-800', 62, red_roll=True), 'QL-500', '29', '62')
    assert (t.id, t.manual) == ('29', True)


def test_size_no_label_matches_is_named_and_the_default_assumed():
    t = tape.detect(reported('QL-800', 40), '', '62')
    assert (t.id, t.assumed, t.unknown, t.known) == ('62', True, '40 mm', False)
    assert tape.detect(reported('QL-800', 40, 30), '', '62').unknown == '40 x 30 mm'


def test_printer_that_measures_only_the_length_has_the_labels_of_that_length():
    # A ZPL printer measures the length of its labels, here of two widths
    status = reported('Zebra/ZPL', None, 50)
    t = tape.detect(status, '', '62')
    assert (t.known, t.unknown, t.candidates) == (False, '50 mm long', ('zpl100x50', 'zpl80x50'))
    # One set by hand among them is the tape
    t = tape.detect(status, 'zpl80x50', '62')
    assert (t.id, t.known, t.manual, t.unknown) == ('zpl80x50', True, True, '')
    assert tape.describe(t)['candidates'] == ['zpl100x50', 'zpl80x50']
    # One of another length, e.g. set for the labels before, counts as none
    t = tape.detect(status, 'zpl102x51', '62')
    assert (t.known, t.manual, t.unknown) == (False, False, '50 mm long')
    design = {'label_size': 'zpl100x50', 'orientation': 'standard'}
    assert tape.on_tape(design, t) is design


def test_printer_that_measures_a_length_only_one_label_size_has_reports_it():
    status = reported('Zebra/ZPL', None, 148)
    assert tape.detect(status, '', '62') == Tape('zpl105x148', assumed=False, candidates=('zpl105x148',))
    assert tape.detect(status, 'zpl105x148', '62').manual
    assert not tape.detect(status, 'zpl100x50', '62').known
    # Of a length no label size has, labels keep their size
    t = tape.detect(reported('Zebra/ZPL', None, 77), '', '62')
    assert (t.known, t.unknown, t.candidates) == (False, '77 mm long', ())


def test_assumed_tape_is_one_the_printer_takes():
    assert tape.detect(reported('PUQU/Q00', None), '', '62') == Tape('puqu50x30', assumed=True)
    assert tape.detect(reported('QL-700', None), '', '62') == Tape('62', assumed=True)


def test_red_roll_and_a_roll_of_unknown_color():
    assert tape.detect(reported('QL-800', 62, red_roll=True), '', '62').id == '62red'
    assert tape.detect(reported('QL-800', 62, red_roll=None), '', '62').red_unknown
    assert tape.fits('62red', tape.detect(reported('QL-800', 62, red_roll=None), '', '62'))
    assert not tape.fits('62red', tape.detect(reported('QL-800', None), '62', '62'))
    assert not tape.moves('62red', tape.detect(reported('QL-800', 62, red_roll=None), '', '62'))


def test_label_for_62_mm_is_placed_wide_on_29_x_90_labels():
    t = tape.detect(reported('QL-800', 29, 90), '', '62')
    design = {'label_size': '62', 'orientation': 'standard', 'cable_flag': '1', 'text': 'x'}
    assert tape.on_tape(design, t) == {'label_size': '29x90', 'orientation': 'standard', 'cable_flag': '0', 'text': 'x'}
    assert design['label_size'] == '62'


def test_on_endless_tape_the_text_keeps_its_direction():
    t = tape.detect(reported('QL-800', 29), '', '62')
    assert tape.on_tape({'label_size': '62', 'orientation': 'standard'}, t) == {'label_size': '29', 'orientation': 'standard'}
    assert tape.on_tape({'label_size': '62', 'orientation': 'rotated'}, t) == {'label_size': '29', 'orientation': 'rotated'}


def test_orientation_other_than_rotated_is_standard():
    # As the renderer reads it
    t = tape.detect(reported('QL-800', 29), '', '62')
    for design in ({'label_size': '62', 'orientation': ''}, {'label_size': '62', 'orientation': 'portrait'}, {'label_size': '62'}):
        assert tape.on_tape(design, t)['orientation'] == 'standard'


def test_unknown_tape_leaves_the_label_alone():
    design = {'label_size': '62', 'orientation': 'standard'}
    assert tape.on_tape(design, tape.detect(reported('QL-800', None), '', '62')) is design


def test_description_lists_what_fits_moves_and_where_it_goes():
    d = tape.describe(tape.detect(reported('QL-800', 29, 90), '', '62'))
    assert (d['id'], d['known'], d['manual']) == ('29x90', True, False)
    assert '29x90' in d['fits'] and '62' in d['moves'] and '29x90' not in d['moves']
    assert d['place']['62|standard'] == {'label_size': '29x90', 'orientation': 'standard', 'cable_flag': '0'}
    assert tape.describe(tape.detect(reported('QL-800', None), '', '62'))['place'] == {}


def test_label_of_the_same_size_only_takes_the_name_of_the_tape():
    t = tape.detect(reported('QL-1100', 102, 51, red_roll=False), '', '62')
    design = {'label_size': 'zpl102x51', 'orientation': 'rotated', 'cable_flag': '1'}
    assert tape.on_tape(design, t) == {'label_size': '102x51', 'orientation': 'rotated', 'cable_flag': '1'}
    assert tape.describe(t)['place']['zpl102x51|rotated'] == {'label_size': '102x51', 'orientation': 'rotated'}
    assert not tape.placed('zpl102x51', t) and tape.placed('62', t)


def test_no_label_size_is_placed_on_a_tape():
    assert not tape.moves('foo', tape.detect(reported('QL-800', 29, 90), '', '62'))
    assert tape.on_tape({'label_size': 'foo', 'orientation': 'standard'}, tape.detect(reported('QL-800', 29, 90), '', '62'))['label_size'] == 'foo'


@pytest.mark.parametrize('status, size_id', [
    (reported('QL-800', 62), '62'),
    (reported('QL-800', 29, 90), '29x90'),
    (reported('QL-800', 62, red_roll=True), '62red'),
    (reported('QL-800', 62, red_roll=None), '62'),
    (reported('QL-810W', 62, media_type='Continuous length tape (red)'), '62red'),
    (reported('QL-800', 12), '12'),
    (reported('PT-P750W', 12), 'pt12'),
    (reported('VC-500W', 12), 'vc12'),
    (reported('Niimbot/D110_M', 12, 40), 'niimbot12x40'),
    # Round and square labels of the same size, told apart by the printer
    (reported('Niimbot/B1', 50, 50, media_type='Round die-cut labels'), 'niimbotd50'),
    (reported('Niimbot/B1', 50, 50, media_type='Die-cut labels'), 'niimbot50x50'),
    (reported('QL-800', 24, 24, media_type='Die-cut labels'), 'd24'),
    # A printer of no known model takes every label size
    (reported('Unknown', 29, 90), '29x90'),
])
def test_tape_a_printer_reports_is_found(status, size_id):
    t = tape.detect(status, '', '62')
    assert (t.id, t.assumed) == (size_id, False)
    assert tape.in_printer(status, status['model'], '', '62') == t


@pytest.mark.parametrize('status, default, size_id', [
    (reported('QL-800', None), '62', '62'),
    (reported('QL-800', 50, 50), '62', '62'),
    (reported('QL-800', None), '29', '29'),
    (reported('QL-800', 36), '62', '62'),
    # The default is not for this printer: the first size it takes
    (reported('PUQU/Q00', None), '62', 'puqu50x30'),
    (reported('VC-500W', 30), '62', 'vc9'),
    # The default for the same paper of another model: the printer's size of it
    (reported('Epson/ESC-POS-180', None), 'escpos58', 'escpos58-180'),
])
def test_tape_is_assumed_where_none_is_reported(status, default, size_id):
    t = tape.detect(status, '', default)
    assert (t.id, t.assumed) == (size_id, True)
    assert tape.in_printer(status, status['model'], '', default) == t


@pytest.mark.parametrize('manual', [62, [1], {'a': 1}, None])
def test_hand_set_tape_that_is_no_text_is_none(manual):
    # A hand-edited settings file may hold anything
    assert tape.hand_set(manual, 'QL-800') == ''
    assert not tape.in_printer(reported('QL-800', None), 'QL-800', manual, '62').known


# As each driver package sets it: ESC/POS and PUQU printers tell no tape
REPORTS_TAPE = {'brother': True, 'escpos': False, 'niimbot': True, 'puqu': False, 'tspl': False, 'vc500w': True, 'zpl': True}


@pytest.mark.parametrize('package', [m.name for m in pkgutil.iter_modules(drivers.__path__) if m.ispkg])
def test_each_driver_tells_whether_its_status_tells_the_tape(package):
    driver = importlib.import_module(f'{drivers.__name__}.{package}').DRIVER
    assert driver.reports_tape is REPORTS_TAPE[package]
    assert all(drivers.for_model(model).reports_tape is REPORTS_TAPE[package] for model in driver.models)


def test_tape_is_taken_from_the_hand_set_one_where_the_driver_reports_none():
    # The status of such a driver is not used
    t = tape.in_printer(reported('Epson/ESC-POS', 62), 'Epson/ESC-POS', '', '62')
    assert t.assumed
    t = tape.in_printer(reported('QL-800', 29, 90), 'QL-800', '62', '62')
    assert t.id == '29x90'


@pytest.mark.parametrize('model, printed', [('Epson/ESC-POS-180', ['escpos80-180', 'escpos58-180', '62']),
                                            ('Epson/ESC-POS', ['escpos80', 'escpos58', '62'])])
def test_label_for_the_same_paper_of_the_other_model_is_on_the_printers_size(model, printed):
    # Also while the paper in the printer is not known: escpos80 and
    # escpos80-180 are the same paper, 62 mm tape is none of it
    t = tape.in_printer({}, model, '', '62')
    assert t.assumed
    shown = tape.describe(t)
    for size, size_printed in zip(('escpos80', 'escpos58-180', '62'), printed):
        design = {'label_size': size, 'orientation': 'rotated'}
        assert tape.on_tape(design, t) == {'label_size': size_printed, 'orientation': 'rotated'}
        assert not tape.placed(size, t)
        assert (size in shown['moves']) == (size != size_printed)
        assert shown['place'].get(f'{size}|rotated', design) == {'label_size': size_printed, 'orientation': 'rotated'}


def test_paper_set_by_hand_for_the_other_model_is_the_same_paper():
    # e.g. kept from before the printer was known to have a 180 dpi head
    t = tape.in_printer({}, 'Epson/ESC-POS-180', 'escpos58', '62')
    assert (t.id, t.known, t.manual) == ('escpos58-180', True, True)
    design = {'label_size': 'escpos58', 'orientation': 'standard'}
    assert tape.on_tape(design, t) == {'label_size': 'escpos58-180', 'orientation': 'standard'}
    assert not tape.placed('escpos58', t) and tape.placed('escpos80', t)


def test_labels_of_a_page_tell_which_side_runs_along(monkeypatch):
    # Two 20 x 30 mm labels side by side: a 40 x 30 mm page of labels longer than wide
    from app.labeldesigner.drivers.labels import FormFactor, Label
    page = Label('test20x30-2x1', (40, 30), FormFactor.DIE_CUT, (320, 240), (320, 240), 0, pieces=(2, 1, 0))
    monkeypatch.setitem(tape.SIZES, page.identifier, page)
    assert tape._long_along_tape(page.identifier)
