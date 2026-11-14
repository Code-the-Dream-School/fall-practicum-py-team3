This branch adds insight to the dashboard.

Data pulled from insight includes:

City (in drop down)
Dates
AQI
Category

To run Streamlit locally use:
streamlit run services/pipeline/src/pipeline/dashboard/dashboard_app.py

SQL script for timeouts in Supabase:

alter role service_role set statement_timeout = '60s';
NOTIFY pgrst, 'reload config';

If all the cities don’t load on your end, increase the max rows in Supabase (Project Settings → Data API → Settings (tab in Data API)).