# Extract: manual verification

## Setup
- Copy `.env.example` to `.env` and set `OPENWEATHER_API_KEY` (never commit `.env`).

## Automated tests
- Run `pytest services/pipeline/tests/extract -v`
- Result: 13 passed, 7 xfailed (xfail = known gaps listed below).

## Live check
- Date run: 2026-10-14
- City: Washington, DC (38.9, -77.04)
- Range: last 24 hours
- Status code: 200
- Records returned: 24
- All fields present (dt, main.aqi, 8 components): yes
- Sample: `docs/samples/air_sample.json` (2 records, no key)

## Findings
- `coord` is returned as an object (`{lon, lat}`), but the contract defines `list[float]`.
- `City` has no lat/lon range check or START < END check.
- Extract has no clear error for a missing API key.
- A missing `list` key raises a raw `KeyError`.
- `gold_example` in `data-contracts/schemas.py` was missing `no2`, so importing the schema raised a ValidationError; fixed in this PR (added `no2=0.5`).
- `test_extract.py` patch target pointed at a renamed module; fixed in this PR.