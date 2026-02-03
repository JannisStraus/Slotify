# Slotify

Slotify is a Python project designed to continuously search for available slots
at Morante Hair Salon or Wellnest and send them via Telegram to you mobile
device.

---

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/JannisStraus/Slotify.git
cd Slotify
pip install -e .
```

*Requires **Python ≥ 3.10***

---

## Configuration

Slotify needs two parameters to authenticate against Telegram.
Create a `.env` File with key value pairs like in this [sample](.env_sample):

```txt
BOT_TOKEN=TODO
CHAT_ID=TODO
```

Alternatively, you can export the variables directly in your shell:

```bash
export BOT_TOKEN=TODO
export CHAT_ID=TODO
```

---

## Usage

After installation, you can run the tool directly from the command line:

```bash
slotify morante -m <minutes> -d <days>
```

or

```bash
slotify wellnest -m <minutes> -d <date>
```

---

## Command Line Arguments

### Morante

- `-m`, `--minutes`: *(Optional)* Number of minutes
to wait between checks (default: 5).
- `-d`, `--days`: Number of days in advance
for which to search for available slots.

### Wellnest

- `-m`, `--minutes`: *(Optional)* Number of minutes
to wait between checks (default: 5).
- `-d`, `--date`: Date (DD.MM.YYYY or YYYY-MM-DD) to search for available slots.
