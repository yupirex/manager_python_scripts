# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

- **Run main manager**: `python main.py` - Starts the main engine that discovers and runs all userbot engines
  - Interactive mode with menu: Choose between background launch (requires existing sessions) or sequential launch (for authentication)
  - Sequential launch: Authenticates each userbot one by one, then runs all in background
  - Background launch: Runs all userbots concurrently (requires pre-existing session files)
- **Run individual engines**: Each engine can be run standalone from its directory:
  - `python _default/default_engine.py` - Default/example userbot engine
  - `python _autonomous/autonom_engine.py` - Autonomous userbot engine  
  - `python _garem_chatbot/main_bot_engine.py` - Garem chatbot engine
- **Dependencies**: `telethon` is the main requirement (see individual `requirements.txt` files in each project)
- **Build executables**: Use scripts in `#mixer/` directory for PyInstaller compilation across platforms

## Architecture Overview

This is a Telegram userbot management system that automatically discovers, deploys, and manages multiple Telegram userbots. The architecture follows a plugin-based pattern:

### Core Components

- **main.py**: Central manager that discovers engine files matching pattern `_*/[*_engine.py]` and runs them as separate processes
- **commons/common.py**: Shared utilities for all userbot engines. It is assumed that this folder will be copied into your project directory.
  - `debug()`: Message debugging with configurable output formats.
  - `use_config()`: INI file configuration management.
  - `main_auth()`: Telethon authentication flow with 2FA support.

### Project Structure

- **_[project_name]/**: Each directory starting with underscore contains a userbot project
  - `*_engine.py`: Main engine file that handles Telegram events
  - `*.session`: Telethon session files (auto-generated)
  - Configuration files (creds.ini, debug.ini, etc.)

### Configuration System

- **creds.ini**: Telegram API credentials (api_id, api_hash, phone, password)
- **debug.ini**: Debug output settings per project
- **[project]_set.ini**: Project-specific configuration files

### Engine Pattern

All engines follow this pattern:

  1. Import shared functions from `commons.common`
  2. Configure Telethon client with project-specific settings
  3. Register event handlers for `NewMessage` and `MessageEdited`
  4. Implement engine function that processes events and calls debug()
  5. Handle keyboard markup state (inline vs reply keyboards)

## Key Implementation Details

- **Process Isolation**: Each userbot runs as an independent subprocess for fault tolerance
- **Auto-Discovery**: Main manager automatically finds and deploys engines matching `_*/[*_engine.py]` pattern
- **Archive Support**: Automatic extraction and deployment of `_*.zip` archives containing userbot projects
- **Dual Launch Modes**: Sequential (interactive auth) vs background (concurrent execution) modes
- **Configuration Management**: INI-based configuration with UTF-8 encoding support
- **Debug System**: Highly configurable per-project output (sender, id, date, text, buttons, raw data)
- **Authentication**: Robust Telethon auth flow with 2FA support and credential persistence

## Security Considerations

- Session files contain sensitive authentication data - handle with care
- Some engines may contain hardcoded credentials (e.g., `_autonomous/autonom_engine.py`)
- Credential files (creds.ini) should never be committed to version control

## Development Notes

- **Language**: Codebase uses Russian/Ukrainian comments and debug messages
- **Configuration**: Uses configparser for INI files with UTF-8 encoding
- **Authentication Flow**: Interactive authentication with 2FA support, credentials stored in `creds.ini`
- **Event Handling**: Telethon async/await pattern with `NewMessage` and `MessageEdited` events
- **Process Management**: Each userbot runs as independent subprocess for fault tolerance
- **Testing**: No formal testing framework - manual testing required
- **Build System**: PyInstaller available in `#mixer/` for cross-platform binaries
- **Session Management**: Telethon session files auto-generated and stored per project

## Environment Variables

- `AUTH_ONLY_MODE=true` - Used during sequential launch to run engines in authentication-only mode
