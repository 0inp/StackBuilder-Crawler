# Table of contents

1. [Introduction](#introduction)
2. [Clean Architecture](#clean_architecture)
3. [CLI Controller](#cli_controller)
4. [Crawler Adapter](#crawler_adapter)

## Introduction <a name="introduction"></a>

This is the Architecture Design Record.

## Clean Architecture <a name="clean_architecture"></a>

In the context of the test for the Stack Builders job application,
I had to create an application that crawls the website HackerNews.
I decided to use the clean architecture because of the flexibility provided
to the implementation.
This comes with a cost in the beginning, but allow me to choose what I want for the entrypoints or the way of crawling

## CLI controller <a name="cli_controller"></a>

I choose to implement first a CLI entrypoint since it seems the easier
and faster to implement.

## Crawler Adapter <a name="crawler_adapter"></a>

I choose to implement fisrt the crawler adapter because
the description of the test mentionned explictly to do a crawler.
