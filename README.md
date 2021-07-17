# User editing app


### Requirements
* Python 3.7+
* PostgreSQL 13.3


### Prepare project
```bash
sudo su - postgres


psql -U postgres -c "alter user postgres with password 'postgres';"
psql -U postgres -c "create database user_app;"
exit

# run database
sudo service postgresql start

git clone https://github.com/iFunnyMan520/user-app
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# If you have a PostgreSQL server on a port other than '5432'
export DB_PORT = your_port

pytest -s -v --pdb
```


### Run Project
```bash
chmod +x ./run_server.py

# run server
./run_server.py
```


### Migrations
```bash
alembic revision -m "migration name" --autogenerate
alembic upgrade head

# downgrade by one step
alembic downgrade -1
```