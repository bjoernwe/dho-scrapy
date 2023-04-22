Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Set up your environment. You can use .envrc if you have direnv installed
```bash
export REDDIT_CLIENT_ID="abc"
export REDDIT_CLIENT_SECRET="def"
export REDDIT_USERNAME="username"
export REDDIT_PASSWORD="password"

export PGUSER="user"
export PGPASSWORD="password"
export PGHOST="localhost"
export PGPORT="5432"
export PGDATABASE="reddit"
```

Run database migrations:
```bash
export DB_TMP=$PGDATABASE
PGDATABASE="" psql -c "CREATE DATABASE $DB_TMP"
psql -f migrations/1_posts.sql
```

Then you can run the script
```bash
python main.py streamentry
```

## Local Postgres
```bash
docker pull postgres:14.2
docker run --rm --name reddit-pg-docker \
  -e POSTGRES_PASSWORD=docker \
  -d -p 5432:5432 \
  postgres:14.2

export PGUSER=postgres
export PGPASSWORD=docker
export PGDB=reddit
export PGHOST=localhost
export PGPORT=5432
```
