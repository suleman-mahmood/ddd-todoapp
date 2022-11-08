# The most awesome Todo list ever created as it magically completes the tasks stored in it even practically!!

### Install the python dependencies:
- `pip install -U pytest`
- `pip install psycopg2`

### Creating a python virtual env:
- `virtualenv --python=/usr/bin/python3.7 venv`
- `source venv/bin/activate`

### Setting up Postgres locally:
- `sudo -u postgres psql`
- `create database todolist;`
- `create user suleman with encrypted password 'root';`
- `grant all privileges on database todolist to suleman;`
- `exit`

### To initialize the postgres and populate with our tables run:
- `psql todolist -af initialize-db.sql`


### Connect to remote Cloud Sql instance using local computer
## Whitelist your public ip in the dashboard for smoother access
- `psql -h 34.136.84.83 -p 5432 -U suleman -d suleman -W`