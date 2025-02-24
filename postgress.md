
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: my_postgres
    restart: always
    environment:
      POSTGRES_DB: my_database
      POSTGRES_USER: my_user
      POSTGRES_PASSWORD: my_password
      POSTGRES_INITDB_ARGS: "--data-checksums --wal_level=logical"
      PGDATA: /var/lib/postgresql/data/pgdata
      POSTGRES_INITDB_WALDIR: /var/lib/postgresql/data/wal
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

