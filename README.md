# Nova Tickets
Novatickets is a service for booking workplaces in the office.

## Components:
1. **Python 3.8**
2. **Redis** — Cache service
3. **Postgres** — DB 
4. **Sreamlit** - Web view
5. **Flask** - Request handler
6. **Nginx** - web serving 


# Installation
    git clone https://github.com/selezGit/novatickets.git
    cd novatickets/
    pip install -r ticket_service/requirements/base.txt

# Usage
Before starting the project, you need to run redis and postgresql + specify the connection settings to them in the file ticket_service/src/core/config/config.py

    cd ticket_service/src
    python main.py


# demo

![](ticket_service/src/static/img/demo.gif)