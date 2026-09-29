# What A Data Pipeline Is And Why It Exists

## Purpose

This document explains, in plain language, what a data pipeline is and why teams build one.

It also connects the idea to this repository so contributors can see how the concept maps to the City Air Tracker project.

## What is a data pipeline?

A data pipeline is a repeatable process that moves data from one place to another while preparing it for use.

In most projects, a pipeline does more than copy files. It usually:

1. collects data from a source
2. cleans or reshapes the data
3. stores the result in a format that people or applications can use

The key idea is automation. Instead of manually downloading data, editing it, and uploading it somewhere else every time, the pipeline performs the same steps in a consistent way.

## Why a data pipeline is useful

Teams build data pipelines to solve a few common problems.

### 1. Raw source data is rarely ready to use

APIs, CSV files, and logs often come in formats that are inconsistent, noisy, or hard to analyze directly.

A pipeline can:

- rename fields
- standardize timestamps
- remove duplicates
- fill in derived values
- validate required columns

This makes the final dataset easier for dashboards, reports, and downstream systems to trust.

### 2. Repeating manual work does not scale

If a person has to run the same data steps every day, mistakes become more likely and progress becomes slower.

A pipeline makes the process repeatable so the same inputs produce the same kind of outputs.

### 3. Different parts of a system need different versions of the data

Teams often keep:

- raw data for traceability
- cleaned data for analysis
- published data for dashboards or applications

A pipeline helps maintain those layers in a clear order.

### 4. Reliability matters

Good pipelines make it easier to:

- retry failed steps
- log what happened
- inspect intermediate outputs
- test transformations
- detect schema or data-quality problems early

## Common stages of a data pipeline

Many pipelines follow an ETL or ELT pattern.

### Extract

Extract means collecting data from the source system.

Examples:

- calling an external API
- reading a CSV file
- loading data from cloud storage
- consuming application logs

### Transform

Transform means changing the data into a more useful structure.

Examples:

- converting timestamps into a standard timezone
- flattening nested JSON
- calculating new metrics
- filtering invalid rows
- combining data from multiple sources

### Load

Load means writing the prepared result to a destination.

Examples:

- saving Parquet files
- loading a database table
- publishing a dataset for a dashboard

## What a pipeline is not

A data pipeline is not automatically a machine learning system, a dashboard, or a database.

Those tools may use the pipeline's output, but the pipeline itself is the process that prepares and moves the data.

## How this applies to City Air Tracker

This repository is a small example of a batch data pipeline.

At a high level, City Air Tracker:

1. reads a list of cities from configuration
2. geocodes those cities through the OpenWeather API
3. downloads historical air pollution data
4. stores the raw responses
5. transforms the raw data into a cleaner analytical dataset
6. writes the final gold dataset for the dashboard

That means the project already follows the standard pipeline pattern:

- Extract: geocoding and air-pollution API calls
- Transform: parsing, deduplication, timestamp normalization, derived metrics
- Load: writing the gold dataset for downstream use

## Why this project uses a pipeline

City Air Tracker uses a pipeline because the dashboard should not have to solve data collection and cleanup on every page load.

Separating the pipeline from the dashboard gives a few benefits:

- API calls happen in one place instead of inside the UI
- raw responses can be cached and inspected later
- data cleanup rules are centralized
- the dashboard can read a prepared dataset instead of rebuilding it live
- contributors can test pipeline logic separately from dashboard behavior

## A simple mental model

You can think of a data pipeline like a kitchen prep workflow.

- raw ingredients arrive from suppliers
- the kitchen washes, cuts, and combines them
- the final dishes are plated for serving

In the same way:

- source systems provide raw data
- the pipeline cleans and shapes it
- applications consume the prepared result

## What contributors should keep in mind

When working on pipeline code, ask:

- Where does the data come from?
- What assumptions are we making about its shape?
- How do we handle bad or missing data?
- What output do downstream consumers depend on?
- How will we verify the pipeline still works after a change?

These questions help keep the pipeline reliable and easier to maintain.
