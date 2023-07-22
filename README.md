# Digest Compilator

micro service that compiles a digest of posts

## How To Run
1. Create a `.env` file as in the [example](./.env.example).

2. Run the command:

    ```
    docker run ghcr.io/nikuma0/digestcompilator:latest --env_file=.env
    ```

You can also use `docker-compose`. The `infra` directory has some usage examples.


## Developing
1. Create a `.env` file as in the [example](./.env.example).
2. Install packages using `poetry`

    ```
    poetry install
    poetry shell
    ```

3. You can use `docker-pg.yml` to access postgres.

    ```
    docker compose -f infra/docker-pg.yml up -d
    ```

4. Run it:

    ```
    uvicorn app.main:init_app --factory
    ```
