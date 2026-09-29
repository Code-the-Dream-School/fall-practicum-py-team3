# Sprint 2: Choose an API Direction and Build the Extract Layer

Welcome to **Sprint 2**!

This sprint is about understanding OpenWeather's free-access APIs, choosing the data your team wants to emphasize, and building the first working version of the extract layer. Your API choice will shape the questions your dashboard answers later in the practicum.

By the end of Sprint 2, your team should be able to explain:

- which API is the team's primary data source and why
- what the dashboard will emphasize based on that choice
- which endpoint, parameters, and credentials the extract layer needs
- what fields are present in the chosen API response
- how location input becomes valid request parameters
- how the extract layer behaves when inputs or API responses are invalid

> **Food for thought:** Data security is not the focus of this practicum, but API keys should still be treated as secrets. Your team may share one key or use one key per student; either way, keep real keys out of the repository by using environment variables or a local `.env` file included in `.gitignore`. Larger organizations use more formal processes to manage credentials across many internal and external services, which could be an optional topic to explore later in the practicum. For a simple introduction, review the [`python-dotenv` Getting Started guide](https://bbc2.github.io/python-dotenv/#getting-started). If a real key is ever committed, revoke it and generate a replacement.

## Explore the API with Postman

Postman lets you send an API request and inspect its JSON response before writing the same request in Python. Use the [Postman Installation & Usage Guide](../collaboration/Postman%20Installation%20%26%20Usage%20Guide.pdf) in this repository to get started.

## Start with the OpenWeather overview

Read the [OpenWeather API overview](../reference/openweather_api_overview.md) before implementing the extract client. It explains which free-access APIs are in scope, how the available APIs can support different dashboard goals, and which APIs are supplementary.

> **No payment is required for this practicum.** The APIs listed in the overview work with OpenWeather's free-access API key. If the website asks for credit-card information, stop—you do not need to subscribe to One Call or another paid product—and ask your mentor for help if needed.

## The team pivot point

Choose one primary direction as a team:

- **Current weather:** emphasize present conditions and comparisons across cities.
- **Weather forecast:** emphasize how conditions are expected to change over the next five days.
- **Air pollution — recommended:** emphasize air quality, pollutant concentrations, and changes across locations or time.

Air pollution is recommended because the original curriculum and reference materials were built around it, but it is not required. Record the team's choice and explain what that choice means for the future dashboard.

Focus on one primary API. Add a second data or supplementary API—Weather Maps, Geocoding, or Weather Stations—only when it directly supports the team's goal and the team can complete the primary extraction path first. During the core practicum, avoid taking on more than two API integrations.

## Sprint 2 scope

This sprint focuses on **extracting data**, not storing it. Your team should identify the response fields that later parts of the application will probably need, but you do not need to design final database tables, select PostgreSQL column types, write migrations, or create a complete data schema yet.

Sprint 3 will bridge the extract output into the later data work. The fuller schema and data-model decisions will be handled in Sprint 4, after the team has seen real API responses and understands their shape.

## Sprint 2 deliverables

### 1. API direction and extraction plan — 3 points

Create a short team decision note that documents:

- the primary API the team selected
- why it supports the team's dashboard goal
- any optional second or supplementary API the team may use
- the endpoint and required request parameters
- how the API key will be supplied safely
- the response fields the project expects to use and why
- common API errors or limits the extract layer should anticipate

Include a trimmed example response. This is an API exploration artifact, not a final database schema.

### 2. Location input and validation — 3 points

Update the location input contract from Sprint 1 and turn it into working code. The extract layer should be able to:

- find and read the configured location input
- return records in a predictable Python structure
- validate the fields required by the chosen API
- skip or clearly report missing and invalid required values

The team may provide latitude and longitude directly or choose the Geocoding API to convert place names into coordinates. Geocoding is not required when the input already provides the location values needed by the primary API.

Include focused tests for valid input, missing required values, and an empty or missing input source.

### 3. Primary API extract client — 5 points

Create a small client or function for the team's chosen primary API. It should:

- accept a validated location and any other required request options
- keep authentication and request code in one testable boundary
- return the raw API response without transforming its data fields
- handle empty results and unsuccessful responses clearly
- support mocked responses so tests do not repeatedly call the live API

### 4. Raw response contract and sample — 3 points

Document and demonstrate what the extract layer returns. Keep enough context with the raw response for later work, such as:

- the source location
- the API and endpoint used
- the request time or forecast window, when applicable
- when the response was retrieved
- the raw OpenWeather payload

Identify the response fields that appear important to the future dashboard, but do not design the final storage schema yet.

Use this contract as the Sprint 3 handoff by noting what a later storage layer will need to accept and which questions remain unanswered.

### 5. Extract tests and verification notes — 3 points

Add automated tests with mocked API responses, plus any short manual verification notes needed to demonstrate the extract flow. Cover at least:

- one successful location-to-data flow
- an invalid location input
- an empty, unsuccessful, or malformed API response
- a missing API key or configuration value

If the team makes a live test request, record the result without committing the API key or an unnecessarily large response file.

### Optional: Second API integration — 5 points

After the primary extraction path works and has tests, the team may integrate one additional API from the overview. Explain how it supports the dashboard goal and add appropriate error handling, mocked tests, and documentation.

Do not add a second API only because it is available. A smaller, reliable project is better than several incomplete integrations.

## What to turn in

By the end of Sprint 2, submit:

1. The API direction and extraction plan.
2. The location input and validation implementation.
3. The primary API extract client.
4. The raw response contract, sample, and Sprint 3 handoff.
5. The extract tests and verification notes.
6. If completed, the optional second API integration.

**Total: 17 core story points, or 22 with the optional second API integration**

## End-of-sprint checkpoint

Before closing Sprint 2, mentors should review the team's project documents with the entire group. Use this same checkpoint at the end of every future sprint.

1. **Revisit earlier decisions.** Review every Sprint 1 deliverable and identify assumptions that changed during Sprint 2.
2. **Update the diagrams.** Revise the architecture and process flow diagrams to reflect the selected API, location-input approach, extract flow, optional supporting API, and expected downstream handoff.
3. **Maintain the other working documents.** Update the product and pipeline summary, location-input contract, team working agreement, and any other project documentation that no longer reflects how the team is working or what it is building.
4. **Reflect on the team process.** Discuss what the practice PRs, reviews, meetings, communication, and blocker-handling revealed. Adjust the working agreement when the team finds a better way to collaborate.
5. **Confirm shared understanding.** Every team member—not only the team lead or document author—should review the updated materials, be comfortable with their contents, understand the current direction, and agree that they represent the team's decisions.
6. **Record the updates.** Include documentation changes in a reviewed PR and summarize important decisions in the next sprint handoff.

These are living documents, not one-time submissions. As the project changes, the documentation should change with it.
