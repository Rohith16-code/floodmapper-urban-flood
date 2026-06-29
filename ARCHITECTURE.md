# Architecture Overview

## Project: real-time-urban-flood-inundation-mapping

## Pattern
Not specified

## Summary
Urban flooding displaces millions annually, and city emergency managers lack real-time, street-level inundation maps during active flood events. Build a platform that fuses rainfall radar data, IoT water-level sensor streams, OpenStreetMap elevation profiles, and crowdsourced social media reports to generate a live flood depth map updated every 5 minutes. The system should auto-generate dynamic, f

## Technology Stack
- Python 3.11
- FastAPI
- SQLite
- HTML/JS

## Files to Create
- `[api]` `src/main.py` — Entry point with static frontend mount
- `[api]` `src/api/routes.py` — REST endpoints with standardized schemas
- `[frontend]` `static/index.html` — Modern responsive dashboard
- `[frontend]` `static/css/style.css` — Design system with CSS variables
- `[frontend]` `static/js/app.js` — Fetch-based frontend logic

## API Contracts
- `GET /api/v1/health` — Health check

## Data Models

## Frontend Pages
- `/dashboard` — Main dashboard — calls: GET /api/v1/health

## Compliance Requirements

## Performance Targets

## Risks

## Infrastructure