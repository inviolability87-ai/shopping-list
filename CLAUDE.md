# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

The app is implemented and working:
- `PRD.md` — the product requirements document (source of truth for scope, features, and acceptance criteria)
- `prompts/01_skeleton_prompt.md` through `prompts/04_review_prompt.md` — the staged prompts used to build the app (skeleton → features → UI → PRD review); all four stages are complete
- `app.py` — the full Streamlit app
- `requirements.txt` — dependencies

When asked to make further changes, still treat `PRD.md` as the authoritative spec and `prompts/04_review_prompt.md` as the checklist for verifying changes, even though the initial staged build is done.

## Product Overview

A single-user shopping list app built with Python + Streamlit, intended to run locally with no login, no persistence across restarts, and no multi-user support (see "Out of Scope" in `PRD.md`). Core features: add, delete, edit, and check off items, backed entirely by `st.session_state` (no file/DB persistence in v1).

## Architecture

Single file, as required by the PRD's non-functional requirements:
- `app.py` — the entire Streamlit app (UI + logic in one file)
- `requirements.txt` — dependencies (`streamlit`)

Data model: `st.session_state.shopping_items` is a list of `{"id": int, "text": str, "checked": bool}`. Each item gets a unique, never-reused `id` from `st.session_state.next_id` (an incrementing counter). Widget keys for per-item controls (`check_{id}`, `edit_{id}`, `delete_{id}`, `edit_input_{id}`, `save_{id}`, `cancel_{id}`) are built from this `id`, not from list index/position — this is deliberate: index-based keys break after a delete reorders the list (a later item silently inherits an earlier item's stale widget state). `st.session_state.editing_id` tracks which single item (if any) is currently in edit mode; entering/leaving edit mode pops that item's `edit_input_{id}` key so a later edit session never shows stale leftover text.

All mutations (add/delete/edit/toggle) are wired through `on_click`/`on_change` callbacks that read and write `st.session_state` directly, rather than branching on widget return values in the main script body — this is the correct Streamlit pattern for immediate same-rerun consistency.

### Known gotcha: don't use dict-method names as session_state attribute keys

`st.session_state.items` was originally used as the list's storage key and silently returned `dict.items` (the bound method), not the stored list, because attribute-style access on `session_state` resolves real methods (`items`, `keys`, `values`, `get`, `pop`, `update`, `clear`, ...) before falling back to the state dict. It does not raise — it just silently returns the wrong object, so bugs here surface as confusing `TypeError`s far from the actual cause. This is why the list is named `shopping_items`, not `items`. Avoid reintroducing a session_state key that shadows a dict method.

## Commands

```bash
pip install -r requirements.txt
streamlit run app.py
```

There is no build step, linter, or formal test suite configured in this repository.

To verify behavior without a browser, use Streamlit's built-in `AppTest` framework (`from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py"); at.run()`), then drive widgets by `key` (e.g. `at.text_input(key="new_item_input").set_value(...).run()`, `at.button(key=f"delete_{item_id}").click().run()`) and assert on `at.session_state` / `at.exception`. This is how each build stage was verified in this project — write such scripts as scratch files and delete them after use rather than committing a test suite, unless the user asks for one.

## Working from the PRD

`PRD.md` defines the authoritative feature list (F1–F5), success/acceptance criteria, and UI layout expectations. When implementing or reviewing code in this repo, check against `PRD.md` rather than inferring requirements from code alone, especially for:
- what counts as in-scope vs. out-of-scope (e.g. no auth, no persistence in v1)
- the exact acceptance criteria used to judge whether a feature is "done"

`prompts/04_review_prompt.md` contains the specific checklist and output format to use when reviewing an implementation against the PRD (functional requirements, success criteria, common Streamlit `session_state`/widget-key bugs, and non-functional requirements).
