# Python web app

FastAPI + Authlib + TailwindCSS

## Install

```bash
$ python -m venv .venv/
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp .env.sample .env
$ cd styles/ && pnpm install
```

## Run

* Start app:

    ```bash
    $ make
    ```

## Dev

* Build & watch python app:

    ```bash
    $ make dev
    ```

* Build & watch CSS styles:

    ```bash
    $ make css
    ```

* Format python code

    ```bash
    $ make fmt
    ```
