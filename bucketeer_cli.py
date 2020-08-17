#!/usr/bin/env python

import logging
import pathlib
import pkg_resources
import random
import sys

from bs4 import BeautifulSoup
import click
import requests


@click.command()
@click.argument("src", nargs=-1)
@click.option(
    "--server",
    default="https://bucketeer.library.ucla.edu",
    show_default=True,
    help="URL of the Bucketeer service",
)
@click.option("--failures-only", is_flag=True, help="Process previous failures only")
@click.option("--slack-handle", required=True, help="Slack handle of the user")
@click.option(
    "--loglevel",
    type=click.Choice(["INFO", "DEBUG", "ERROR"]),
    default="INFO",
    show_default=True,
)
@click.option("--version", "-V", is_flag=True, help="Print the version number and exit")
def cli(src, server, failures_only, slack_handle, loglevel, version):
    """Uploads CSV files to the Bucketeer service for processing.

    Arguments:

        SRC is either a path to a CSV file or a Unix-style glob like '*.csv'.
    """
    bucketeer_cli_version = pkg_resources.require("bucketeer_cli")[0].version
    user_agent = "{}/{}".format("Bucketeer CLI", bucketeer_cli_version)
    user_agent_human_readable = "{} v{}".format("Bucketeer CLI", bucketeer_cli_version)

    if version:
        click.echo(user_agent_human_readable)
        sys.exit(0)
    elif len(src) is 0:
        click.echo("Please provide one or more CSV files", err=True)
        sys.exit(1)

    # Logging setup.
    logging.basicConfig(
        filename="bucketeer_cli.log",
        filemode="a",
        level=loglevel,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%b-%d %H:%M:%S %p (%Z)",
    )
    extra_satisfaction = ["🎉", "🎊", "✨", "💯", "😎", "✔️ ", "👍"]

    logging.info("--- START ---")
    logging.info(
        "{}, sending batch job requests to {}".format(user_agent_human_readable, server)
    )

    # HTTP request URLs.
    get_status_url = server + "/status"
    post_csv_url = server + "/batch/input/csv"

    # HTTP request headers.
    request_headers = {"User-Agent": user_agent}

    # Make sure the Bucketeer service is up.
    try:
        status_response = requests.get(get_status_url, headers=request_headers)
        status_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_msg = "Bucketeer service unavailable: {}".format(str(e))
        click.echo(error_msg, err=True)
        logging.error(error_msg)
        sys.exit(1)

    for pathstring in src:
        csv_filepath = pathlib.Path(pathstring)
        csv_filename = csv_filepath.name

        if not csv_filepath.exists():
            error_msg = "File '{}' does not exist, skipping".format(csv_filename)
            click.echo(error_msg, err=True)
            logging.error(error_msg)

        # Only works with CSV files that have the proper extension.
        elif csv_filepath.suffix == ".csv":
            # Upload the file.
            files = {
                "file": (
                    pathstring,
                    open(pathstring, "rb"),
                    "text/csv",
                    {"Expires": "0"},
                )
            }
            form_data = [("failures", failures_only), ("slack-handle", slack_handle)]
            post_csv_response = requests.post(
                post_csv_url, headers=request_headers, files=files, data=form_data
            )

            # Handle the response.form_data
            if post_csv_response.status_code is 200:
                # Send an awesome message to the user.
                info_msg = "SUCCESS! CSV {} accepted for processing. You will be notified in Slack when it's done.".format(
                    csv_filename
                )
                border_char = extra_satisfaction[
                    random.randint(0, len(extra_satisfaction) - 1)
                ]
                border_length = 2 + (88 + len(csv_filename)) // 2

                click.echo(border_char * border_length)
                click.echo("{} {} {}".format(border_char, info_msg, border_char))
                click.echo(border_char * border_length)
                logging.info(info_msg)
            else:
                error_cause = (
                    BeautifulSoup(post_csv_response.text, features="html.parser")
                    .find(id="error-message")
                    .string
                )
                error_msg = "Failed to enqueue {}: {} (HTTP {})".format(
                    csv_filename, error_cause, post_csv_response.status_code
                )
                click.echo(error_msg, err=True)
                logging.error(error_msg)
        else:
            error_msg = "File '{}' does not have a '.csv' filename extension, skipping".format(
                csv_filename
            )
            click.echo(error_msg, err=True)
            logging.error(error_msg)

    logging.info("---- END ----")
