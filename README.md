# GRRAOU bot

A simple python bot to update a MediaWiki resources catalog page from a LibreBooking database. 

# Quick start

- Copy `conf.example.yaml` to `conf.yaml` and make your changes
- Create a virtual environment and install the requirements.txt packages

```bash
python -m venv env --prompt grraou-bot
source env/bin/activate
python -m pip install -f requirements.txt
```

- Insert this comment in your MediaWiki page where you want to insert the resources catalog.

```html
<!-- GrraouBot content below -->
```

- Set a cron job to run GrraouBot every time you want

```bash
crontab -e

# Example for every night at 1am
0 1 * * * /path/to/python.exe /path/to/grraoubot.py
```
