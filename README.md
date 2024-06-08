# StackBuilders Crawler

## Resume

This is the StackBuilders test for the application process.

## Usage

### Local Python/Poetry environment

If you have a working python/poetry environment:

```bash
poetry install
poetry run python main.py
```

If you want to know more about tests and coverage:

```bash
pytest --cov=src tests/
# OR
make test-cov
```

### Docker

If you want to use docker:

```bash
# Build the docker image
docker build -t sb-crawler --rm .
# OR
make docker-image

# Run the container
docker run -it --name sb-crawler-app --rm -v ./data:/app/data/ sb-crawler
# OR
make docker-run
```

Inside the container you can run the cli application

```bash
poetry run python main.py
```

For more information about the usage of the application:

```bash
python main.py --help
```

### Examples

```bash
# Simple mode. Will get all the entries from HackeNews.
python main.py
# Help.
python main.py --help
# Get entries and filter out the entries with more than or equal to 5 words in the title.
python main.py --filter number_of_words lt 5
# Order the entries with the number of comments from the entry with top comments to lowest one.
python main.py --order comments desc
# Will log some debug messages.
python main.py --verbose
# Will prefer to log in an SQLite DB.
python main.py --db-log
# To check the db.
python -m sqlite3 data/app.db
```

The log directory `data/*` will be also saved in your local environment
You can find in this file the logs of the usage of the application

### Exercise description

> Using the language that you feel most proficient in, create a web crawler
> using scraping techniques to extract the first 30 entries from [https://news.ycombinator.com/].
> You'll only care about the number, the title, the points, and the number of
> comments for each entry.
> From there, we want it to be able to perform a couple of filtering operations:
>
> - Filter all previous entries with more than five words in the title ordered by the number of comments first.
> - Filter all previous entries with less than or equal to five words in the title ordered by points.
>
> When counting words, consider only the spaced words and exclude any symbols.
> For instance, the phrase “This is - a self-explained example” should be
> counted as having 5 words.
> The solution should store usage data, including at least the request timestamp
> and a field to identify the applied filter. You are free to include any
> additional fields you deem relevant to track user interaction and crawler
> behavior. The chosen storage mechanism could be a database, cache, or any
> other suitable tool.
> To gain insight into your thought process, please consider including brief
> documentation explaining the key design decisions you made.
> This can be formatted in any way you find comfortable, such as an explanatory
> text file, markdown document, or comments within the code.
> While an Architectural Decision Record (ADR) format is certainly welcome,
> exploring alternative formats to explain your decisions is also encouraged.
> We will measure the performance of the provided solution and your ability to
> test the requested operations in the scenarios described above.
> In addition, we'd love to see the following in your code for extra points:
>
> - Good object-oriented/functional code
> - Avoiding repetition and favoring a consistent organization.
> - You should stick to the semantics of your chosen language and be as consistent as possible.
> - Correct usage of version control tools, with a good commit history and incremental software delivery practices.
> - Automated testing with any framework or tool of your choice.
> - We value candidates who love clean, well-structured code and who can creatively solve problems.
> - A README.md is always helpful in guiding us through your work.
>
> Please submit the result to a GitHub, GitLab, or Bitbucket repository and send us the URL within 72 hours. Once we receive this information, we'll ask our technical team to review it and let you know about the next steps of the process soon.

## Architecture

We will use the [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) for this test. Here is the description:

### Entities

#### Entry

- index
- title
- number of points
- number of comments
- source

#### Filter

- field (the field of the entry on which to do the filtering operation)
- operator (less than, greater than or equal, etc.)
- value

#### Order

- field (the field of the entry on which to do the ordering operation)
- direction (asc/desc)

#### Log

- request timestamp
- applied filters
- applied order

### Usecases

#### GetEntries

Get all the entries from one or more sources and apply filters.
Then log usage data
Inputs:

- source: str
- filter: FilterEntity

Outputs:

- Entries: list(Entry)

### Controllers

- CLI
- API(s) (TODO)
  - FastAPI
  - GraphQLAPI

### Adapters

#### Logger

- Local File Storage (JSON or txt)
- DB Storage (TODO)

#### Get Entries data

- Scrapping (BeautifullSoup)
- API (HackerNews API) (TODO)

## ADR

see documentation [here](adr/adr.md)

```

```
