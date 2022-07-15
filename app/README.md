# Houses API
Это API - маркетплейс для недвижимости, который позволяет легко продавать и покупать дома
## Instructions for project preparation
Change directory to app folder:
```bash
cd app
```
First of all you need to create our virtual environment:
```bash
python3 -m venv env
```
Then you need to activate the virtual environment:
```bash
source env/bin/activate
```
After you need to upgrade pip:
```bash
pip install --upgrade pip
```
You need to install the libraries from requirements/development.txt file:
```bash
pip install -r requirements/development.txt
```
## Instructions for project starting
Required to copy and fill up file .env.example to .env:
```bash
copy .env.example .env
```
Activate environment variables:
```bash
source ../.env
```
Create app env variables:
```bash
export APP_MODE=dev
```
```bash
export FLASK_APP=run.py
```
For fast app launching use:
```bash
flask run
```
## Database operations
Before db migrations you need to make actual dump:
```bash
pg_admin -U DB_USER -h DB_HOST -p DB_PORT DB_NAME > dumps/dump_name.dump
```
For commit database migrations use:
```bash
flask db migrate -m "YOUR CHANGES"
```
For upgrade database:
```bash
flask db upgrade
```
For downgrade database:
```bash
flask db downgrade
```
To load dump to database use:
```bash
psql -U DB_USER -h DB_HOST -p DB_PORT DB_NAME < dumps/dump_name.dump
```
## Docker operations
For creating and starting docker development app container use(from project directory):
```bash
cd ..
```
```bash
docker-compose up dev_app_local
```
