curl --parallel --parallel-immediate --parallel-max 3 --config async_request.txt

# This script executes asynchronous HTTP requests using curl with parallel options.
# With this specific curl it launches multiple HTTP requests in parallel according to the configuration specified in async_request.txt.
# The request its basically a GET directed to the endpoints specified in async_request.txt.