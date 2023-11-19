#! /usr/bin/env python3

import csv
import time
import asyncio
import aiohttp
import requests
from typing import Callable, Any


async def request_url_response_content(
    session: aiohttp.ClientSession, url: str) -> bytearray:
    """
    Asynchronously download URL response content
    If response is invalid, return empty result
    """
    async with session.get(url) as response:
        if response.ok:
            b_array = bytearray()
            while True:
                chunk = await response.content.read(1024)
                b_array.extend(chunk)
                if not chunk:
                    break
            return b_array
        else:
            return bytearray()


async def request_url_response_json(
    session: aiohttp.ClientSession, url: str) -> dict[Any, Any]:
    """
    Asynchronously download URL response content as JSON
    If response is invalid, return empty result
    """
    async with session.get(url) as response:
        if response.ok:
            response_json = await response.json()
            return response_json
        else:
            return {}


async def request_url_csv_list(
    session: aiohttp.ClientSession, url: str, delimiter: str=','
    ) -> list[list[str]]:
    """
    Asynchronously download 'csv'-formatted text and return as list of lists 
        where nested lists represent each row of the 'csv' file
    If response is invalid, return empty result
    """

    async with session.get(url) as response:

        if response.ok:

            b_array = bytearray()
            while True:
                chunk = await response.content.read(1024)
                b_array.extend(chunk)
                if not chunk:
                    break

            decoded_content = b_array.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=delimiter)
            cr_list = list(cr)

            return cr_list 

        else:

            return [['']]


async def request_url_responses(
    urls: list[str], request_url: Callable, *args, **kwargs) -> list:
    """
    Returns asynchronously-downloaded URL responses 
    Accepts 'request_url' as a function that asynchronously downloads and 
        processes a single URL
    """

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(request_url(session, url, *args, **kwargs)) 
            for url in urls]
        results = await asyncio.gather(*tasks)

    return results


def sequential_downloads(urls: list[str]) -> list[bytearray]:
    """
    Sequentially download a series of URLs
    """

    downloads = []
    for url in urls:
        with requests.Session() as s:
            with s.get(url) as response:
                if response.ok:
                    downloads.append(bytearray(response.content))

    return downloads


def asynchronous_downloads(urls: list[str]) -> list[bytearray]:
    """
    Asynchronously download a series of URLs
    """

    downloads = asyncio.run(
        request_url_responses(urls, request_url_response_content))

    return downloads


def main():
    """
    Compare sequential and asynchronous download speeds of a batch of URLs
    """

    urls = ['https://jsonplaceholder.typicode.com/todos/1'] * 50

    start_time = time.time()
    downloads01 = sequential_downloads(urls)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time for sequential downloads: {elapsed_time} seconds')

    start_time = time.time()
    downloads02 = asynchronous_downloads(urls)
    elapsed_time = time.time() - start_time
    print(f'Elapsed time for asynchronous downloads: {elapsed_time} seconds')

    print('\n')
    print(f'Sequential downloads, first item:\n{downloads01[0]}')
    print('\n')
    print(f'Asynchronous downloads, first item:\n{downloads02[0]}')
    print('\n')
    if downloads01 == downloads02:
        print('Both sets of downloads are identical')
    else:
        print('The two sets of downloads are not identical')


if __name__ == '__main__':
    main()
