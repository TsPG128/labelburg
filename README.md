# Labelburg

[![Python tests](https://github.com/DL6ER/labelburg/actions/workflows/ci.yml/badge.svg)](https://github.com/DL6ER/labelburg/actions/workflows/ci.yml) [![CodeQL Advanced](https://github.com/DL6ER/labelburg/actions/workflows/codeql.yml/badge.svg)](https://github.com/DL6ER/labelburg/actions/workflows/codeql.yml) [![Build and push images to GHCR.io](https://github.com/DL6ER/labelburg/actions/workflows/devcontainer-ghcr.yml/badge.svg)](https://github.com/DL6ER/labelburg/actions/workflows/devcontainer-ghcr.yml)

Design and print labels 100% offline. With Labelburg you design labels in your web browser, on a computer or a phone, and print them on your label printer. You set it up once on a computer that is always on, e.g., a Raspberry Pi or a home server, and everyone at home or in the office can use it from their browser. It needs no cloud and no app of the printer's maker, and your saved labels stay on that computer, also through updates. Labelburg is 100% free, with no account, no subscription and no paid version, forever. It is fully open source under the GPLv3: all of the code is on GitHub and stays fully open.

![Label designer](./screenshots/image1.png)

## Supported printers

| Vendor | Printers | Labels |
|---|---|---|
| Brother | PT-E550W\*, PT-P700, PT-P750W | TZe tapes 6 to 24 mm wide: laminated, non-laminated and fabric (iron-on) tapes, and heat-shrink tubes in compatible cassettes |
| Brother | PT-P900W, PT-P950NW | TZe tapes 18 and 36 mm wide |
| Brother | QL-500, QL-550, QL-560\*, QL-570, QL-580N, QL-600, QL-650TD, QL-700\*, QL-710W, QL-720NW | up to 62 mm wide |
| Brother | QL-800, QL-810W\*, QL-820NWB | up to 62 mm wide, also black/red |
| Brother | QL-1050, QL-1060N, QL-1100\*, QL-1110NWB, QL-1115NWB | up to 103 mm wide, e.g. 4 x 6 in shipping labels |
| Brother | VC-500W\* | 9 to 50 mm wide ZINK tape in full color, about 40 s per label |
| Epson | ESC/POS receipt printers (USB or network), e.g., the TM-T20II\* and TM-T20III\* | 80 and 58 mm receipt paper, cut, or torn off on printers without a cutter such as the TM-P20, with as much blank paper before each receipt as the cutter is away from the head |
| Niimbot | D110_M\* (Bluetooth) | 12 to 15 mm wide die-cut thermal labels, torn off, printed on 12 x 40 mm only |
| Niimbot | B1\* (USB, Bluetooth) | 40 and 50 mm wide die-cut thermal labels, also rolls of several small labels to a page, torn off |
| PUQU | Q00\* (Bluetooth), also sold as the [Reekon P1 Tagger](https://reekon.tools/products/p1-tagger-construction-printer) (P1L\*) | 50 x 30, 50 x 80, 40 x 30 and 40 x 50 mm die-cut thermal labels, torn off |
| Zebra | ZPL printers (USB or network), e.g., the GK420t\*, also the Datamax E-4204B\* | common metric and inch die-cut labels up to 104 mm wide, e.g. 4 x 6 in or A6, torn off |
| Nelko | PM220 (also sold as the P20), and other TSPL printers with a 48 mm printhead (USB or network, e.g. behind p910nd) | 50 x 30 mm die-cut thermal labels, calibrated on a real printer; 40 x 30 and 40 x 20 mm not yet, torn off |

\* Tried on a real printer. The others are built from the makers' technical documents and open source drivers.

**Not sure which printer to buy?** Try it first: the demo printer can be any printer in this list. Choose its model and roll in the Settings, design your labels and see how they fit on that printer's labels before you buy it. It needs no printer at all.

Labelburg finds printers plugged in with USB by itself, most network printers too. Printers the search does not find can be added in the Settings of the label designer. It sees which labels are loaded and offers only the sizes that fit, on the QL-800 series it knows whether the roll is black and red, and on P-touch printers the preview shows the colors of the tape, e.g., white on black. A USB printer can also stand somewhere else, plugged into a small board on your network, see [USB printer on another device](docs/usbip.md).

## Features

- **Text:** font, size, alignment, line and letter spacing for each line, capitals, inverted text, checkboxes for to-do lists, red text on black/red labels and any color on the VC-500W. Long lines wrap, and the text can shrink to fit the label or grow as large as fits, at the top, in the middle or at the bottom of die-cut labels. Emoji and symbols, e.g., check marks, stars and arrows, can be typed right into the text.
- **Codes:** QR, DataMatrix, Micro QR, Aztec and PDF417 codes, a long, flat QR code for narrow tape, and barcodes like EAN, UPC, Code 128, Code 39, ITF, GS1-128 and ISBN, alone or with text. Labelburg tells you when a code may be too small to scan.
- **Pictures:** photos, drawings and PDFs, dropped, chosen or pasted, several at once, alone or with text and a code. Labelburg fits, crops and turns them and makes them black and white (or black and red) for the printer, and on the VC-500W it can make faint drawings stronger.
- **Filled in when printing:** blanks Labelburg asks for when you print, e.g., a name or a choice from a list, numbers that count up from label to label, e.g., "Box 1 of 6", and today's date or a date some days ahead, e.g., "best before", with months and weekdays [in your language](docs/languages.md).
- **Icons:** 7400 icons, e.g., a light bulb, and symbols of screws, nuts, washers and electronic parts for workshop bins, next to the text, found by name.
- **Labels:** save your labels, group them by tags and print them again, pass them on as files, or start from one of about 740 ready-made labels in English and German, e.g., addresses, safety signs, hazard labels, name badges, price tags and pictures for kids.
- **Printing:** copies, cut after every label, only after the last one or not at all, half cuts and chain printing on P-touch printers, labels of a fixed length, borders, round labels, flags that fold around a cable, mirrored for clear tape behind glass, which end of a label comes out first, a sharper slow mode and a faster one. While a job prints, Labelburg shows how long it still takes. Labels sent while the printer is busy wait in a queue shown at the print message, also when Labelburg restarts, and waiting ones can be removed. Every label printed, from any browser or program, can be printed again from the list of printed labels. A last label left in the printer, e.g., after printing without a cut, comes out with "Feed and cut" at the printer in the Settings. Labels that come out off to one side on a Niimbot B1 are lined up with a calibration label: choose "Calibrate printer" at the printer in the Settings.
- **Easy to use:** a preview that shows the label as it will come out, templates that show the text you type in them, search, undo and dark mode. It works on phones and can be installed like an app, which on Android also takes pictures, PDFs and links from the share menu.
- **Several printers:** use several printers at once, each with a name of your choice and the same settings in every browser, or try everything without a printer on the demo printer, as any printer Labelburg supports.
- **Other programs:** e.g., [Grocy](docs/grocy.md) and [Homebox](docs/homebox.md) can print their labels through Labelburg, [Home Assistant](docs/home-assistant.md) prints yours from a button, an NFC tag or by voice, labels with the next archive serial number for [Paperless-ngx](docs/paperless.md) stick on your paper documents, and [AI assistants](docs/mcp.md) can find, fill in and print your labels for you.

## Screenshots

| Saved and ready-made labels | Image with text |
|---|---|
| ![Saved and ready-made labels](./screenshots/image2.png) | ![Image with text](./screenshots/image3.png) |
| **Barcodes** | **Your text in the templates, in dark mode** |
| ![Barcodes](./screenshots/image4.png) | ![Your text in the templates, in dark mode](./screenshots/image6.png) |
| **Blanks, filled in when printing** | **Printer settings** |
| ![Blanks, filled in when printing](./screenshots/image7.png) | ![Printer settings](./screenshots/image8.png) |

## Installation

Labelburg runs in [Docker](https://docs.docker.com/get-started/get-docker/) on a Linux computer, e.g., a Raspberry Pi with a 64-bit system, a home server or a NAS. The printer is plugged into that computer or on the same network.

Install Docker on the computer, make a folder, e.g., `labelburg`, and save this in it as `docker-compose.yml`:

``` yaml
services:
  labelburg:
    image: ghcr.io/dl6er/labelburg:latest
    container_name: labelburg
    restart: always
    privileged: true
    network_mode: host
    volumes:
      - /dev/usb:/dev/usb
      - /dev/bus/usb:/dev/bus/usb
      - ./labels:/app/labels
    environment:
      - TZ=Europe/Berlin  # your time zone, for dates on labels
```

Switch the printer on and start Labelburg in that folder with `docker compose up -d`. Then open `http://<computer>:8013` in a browser, e.g., `http://192.168.1.10:8013`.

Your labels are saved in the folder `labels` next to the file. To get a new version, run `docker compose pull && docker compose up -d` in the folder. To report a problem, click "Report a problem" in the Settings under About: it opens the form on GitHub with the version and your printers filled in.

## Technical details

Everything below is for those who want to set Labelburg up in depth, use it from their own programs or work on it. You don't need it to design and print labels.

### Settings

| Environment variable | Meaning | Default |
|---|---|---|
| `PRINTER_PRINTER` | The printer, see [Printer addresses](#printer-addresses) | `?` |
| `PRINTER_MODEL` | Model of a printer that does not report it, e.g. a network printer. Models of other makers than Brother are named with their maker, e.g. `PUQU/Q00` or `Epson/ESC-POS` (`Epson/ESC-POS-180` for a receipt printer with a 180 dpi head, e.g. a TM-T88), Brother ones with or without it (`Brother/QL-800`). | `QL-800` |
| `PRINTERS` | Several printers of different models instead of `PRINTER_PRINTER` and `PRINTER_MODEL`, as `<model>=<printer>`, comma-separated, e.g., `QL-700=usb://0x04f9:0x2042,QL-1100=file:///dev/usb/lp1,PUQU/Q00=bt://<MAC>`, the models as for `PRINTER_MODEL`. A name in front, e.g., `Kitchen:QL-700=usb://0x04f9:0x2042`, is shown in the label designer, and requests may choose the printer by it (`printer=Kitchen`). There is no detection, each printer keeps its model and its own printer settings, requests that name no printer go to the first one. The demo printer is offered only when listed, e.g., `QL-700=simulation`. | none |
| `ADD_PRINTERS` | Where printers the search does not find may be added in the Settings of the label designer: `local` only in your own network (private addresses, `localhost`, 100.64.0.0/10 as on Tailscale, which also holds the carrier-grade NAT of your provider, and names like `printer.local` that lead there), `any` also elsewhere, `off` not at all, printers added before are then not used. The same holds for network printers that requests name by their address, e.g., `tcp://<host>`, and that are neither configured, added nor found by the search. Anyone who can open Labelburg can add printers, there is no login, and the answers of Identify show them which hosts and ports exist there, the refusals of requests whether a name exists and is local. | `local` |
| `LABEL_DEFAULT_SIZE` | Label size the label designer starts with when the printer does not report its roll, e.g., the demo printer. The name tells the kind: `62` or `102` is endless tape, `62x29` or `103x164` die-cut labels, `d24` round ones. | `62` |
| `LABEL_DEFAULT_ORIENTATION` | `standard` or `rotated` | `standard` |
| `LABEL_TEMPLATE_ENV_VARS` | Environment variables labels may insert with `{{env:<var>}}`, comma-separated. All others stay empty, so that nobody can read secrets of the server through a label. | none |
| `WEBHOOK_PASSWORD` | Turns on the webhook, see [API](#api) | off |
| `PAPERLESS_URL`, `PAPERLESS_TOKEN` | Address and API token of Paperless-ngx, whose next archive serial number `[ASN]` continues from, see [Paperless-ngx](docs/paperless.md) | none |
| `HOSTS` | Further host names Labelburg answers besides those of the home network, comma-separated, e.g., `labels.example.com` or `.example.com` with its subdomains, see [Host names](#host-names). `MCP_HOSTS`, its former name, still works. | none |
| `TRUSTED_HOSTS` | Only these host names, comma-separated, e.g., `labels.local,192.168.0.10`, instead of those of the home network and `HOSTS` | none |
| `PROXY_COUNT` | Number of reverse proxies in front of the server, e.g. to serve the label designer below a path, see [Reverse proxy](docs/reverse-proxy.md). Only then the `X-Forwarded-*` headers they set are used, others could fake them. | `0` |
| `PRINT_MAX_COUNT` | Most labels per print request | `100` |
| `MCP_ENABLED` | `false` to turn off the [MCP endpoint](docs/mcp.md) for AI assistants | `true` |
| `MCP_MAX_COUNT` | Most labels per call of an [AI assistant](docs/mcp.md) | `10` |
| `MAX_CONTENT_LENGTH` | Largest request in bytes, e.g. for uploaded images | 32 MB |
| `FONT_FOLDER` | Folder with more fonts, see [Fonts](#fonts) | none |
| `SYSTEM_FONTS` | `false` to offer only the fonts of `FONT_FOLDER`, not those installed on the system | `true` |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL` | `WARNING` |
| `SERVER_PORT` | Port the server listens on with `python3 run.py`, e.g. for several instances on one host. The container always uses 8013, map another port with `ports:`. | `8013` |

Other settings, e.g. the default font and margins, go into `instance/application.py`, see [`config.py`](./config.py). Environment variables take precedence over it. An invalid value stops the server at startup with a message naming the variable.

### Host names

Labelburg answers only requests for the names a home network uses, IP addresses, single-label names (e.g., `printserver`) and names ending in `.local`, `.lan`, `.home`, `.home.arpa`, `.internal`, `.localdomain` or `.fritz.box`, and for those listed in `HOSTS`. That protects against DNS rebinding, where a website points its own name at your server to use it through your browser. Other names go into `HOSTS`, e.g., of a domain of your own, behind a [reverse proxy](docs/reverse-proxy.md), of Tailscale (`*.ts.net`) or of dynamic DNS like DuckDNS or `synology.me`.

### Printer addresses

| Address | Printer |
|---|---|
| `?` | Printers found automatically: on USB, also ones plugged in later, and on the network, see [Network printers](#network-printers) |
| `file:///dev/usb/lp<N>` | A USB printer, Linux only |
| `usb://<vendor>:<product>[/<serial number>]` | A Brother, Epson or ZPL printer on USB, also on macOS. On Windows untested, PyUSB needs the WinUSB driver for the printer, e.g. installed with Zadig. The serial number tells printers of the same model apart. |
| `tcp://<host>` | A network printer, an IPv6 address in brackets |
| `vc500w://<host>` | A VC-500W on the network |
| `usbip://<host>` | A USB printer another device shares, see [USB/IP](docs/usbip.md) |
| `bt://<MAC>[/<RFCOMM channel>]` | A PUQU Q00, Reekon P1 Tagger, Niimbot D110_M or Niimbot B1 on Bluetooth, channel 2 on a PUQU and 1 on a D110_M if left out. A D110_M has to be paired with the computer, a B1 needs no pairing. In a container only with `network_mode: host`. |
| `simulation` | The demo printer, which saves the labels as PNG files in `simulated_labels` (the newest 100) instead of printing them. Its model and roll are chosen in the Settings of the label designer, else it is `PRINTER_MODEL` or the model listed with it in `PRINTERS`. |

The installation above gives the container all of USB, the network and Bluetooth, so that it finds printers by itself, also a Niimbot B1 nearby on Bluetooth. Other Bluetooth printers are paired with the computer and set up by their `bt://` address. `/dev/usb` holds the printers as `/dev/usb/lp<N>`, `/dev/bus/usb` the USB devices that `usb://<vendor>:<product>` printers are reached through. A printer gets a new device there each time it is plugged in or switched on, so the folder is mounted rather than single devices given. Without `privileged`, the container may use them with `device_cgroup_rules: ['c 189:* rmw']` next to the volume.

To give it a single printer instead, map that one and name it:

``` yaml
services:
  labelburg:
    image: ghcr.io/dl6er/labelburg:latest
    container_name: labelburg
    restart: always
    ports:
      - "8013:8013"
    devices:
      - "/dev/usb/lp0:/dev/usb/lp0"
    volumes:
      - ./labels:/app/labels
    environment:
      - PRINTER_MODEL=QL-800
      - PRINTER_PRINTER=file:///dev/usb/lp0
```

Address each printer in one way only (e.g. always `file:///dev/usb/lp0`). Two addresses of the same printer are not recognized as one, and their jobs could get in each other's way.

### Network printers

Network printers are found when they announce themselves like for Bonjour, which in Docker needs `network_mode: host`, or by a known MAC address prefix in the ARP table. Add others in the Settings of the label designer, or with `tcp://<IP address>` in `PRINTER_PRINTER` or `PRINTERS`, and please open an issue. Network printers report their model, the loaded labels and errors over SNMP (UDP port 161) like to Brother's apps, with the same status as over USB, or else over IPP (port 631), which e.g. on the QL-810W names neither the cause of every error nor endless rolls. Jobs are not sent while a printer reports an error, and an error after a job is shown like for USB printers. Printers that answer neither only take print jobs on port 9100 and report nothing.

### Fonts

The label designer offers all `.ttf` and `.otf` fonts it finds in the system font folders when it starts. The image comes with DejaVu, Droid, FreeFont, Liberation, Noto and Inconsolata. To add fonts, mount a folder with them, e.g. `./fonts:/usr/local/share/fonts/custom:ro`, and restart the container. A saved label whose font is not installed is shown and printed with the default font, and the preview says so. Characters a font has no glyph for, e.g. emoji, are drawn with the first of DejaVu Sans, Noto Sans Symbols 2, Noto Sans Symbols, Noto Sans Math, FreeSerif and the black and white Noto Emoji of Labelburg that has them. To offer only a few fonts, put them (or links to them) into a folder, set `FONT_FOLDER` to it and `SYSTEM_FONTS=false`, and set the default font in `instance/application.py` to one of them.

### Label designer

Besides blanks, counters and dates, labels can insert the number of labels printed together (`{{total}}`, e.g., `Box {{counter}} of {{total}}` for Box 1 of 6 to Box 6 of 6), archive serial numbers for [Paperless-ngx](docs/paperless.md) (`{{asn}}`), UUIDs, random strings and the environment variables listed in `LABEL_TEMPLATE_ENV_VARS`, in the text and in codes. Icons are inserted as `{{mdi:<name>}}`, e.g. `{{mdi:lightbulb}}`, with the names of the [Material Design Icons](https://pictogrammers.com/library/mdi/), fasteners as `{{fastener:<name>}}`, e.g. `{{fastener:head-torx}}`, and electronic components as `{{electronic:<name>}}`, e.g. `{{electronic:resistor-iec-standard}}`. In the label designer, `[` offers them all, and "What the variables do" explains them.

Images can be PNG, JPG, WEBP, AVIF, GIF, TIFF, BMP and many more formats. A PDF gives one label per page if you like.

The browser offers to install the label designer as an app only over HTTPS, e.g., behind a [reverse proxy](docs/reverse-proxy.md) that adds it.

### Image tags

| Tag | Contains | Changes |
|---|---|---|
| `latest` | the newest release | with every release |
| `1` | the newest `1.x` release | with every release of the `1` series |
| `1.0` | the newest `1.0.x` release | with every release of the `1.0` series |
| `1.0.1` | exactly this release | never |
| `dev` | the current state of `master` | with every change and every night |

`latest` is the right choice for most installations. `dev` gets new features and fixes first, e.g. to test a fix from an issue before it is released, but it may also break things. Pre-releases (e.g. `1.1.0-rc.1`) only get their exact tag. All releases are listed on the [releases page](https://github.com/DL6ER/labelburg/releases). Every tag is also pushed as `ghcr.io/dl6er/brother-ql-web`, the name of the images until v3.0.0, so existing installations keep getting updates.

### API

Everything the label designer does is also available as a REST API. It is described in OpenAPI format in [`app/labeldesigner/openapi.json`](app/labeldesigner/openapi.json), which a running server also serves at `/labeldesigner/api/openapi.json` for tools like Swagger UI, Postman or code generators.

```bash
# Print a text label (lines of text as JSON, without "font" the font of new labels is used)
curl -X POST http://localhost:8013/labeldesigner/api/print \
  -F label_size=62 -F 'text=[{"text": "Hello", "size": "70"}]'

# Print the first page of a PDF on a 103 x 164 mm label
curl -X POST http://localhost:8013/labeldesigner/api/print \
  -F label_size=103x164 -F model=QL-1100 -F print_type=image -F image=@label.pdf

# Generate the label image without printing
curl -X POST http://localhost:8013/labeldesigner/api/preview \
  -F 'text=[{"text": "Hello", "size": "70"}]' -o label.png

# Status of the printers
curl http://localhost:8013/labeldesigner/api/printer_status

# Print images with the webhook (needs WEBHOOK_PASSWORD)
curl -X POST http://localhost:8013/labeldesigner/api/webhook/print \
  -H "Authorization: Bearer $WEBHOOK_PASSWORD" -F label_size=62 -F images=@label.png
```

- A request selects a printer with the `printer` parameter: the configured printer, `simulation`, or a printer given as in [Printer addresses](#printer-addresses). A network printer that is neither configured, added in the Settings nor found by the search prints only at an address `ADD_PRINTERS` allows.
- Every print request is answered at once with `{"success": true, "queued": true, "job": ..., "state": ..., "labels": ..., "title": ...}`: the label is accepted into the queue of its printer, which prints the jobs in turn. `labels` is the number of labels of the job, which `{{total}}` shows, not its pages on a roll with several labels to a page. `title` is the name the queue and the printed labels show for it: the `title` of the request, else its first line as printed, its code or the name of its picture. A queue holds at most 20 waiting jobs per printer, each with up to the usual number of labels; a full one, or one whose waiting jobs hold many large images, answers that the printer is busy. A job the printer does not print, e.g. with the tape used up, holds the jobs behind it until someone presses Continue in the label designer or sends `POST /labeldesigner/api/queue/continue` with `printer`. `GET /labeldesigner/api/queue?printer=<path or name>` lists the queue, `GET /labeldesigner/api/queue/<id>` tells the outcome of a job (`waiting`, `printing`, `printed`, `failed` or `removed`, with the reason), and `POST /labeldesigner/api/queue/<id>/remove` removes a waiting one. The queue is kept in `.print-queue` in the folder of the labels: jobs waiting when the server stops print when it starts again, with their ids and the archive serial numbers they took. The job that printed in that moment is not printed again, its outcome is `unknown`. Where the disk has no room for a job it prints from memory and is lost on a restart.
- The labels printed are kept in `.print-history` in the folder of the labels, the entries of the last year, at most 1000; the images of the oldest go beyond 200 MB. `GET /labeldesigner/api/history` lists them newest first, `limit` of them (60, at most 200), those printed before the entry `before` names for the next ones; `GET /labeldesigner/api/history/<id>/preview.png` is the picture of one, `GET /labeldesigner/api/history/<id>/label` opens one made here as a saved label is loaded, `POST /labeldesigner/api/history/<id>/print` prints one again on the `printer` of the request, with the date it printed and the same archive serial numbers, or with `as_before=0` with today's date and new numbers, `print_count` copies and the values of `blanks` in place of those printed, and `POST /labeldesigner/api/history/clear` removes them all. The files are readable by the server only, but everyone who reaches the label designer sees the list. The label setting `history=0` removes those kept and keeps none.
- `POST /labeldesigner/api/feed` with `printer` feeds and cuts the paper of a Brother QL or P-touch printer or an ESC/POS printer, e.g., to cut off the last label of a job printed without a cut or chain printed, and feeds one label on a ZPL printer. It waits in the queue like a label; `feed` of the printer in `printer_status` tells what it does with the tape in it.
- Labels are printed on the tape in the printer, as in the label designer: a label made for another tape is placed on it.
- The printer settings of the label designer (the label size set by hand, cutting, which end of the labels leaves first and quality) are kept on the server in `.printers.json` in the folder of the labels, the same for every browser; `/labeldesigner/api/settings` reads and changes them, `printer_status` tells them with each printer, and print requests and previews of the API take what they leave out from them. A label size left out is that of the tape the printer reports, else the label size set by hand, else `LABEL_DEFAULT_SIZE`.
- `GET /labeldesigner/api/problem_report` tells the version and each printer with its model, connection and labels in plain words, and the bug form on GitHub with them filled in, which "Report a problem" in the Settings under About opens. It names no addresses, host names, serial numbers, names of printers, files or label texts, and the server sends it nowhere.
- The label settings (how dates are written and in which language, the order of copies of several files, the font of new labels and whether printed labels are kept) are kept in the same file; `/labeldesigner/api/settings/labels` reads and changes them. Requests that leave out `collate`, lines without a font and date blanks without a format take them from there, else the order as sets, the default font and `%Y-%m-%d`. `date_language` (see [Labels in your language](docs/languages.md)) writes the names of months and weekdays (`%a`, `%A`, `%b` or `%h`, `%B`, in capitals with `^` or `#`) of all dates in its language as [CLDR](https://cldr.unicode.org/) has them, else they are English: a month as in a date where the format has the day of the month, e.g., `22 listopada 2026` in Polish, else on its own, `listopad 2026`. A name with a width (`%10B`) or the `E` or `O` modifier, and `%c`, `%x` and `%p`, stay as `strftime()` writes them, in English.
- Requests that print, save or delete labels must be `POST` requests and are refused when a browser sends them from another website, so that a malicious page cannot use your printer. Scripts and `curl` are not affected.
- Text lines may have up to 10000 characters (100000 per label) after the templates are filled in, barcodes up to 1000. Labels and images may have up to 64 million pixels, enough for a 62 mm wide label of about 2 m at 600 dpi. Of PDFs the first page is printed, or the pages `pdf_pages` selects (e.g., `1-3, 5` or `all`), each as a label of its own. Several `image` fields in a print request are printed one after the other. Blanks are filled in from `blanks`, e.g., `{"Room": "Garage"}`, also in saved labels printed by name, or else with their default. A saved label printed by name also takes fields of the request named like its blanks, which is how [Grocy](docs/grocy.md) prints its labels. The `name` of a saved label is the one it is saved under in the label designer, e.g., `Frozen on`, or its file name, with or without `.json`.

### Development

The repository has a development container for [VS Code](https://code.visualstudio.com/) with everything needed. It does not mount USB printers, add them in `.devcontainer/devcontainer.json` if you need them. The tests run in Python 3.15 for Alpine Linux, the base image of the published container:

```bash
pip install -r requirements-dev.txt
pytest -n auto
```

The tests in `tests/browser` open the label designer in Chromium and are skipped unless Playwright is installed. Playwright does not run on Alpine, so outside the devcontainer:

```bash
pip install -r requirements-browser.txt
python -m playwright install --with-deps chromium
pytest -n auto tests/browser
```

To build the image yourself, with the commit and build time shown in the Settings under About:

```bash
docker compose build --build-arg GIT_COMMIT=$(git rev-parse HEAD) --build-arg BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
```

Pull requests are welcome: [fork the repository](https://github.com/DL6ER/labelburg/fork), make your changes with tests and open a pull request with a clear description.

## Credits and license

Labelburg, called brother_ql_web until v3.0.0, is a fork of [`pklaus/brother_ql_web`](https://github.com/pklaus/brother_ql_web). It carries the printer code of [`pklaus/brother_ql`](https://github.com/pklaus/brother_ql) and its fork [`matmair/brother_ql-inventree`](https://github.com/matmair/brother_ql-inventree), both GPLv3, in its Brother driver, and builds on improvements from [`tbnobody/brother_ql_web`](https://github.com/tbnobody/brother_ql_web), [`dersimn/brother_ql_web`](https://github.com/dersimn/brother_ql_web) and [`davidramiro/brother_ql_web`](https://github.com/davidramiro/brother_ql_web), for which we are grateful. Brother, P-touch and PUQU are trademarks of their owners, Labelburg is not affiliated with them.

It is published under the terms of the GPLv3, see [LICENSE](./LICENSE). It includes software of third parties under other licenses:

- [Archivo](https://github.com/Omnibus-Type/Archivo), the typeface of the label designer, [SIL Open Font License 1.1](app/static/designer/OFL.txt)
- [Material Design Icons](https://github.com/Templarian/MaterialDesign-Webfont) 7.4.47 by Pictogrammers, the font under the Apache 2.0 License, see [LICENSE](app/static/mdi/LICENSE)
- [Noto Emoji](https://github.com/googlefonts/emoji-bw) by Google, the emoji on the labels, [SIL Open Font License 1.1](app/static/emoji/OFL.txt)
- The fasteners drawn as in [gflabel](https://github.com/ndevenish/gflabel) by Nicholas Devenish under the BSD 3-Clause License, and the [electronic symbols](https://github.com/chris-pikul/electronic-symbols) by Chris Pikul under the MIT License, built into one font by `tools/symbols_font.py`, see [LICENSE](app/static/symbols/LICENSE)
- The pictograms and the photo silhouette of the demo labels from [Wikimedia Commons](app/labeldesigner/demos/images/SOURCES.md), public domain and CC0
- The names of months and weekdays from the [Unicode CLDR](https://cldr.unicode.org/), written by `tools/date_names.py` with [Babel](https://babel.pocoo.org/), under the Unicode License V3, see [LICENSE](app/labeldesigner/cldr/LICENSE)
