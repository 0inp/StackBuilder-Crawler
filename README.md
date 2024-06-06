# StackBuilders Crawler

## Resume

This is the StackBuilders test for the application process.

## Architecture

We will use the clean architecture for this test. Here is the description:

### Entities

#### Entry

- number
- title
- number of points
- number of comments
- source

#### Log

- request timestamp
- applied filters

### Usecases

#### GetEntries

Get all the entries from one or more sources and apply filters.
Then log usage data
Inputs:

- sources: list(str)
- filters: list(str)

Outputs:

- Entries: list(Entry)

### Controllers

- CLI
- API(s)
  - FastAPI
  - GraphQL API

### Adapters

#### Logger

- Local File Storage (JSON or txt)
- DB Storage

#### Get Entries data

- Scrapping (BeautifullSoup or Scrappy)
- API (HackerNews API)
