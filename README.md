# Slotify

Slotify is a Python project designed to continuously
search for available slots at Morante Hair Salon and
send them via Telegram to you mobile device.

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
slotify -m <minutes> -d <days>
```

or

```bash
slotify -s <seconds> -d <days>
```

---

## Command Line Arguments

- `-m`, `--minutes`: *(Optional)* Number of minutes
to wait between checks (default: 5).
- `-s`, `--seconds`: *(Optional)* Additional seconds
to wait between checks (default: 0).
- `-d`, `--days`: *(Optional)* Number of days in advance
for which to search for available slots.
