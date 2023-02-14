#!/bin/bash
pyinstaller --onefile --noconsole --add-data="resource/ui/maingui.glade;resource/ui" displayin.py