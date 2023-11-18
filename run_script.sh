python src/async_url_downloads.py > results/single_run_results.txt
{ time python -c "from src.async_url_downloads import *; urls = ['https://jsonplaceholder.typicode.com/todos/1'] * 50; sequential_downloads(urls)" ; } 2> results/multi_run_results_sequential.txt
{ time python -c "from src.async_url_downloads import *; urls = ['https://jsonplaceholder.typicode.com/todos/1'] * 50; asynchronous_downloads(urls)" ; } 2> results/multi_run_results_asynchronous.txt
