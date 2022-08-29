# Nova Tickets
Novatickets is a service for booking workplaces in the office.

## Components:
1. **Python 3.8**
3. **Postgres** — DB 
4. **Sreamlit** - Web view


# Installation
    git clone https://github.com/selezGit/novatickets.git
    cd novatickets/
    pip install -r requirements/base.txt

# Usage
Before starting the project, you need to run redis and postgresql + specify the connection settings to them in the file ticket_service/src/core/config/config.py

    cd src/
    streamlit run main.py


# demo

![](src/static/img/demo.gif)