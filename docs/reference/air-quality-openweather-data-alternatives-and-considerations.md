# Air Quality OpenWeather Data Alternatives and Considerations

## Executive summary

**Choose OpenAQ for the main batch pipeline.** Its monitoring data and public file archive support incremental loads, backfills and quality checks. Choose **Open-Meteo** for the easiest MVP, or keep **OpenWeather** to minimize changes. For a U.S. project, **AirNow + AQS** is the strongest combination.

The goal is an autonomous, reliable cloud pipeline with $0 data-access cost. Free sources help; compute, storage and scheduling still need a separate free-tier plan.

## Summary table

| Option | Coverage / data | Access and cost | Best fit |
|---|---|---|---|
| OpenWeather | Global; current, forecast, history | API key; free tier | Keep the existing integration |
| OpenAQ | Global monitoring locations; freshness varies | API key or public S3 files; free access | **Best single source for batch ETL** |
| Open-Meteo | Global; CAMS model forecasts | No key; free non-commercial tier | **Fastest MVP** |
| AirNow | Mainly North America; recent observations and AQI | Account/API key or file products; free public access | Current U.S. dashboard |
| EPA AQS | U.S.; historical monitoring data | Email + API key or bulk CSV; free | Historical analysis |
| **OpenAQ + Open-Meteo** | Observations + model forecasts | Both free within applicable terms/limits | Global observation/forecast comparison |
| **AirNow + AQS** | Recent + authoritative historical U.S. data | Both free | U.S. pipeline with two data layers |

## Recommendations

1. **Default: OpenAQ.** Start with a few locations and PM2.5; use its archive for scheduled batch ingestion.
2. **Fast delivery: Open-Meteo or existing OpenWeather.** Prioritize getting scheduling, retries and monitoring working.
3. **Best U.S. combination: AirNow + AQS.** Add historical validation after the recent-data pipeline works.
4. **Best global combination: OpenAQ + Open-Meteo.** Add forecasts once observational ingestion is stable.

## Single-source options

### OpenWeather — existing baseline

Global coordinate-based concentrations, a four-day hourly forecast and history from November 2020. [API documentation](https://openweathermap.org/api/air-pollution).

- **Pros:** Simple JSON; broad pollutant coverage; minimal migration work.
- **Cons:** Limited station/measurement provenance; its 1–5 AQI scale differs from U.S. AQI.
- **Access/cost:** Account and API key. [Free tier](https://openweathermap.org/price): 60 calls/minute and 1 million/month; paid plans for more capacity.

### OpenAQ — recommended primary source

Aggregates measurements from identifiable monitoring locations worldwide. [API overview](https://docs.openaq.org/about/about).

- **Pros:** Station/sensor metadata; realistic ETL challenges; partitioned, compressed CSV archive.
- **Cons:** Uneven coverage and upstream quality; archive files arrive about 72 hours after each local day and may be revised.
- **Access/cost:** [Free API](https://docs.openaq.org/using-the-api/rate-limits): key, 60 requests/minute and 2,000/hour; higher limits paid. [Public S3 archive](https://docs.openaq.org/aws/about) also supports [credential-free downloads](https://docs.openaq.org/aws/quick-start).

### Open-Meteo — easiest alternative

Serves CAMS model-based air-quality forecasts for coordinates worldwide. [API documentation](https://open-meteo.com/en/docs/air-quality-api).

- **Pros:** No signup/key; simple JSON; pollutant concentrations and U.S./European AQI.
- **Cons:** Model estimates can miss local pollution; no free-tier uptime guarantee.
- **Access/cost:** [Free for non-commercial use](https://open-meteo.com/en/pricing), up to 10,000 calls/day and 300,000/month, with shorter-period limits. Commercial API use requires payment.

### AirNow — recent U.S. air quality

Provides preliminary observations, AQI and forecasts. [Documentation](https://docs.airnowapi.org/).

- **Pros:** Timely public-facing AQI; hourly updates; nationwide files suit batch ingestion.
- **Cons:** Preliminary data; geographically limited; unsuitable for regulatory trend analysis.
- **Access/cost:** Free public account/API key; endpoint-specific limits. Prefer [file products for bulk ingestion](https://docs.airnowapi.org/faq).

### EPA AQS — historical U.S. air quality

Authoritative monitoring records with site, method and quality metadata. [Documentation](https://aqs.epa.gov/aqsweb/documents/data_api.html).

- **Pros:** Strong provenance; detailed historical analysis and backfills.
- **Cons:** Availability can lag six months or more; complex codes/schema.
- **Access/cost:** Free email registration/API key or [bulk CSV](https://aqs.epa.gov/aqsweb/airdata/download_files.html). API: at most 10 requests/minute; EPA requests five-second pauses.

## Two best combinations

### OpenAQ + Open-Meteo — observations and forecasts

Use OpenAQ for measurements and Open-Meteo for forecasts at matching coordinates.

**Pros:** Useful global comparison; demonstrates multi-source ingestion. **Cons:** Requires aligning units, times and locations; grid estimates and station readings are different quantities. Store forecast issue time for later evaluation.

### AirNow + AQS — recent and historical U.S. data

Use AirNow for recent conditions and AQS for authoritative historical analysis.

**Pros:** Covers freshness and historical rigor. **Cons:** Station identifiers, methods and averaging periods may differ. Keep source/validation labels; reconcile only compatible records rather than automatically replacing AirNow values.

*Official access/pricing documentation checked October 8, 2026.*

