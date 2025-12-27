Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


Metric Instability in Real-Time Ticket Sales Pipelines
Overview

In real-time data systems, business metrics often change after they are first reported.
A dashboard queried today can show different numbers tomorrow — even for the same date.

This project demonstrates why metrics become unstable, how late and duplicate data cause drift, and how to design a pipeline that eventually stabilizes metrics.

The focus is data correctness over time, not just moving data through tools.

The Problem

Business users ask questions like:

“How many tickets were sold on December 20?”

In production systems:

Events arrive late

Streaming systems deliver data incrementally

Messages can be duplicated

Pipelines use at-least-once delivery guarantees

As a result:

Early metrics are incomplete

Numbers change retroactively

Dashboards lose trust

This project recreates that scenario end-to-end.

What This Project Shows
Late-Arriving Data

Ticket purchase events are ingested hours or days after purchase, simulating:

Network delays

Backlogs

Streaming retries

Duplicate Events

A small percentage of events are replayed with different ingestion timestamps, mimicking:

Kafka at-least-once delivery

Consumer restarts

Retry logic

Metric Instability

Metrics computed at different observation times produce different results for the same sale date.

Metric Stabilization

By:

Deduplicating on ticket_id

Using purchase_timestamp as event time

Separating raw, staging, and mart layers

Metrics eventually converge and stabilize.

Architecture
Python Producer
     ↓
Kafka (ticket_purchases_raw)
     ↓
Spark Structured Streaming
     ↓
Parquet (append-only, late + duplicate data)
     ↓
DuckDB (raw ingestion)
     ↓
dbt
  ├── staging (deduplication & cleaning)
  └── marts (business metrics)

Data Model (Core Fields)
Raw Events (raw.ticket_events)

ticket_id

match_id

purchase_timestamp

ingest_timestamp

ticket_type

quantity

price

This table intentionally contains:

Late arrivals

Duplicate records

Out-of-order ingestion

dbt Models
Staging: stg_ticket_purchases

Purpose:

Remove duplicates

Retain one canonical record per ticket

Logic:

ROW_NUMBER() OVER (
  PARTITION BY ticket_id
  ORDER BY purchase_timestamp, ingest_timestamp
)

Mart: fct_daily_sales

Purpose:

Produce stable, business-ready metrics

Metrics:

Tickets sold

Revenue

Quantity

Ticket type breakdown

Grouped by:

Sale date

Match

Teams

Stadium

Metric Instability Analysis

To demonstrate metric drift, the same sale date is observed at different ingestion times.

Example Output
Observation Time	Tickets Sold
T0 + 1 hour	183
T0 + 6 hours	1,076
T0 + 1 day	5,575
Final	7,285

The sale date never changes, but the metric grows as late data arrives.

This is exactly what happens in real dashboards queried too early.

Visualization

The project includes a plot showing how ticket counts for a single sale date evolve over time as more data is ingested.

Early queries undercount sales

Late data corrects the metric

Final numbers stabilize only after ingestion completes

(Generated from metric_instability.csv)

Why This Matters

This project highlights why production analytics systems must:

Separate event time from ingestion time

Expect duplicates in streaming systems

Avoid computing business metrics directly from raw streams

Use staging layers to enforce correctness

It explains why real-time does not mean correct-time.

Technology Stack

Python — data generation & Kafka producer

Kafka — event streaming

Apache Spark — structured streaming ingestion

Parquet — append-only storage

DuckDB — analytical database

dbt — transformations & metrics

Matplotlib — metric instability visualization