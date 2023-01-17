# SHEET DATA
This API pulls data from a Google Sheet. Supports pagination and caching.

## Running the Server

Docker needs to be installed to run the server.

    docker-compose up -d

The server should be accessible on `http://localhost:8000`

## Running Test

    docker-compose run --rm web pytest

## Endpoint

`http://localhost:8000/data`
    
### Query Parameters

`http://localhost:8000/data?nocache=1&page=1&page_size=5`

- `nocache`: By default the csv response from the is saved and subsequent request are from the saved csv. This query param instruct the server not to cache the response, that is, fetch the sheet on each request. This is useful for when the data on the Google Sheet changes
- `page`: For pagination. Break the data into pages by `page_size` 
- `page_size`: Number of items on a page.


