import logging

from uvicorn import run as uvicorn_run
from fastapi import FastAPI
from argparse import ArgumentParser

from routes.calc import calc_route

app = FastAPI()

app.include_router(calc_route)


def execute_server_core(arg_host: str, arg_port: int):
    try:
        uvicorn_run(app, host=arg_host, port=arg_port)
    except KeyboardInterrupt:
        logging.warning("Web Site Service stopped working")
    except Exception as e:
        logging.exception(e)


def setup_parser() -> (str, int):
    parser = ArgumentParser(description="Run the FastAPI server.")
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host for the server (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the server (default: 8000)",
    )
    args = parser.parse_args()
    return args.host, args.port


if __name__ == "__main__":
    host, port = setup_parser()
    execute_server_core(host, port)
