# Краткое описание
Сервис ETL

# Install 

## python
```
pyenv install --list
pyenv install  3.9.6
pyenv versions
pyenv local  3.9.6 
```

## Venv 
```
cd ~/venv/airflow
python -m venv .intep_super-glue
source ./.intep_super-glue/bin/activate
python -m pip install --upgrade pip
```

## Requirements
```
pip install apache-airflow
pip install jsonpath-ng
pip install databases psycopg2-binary asyncpg

# pip install -r requirements.txt
```

## Setup
```
export AIRFLOW_HOME=/mnt/c/DiskD/Work/Intep/services/super-glue/
echo $AIRFLOW_HOME

airflow

-- in database tools under user postgres
> create database airflow_metadata;
> create user airflow WITH password 'yugVRA5NJyp2DRAE'
> grant all privileges on database airflow_metadata to airflow

-- in airflow.cfg
> sql_alchemy_conn = postgresql+psycopg2://airflow:yugVRA5NJyp2DRAE@localhost:5432/airflow_metadata
> load_examples = False

airflow db init

airflow users create --role Admin --username admin --email roman@kasovsky.ru --firstname roman --lastname kasovsky --password admin
```

## Database
```
create database etl_data;
create user etl WITH password 'Jyp2DRAEyugVRA5N';
grant all privileges on database etl_data to etl;

-- in database tools under user etl
create table log (
    id serial PRIMARY KEY,
    data VARCHAR NOT NULL
);
```

# Run
```
cd ~/venv/airflow
source ./.intep_super-glue/bin/activate
cd /mnt/c/DiskD/Work/Intep/services/super-glue
export AIRFLOW_HOME=/mnt/c/DiskD/Work/Intep/services/super-glue/

airflow webserver -p 8080
airflow scheduler
```

# Test

# Docker
```
docker build -t intep/super-glue:1.0 .
docker build --target builder_image -t intep/super-glue:1.0 .

docker scan intep/super-glue:1.0
docker run -p 8100:8100/tcp -it --rm --gpus all intep/super-glue:1.0
du -h --threshold=100M
```
