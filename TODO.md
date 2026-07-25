# Implementation Plan - Multi-JD Support

## Steps

- [x] Read and understand all relevant files
- [x] Convert `user_jd` from single value to list in `handlers.py`
- [x] Update `/jd` command to initialize empty list
- [x] Update `receive_resume()` JD upload section to append to list
- [x] Update `/done` command to show both resumes and JDs
- [x] Update `/analyze` to iterate over all JDs and take best score per resume
- [x] Update `analysis_results["jd"]` to store list of JD dicts
- [x] Update `backend/chatbot.py` to handle list of JDs in prompt

## Changes Made

### `bot/handlers.py`
- `user_jd` now stores a list of JD paths per user (like `user_files`)
- `/jd` initializes `user_jd[user_id] = []`
- JD uploads are appended to `user_jd[user_id]`
- `/done` shows both resumes and JDs
- `/analyze` parses all JDs, scores each resume against each JD, picks best match
- `analysis_results[user_id]["jd"]` is now a list of `{"name": ..., "data": ...}`

### `backend/chatbot.py`
- Updated prompt builder to iterate over multiple JDs in the analysis
