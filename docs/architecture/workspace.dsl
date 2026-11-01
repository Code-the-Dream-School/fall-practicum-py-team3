/*
 * City Air Tracker — C4 model (PLAN, subject to change).
 * Source of truth for all architecture diagrams. Render with ./render.sh.
 * Elements tagged "Proposed" are not agreed yet (see docs/adr/0001-use-jev-for-insights.md).
 * Terms follow CONTEXT.md.
 */
workspace "City Air Tracker" "Compares air quality across U.S. cities and Census Divisions from November 2020 onward." {

    model {
        viewer = person "Dashboard Viewer" "Anyone comparing air quality across Tracked Cities and Divisions."
        team = person "Project Team" "fall26-py-team3, as operators: edit the city list, run Backfill Runs, watch Pipeline Runs."

        openWeather = softwareSystem "OpenWeather Air Pollution API" "Modelled hourly air pollution history per coordinate, from Nov 2020." "External"
        aiMlApi = softwareSystem "AI/ML API" "[Proposed] Hosted model API for the LLM Enrichment stage. Serves TypeSafe Jev (typed judgments: choice, score, yes/no) and gpt-4o-mini (Insight text)." "External,Proposed"

        cat = softwareSystem "City Air Tracker" "Collects daily air quality for 33 Tracked Cities and explains it on a dashboard." {
            citiesFile = container "City Configuration" "33 Tracked Cities: name, state, Division, lat/lon, timezone, 2020 metro population." "YAML in Git (config/cities.yaml)" "File"

            pipeline = container "Pipeline" "Stage functions plus thin entry points. Stages never depend on the caller." "Python 3.12, Pydantic, pandas" {
                prefectFlow = component "Prefect Flow" "Local entry point for Backfill and Incremental Runs. Retries network steps only." "Prefect @flow"
                ingestHandler = component "Ingest Handler" "AWS entry point for the daily Incremental Run." "AWS Lambda handler"
                llmEnrichmentHandler = component "LLM Enrichment Handler" "[Proposed] AWS entry point for the LLM Enrichment stage: builds missing Insights." "AWS Lambda handler" "Proposed"
                runTracker = component "Run Tracker" "Opens and closes a Pipeline Run with trigger, mode, status and counts." "Python"

                cityConfig = component "City Config Loader" "Loads and validates Tracked Cities; syncs them to tracked_cities." "Python, Pydantic, PyYAML"
                extract = component "extract()" "Calls OpenWeather for one city and window. Returns the Raw Response unchanged." "Python, requests"
                loadRaw = component "load_raw()" "Idempotent write of Raw Responses." "Python, psycopg"
                transform = component "transform()" "Raw Responses to hourly gold rows (UTC): AQI Level, category, score, rolling aqi_24h_avg, 8 pollutants. Rejects responses with missing required fields." "Python, pandas"
                lookups = component "AQI and Health Tip Lookup" "AQI Level labels, pollutant units, EPA-based Health Tips." "Python constants"
                loadGold = component "load_gold()" "Idempotent upsert of hourly gold rows on (city, timestamp)." "Python, psycopg"

                insightFacts = component "Insight Facts Builder" "[Proposed] Computes facts per Tracked City month from hourly gold: coverage, pollutant means, worst AQI Level, AQI Level shares, year-over-year change, z-scores. Skips incomplete months and months under 75% coverage." "Python, pandas" "Proposed"
                jevJudge = component "Jev Judge" "[Proposed] Asks Jev (typesafe/jev-1.14) for getting_worse, pollution_profile and unusualness." "Python" "Proposed"
                insightWriter = component "Insight Writer" "[Proposed] Asks gpt-4o-mini for a 1-2 sentence Insight from facts and judgments; validates it, falls back to a fixed template, records model and prompt version, upserts insights as enriched, skipped or failed." "Python" "Proposed"
            }

            database = container "Database" "Tables: tracked_cities, raw_air_pollution (JSONB), gold_air_quality (hourly), insights, pipeline_runs. View: division_figures (population-weighted)." "Supabase (PostgreSQL)" "Database"

            dashboard = container "Dashboard" "City and Division views, AQI history, Health Tips, Insights, modelled-data notice." "Streamlit, Plotly" {
                cityView = component "City View" "Pick a Tracked City: latest AQI Level and Health Tip, pollutant history, Insights." "Streamlit page"
                divisionView = component "Division View" "Compare Divisions by Division Figures, with per-city values alongside." "Streamlit page"
                dataAccess = component "Data Access" "Read-only queries with caching; turns database errors into an error state." "Python, SQLAlchemy, st.cache_data"
                charts = component "Chart Builders" "Plotly figures for history and comparisons." "Python, Plotly"
                uiStates = component "UI States" "No data yet, loading, database error, modelled-data notice." "Streamlit"
            }
        }

        # L1
        viewer -> cat "Compares air quality across cities and Divisions"
        team -> cat "Configures cities, runs backfills, monitors runs"
        cat -> openWeather "Fetches hourly air pollution history" "HTTPS/JSON"
        cat -> aiMlApi "Asks Jev and gpt-4o-mini to build Insights" "HTTPS/JSON" "Proposed"

        # L2
        viewer -> dashboard "Picks a city or Division, reads charts and tips" "HTTPS"
        team -> citiesFile "Edits via pull request"
        team -> pipeline "Starts Backfill Runs locally"
        pipeline -> citiesFile "Reads Tracked Cities"
        pipeline -> openWeather "Fetches hourly history" "HTTPS/JSON"
        pipeline -> database "Writes Tracked Cities, Raw Responses, hourly gold, Insights, Pipeline Runs" "SQL"
        pipeline -> aiMlApi "Asks Jev and gpt-4o-mini" "HTTPS/JSON" "Proposed"
        dashboard -> database "Reads hourly gold, Division Figures, Insights (read-only user)" "SQL"

        # L3: dashboard
        viewer -> cityView "Picks a city"
        viewer -> divisionView "Compares Divisions"
        cityView -> dataAccess "Asks for city data"
        divisionView -> dataAccess "Asks for Division Figures"
        cityView -> charts "Builds charts"
        divisionView -> charts "Builds charts"
        cityView -> uiStates "Shows states and notice"
        divisionView -> uiStates "Shows states and notice"
        dataAccess -> database "Reads gold_air_quality, division_figures, insights" "SQL"

        # L3: entry points
        team -> prefectFlow "Starts Backfill or Incremental Run"
        prefectFlow -> runTracker "Opens and closes run"
        prefectFlow -> cityConfig "Loads cities"
        prefectFlow -> extract "Calls per city and window"
        prefectFlow -> loadRaw "Passes Raw Responses"
        prefectFlow -> transform "Passes Raw Responses"
        prefectFlow -> loadGold "Passes hourly gold rows"
        prefectFlow -> insightFacts "Runs LLM Enrichment stage" "" "Proposed"

        ingestHandler -> runTracker "Opens and closes run"
        ingestHandler -> cityConfig "Loads cities"
        ingestHandler -> extract "Calls per city and window"
        ingestHandler -> loadRaw "Passes Raw Responses"
        ingestHandler -> transform "Passes Raw Responses"
        ingestHandler -> loadGold "Passes hourly gold rows"

        llmEnrichmentHandler -> runTracker "Opens and closes run" "" "Proposed"
        llmEnrichmentHandler -> insightFacts "Runs LLM Enrichment stage" "" "Proposed"

        # L3: stages
        runTracker -> database "Writes pipeline_runs" "SQL"
        cityConfig -> citiesFile "Reads"
        cityConfig -> database "Upserts tracked_cities" "SQL"
        extract -> openWeather "GET /air_pollution/history" "HTTPS/JSON"
        loadRaw -> database "Upserts raw_air_pollution" "SQL"
        transform -> lookups "Uses labels, units, Health Tips"
        loadGold -> database "Upserts gold_air_quality" "SQL"
        insightFacts -> database "Reads hourly gold without an Insight" "SQL" "Proposed"
        insightFacts -> jevJudge "Passes computed facts" "" "Proposed"
        jevJudge -> aiMlApi "POST /v1/decisions (Jev)" "HTTPS/JSON" "Proposed"
        jevJudge -> insightWriter "Passes typed judgments" "" "Proposed"
        insightWriter -> aiMlApi "POST chat completions (gpt-4o-mini)" "HTTPS/JSON" "Proposed"
        insightWriter -> database "Upserts insights" "SQL" "Proposed"

        aws = deploymentEnvironment "AWS" {
            ingestGroup = deploymentGroup "Ingest"
            insightGroup = deploymentGroup "Insight"
            servingGroup = deploymentGroup "Serving"

            deploymentNode "GitHub" "Repository and CI." "GitHub" {
                repoMain = infrastructureNode "main branch" "Protected. Plan: require passing checks (not set up yet)." "Git"
                actions = infrastructureNode "GitHub Actions" "Tests, Jira title check, diagram rendering; SAM deploy later (Could)." "GitHub Actions"
            }

            deploymentNode "Amazon Web Services" "" "AWS" {
                deploymentNode "us-east-1 (placeholder)" "" "AWS Region, should match Supabase" {
                    scheduler = infrastructureNode "EventBridge Scheduler" "Daily ingest after the last city's local midnight (~10:00 UTC). Separate Insight schedule." "Amazon EventBridge"
                    ssm = infrastructureNode "SSM Parameter Store" "OpenWeather key, Supabase URL, AI/ML API key (SecureString)." "AWS SSM"
                    logs = infrastructureNode "CloudWatch" "Logs and failed-run alarm." "Amazon CloudWatch"
                    alerts = infrastructureNode "SNS Topic" "Failure and cost alerts to the team (Should)." "Amazon SNS"
                    budgets = infrastructureNode "AWS Budgets" "Monthly spend alarm." "AWS Budgets"

                    deploymentNode "Ingest Lambda" "" "AWS Lambda, Python 3.12, zip via SAM" {
                        ingestInstance = containerInstance pipeline ingestGroup
                        citiesInstance = containerInstance citiesFile ingestGroup
                    }
                    deploymentNode "Insight Lambda" "[Proposed]" "AWS Lambda, Python 3.12, zip via SAM" "Proposed" {
                        insightInstance = containerInstance pipeline insightGroup "Proposed"
                    }
                }
            }

            deploymentNode "Supabase" "" "Managed PostgreSQL" {
                containerInstance database ingestGroup,insightGroup,servingGroup
            }

            deploymentNode "Streamlit Community Cloud" "" "Free Streamlit hosting" {
                dashboardInstance = containerInstance dashboard servingGroup
            }

            deploymentNode "OpenWeather" "" "SaaS" {
                softwareSystemInstance openWeather ingestGroup
            }

            deploymentNode "AI/ML API" "[Proposed]" "SaaS" "Proposed" {
                softwareSystemInstance aiMlApi insightGroup "Proposed"
            }

            scheduler -> ingestInstance "Invokes daily"
            scheduler -> insightInstance "Invokes on its own schedule" "" "Proposed"
            ingestInstance -> ssm "Reads secrets"
            insightInstance -> ssm "Reads secrets" "" "Proposed"
            ingestInstance -> logs "Writes logs"
            insightInstance -> logs "Writes logs" "" "Proposed"
            logs -> alerts "Alarm on failed run"
            budgets -> alerts "Alarm on spend"
            repoMain -> dashboardInstance "Redeploys on merge"
            actions -> repoMain "Checks pull requests"
        }
    }

    views {
        systemContext cat "L1-SystemContext" "L1: who uses City Air Tracker and what it depends on." {
            include *
            autoLayout lr
        }

        container cat "L2-Containers" "L2: runnable parts and data stores." {
            include *
            autoLayout lr
        }

        component pipeline "L3-PipelineComponents" "L3: inside the Pipeline. Stages are plain functions; entry points only call them." {
            include *
            autoLayout lr
        }

        component dashboard "L3-DashboardComponents" "L3: inside the Dashboard. Pages only read through Data Access." {
            include *
            autoLayout lr
        }

        dynamic pipeline "Dynamic-DailyIncrementalRun" "One daily Incremental Run on AWS." {
            ingestHandler -> runTracker "Open Pipeline Run (trigger=schedule, mode=incremental)"
            runTracker -> database "Insert pipeline_runs row"
            ingestHandler -> cityConfig "Load 33 Tracked Cities"
            cityConfig -> citiesFile "Read"
            ingestHandler -> extract "Per city: window = yesterday in city local time"
            extract -> openWeather "GET /air_pollution/history"
            ingestHandler -> loadRaw "Raw Responses"
            loadRaw -> database "Upsert raw_air_pollution on (lat, lon, start, end)"
            ingestHandler -> transform "Raw Responses"
            transform -> lookups "AQI label and Health Tip"
            ingestHandler -> loadGold "Hourly gold rows"
            loadGold -> database "Upsert gold_air_quality on (city, timestamp)"
            ingestHandler -> runTracker "Close run: status and counts"
            runTracker -> database "Update pipeline_runs row"
            autoLayout lr
        }

        deployment cat aws "Deployment-AWS" "Eventual AWS deployment (sketch)." {
            include *
            autoLayout lr
        }

        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External" {
                background #6b6b6b
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
            element "Database" {
                shape Cylinder
            }
            element "File" {
                shape Folder
            }
            element "Proposed" {
                background #eeeeee
                color #555555
                stroke #888888
                border dashed
            }
            relationship "Relationship" {
                style solid
            }
            relationship "Proposed" {
                style dashed
                color #888888
            }
        }

        properties {
            "c4plantuml.tags" "true"
        }
    }

}
