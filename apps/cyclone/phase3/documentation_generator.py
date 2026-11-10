"""Phase 3: Documentation Generation module.

Generates professional documentation:
- API documentation (auto-generated from feature definitions)
- README.md (project overview, setup, usage)
- CHANGELOG.md (version history, release notes)
- CONTRIBUTING.md (development guidelines, coding standards)
- Models.md (data structure documentation)
- Examples (usage examples for developers)

Usage:
    from apps.cyclone.phase3.documentation_generator import DocumentationGenerator

    generator = DocumentationGenerator()
    readme = await generator.generate_readme({"name": "MOON-AI", "version": "13.0"})
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from .interface import (
    DocumentationError,
    DocumentationGenerator,
)

logger = logging.getLogger(__name__)


class DocumentationGeneratorImplementation(DocumentationGenerator):
    """Implementation of the documentation generator."""

    def __init__(self, output_dir: str = "docs") -> None:
        self.output_dir = output_dir
        self.generated_documents: list[str] = []

    async def generate_api_docs(self, features: list[dict[str, Any]]) -> str:
        """Generate API documentation in Markdown format."""
        docs = []
        docs.append("# API Documentation")
        docs.append("")
        docs.append(f"Generated: {datetime.now().isoformat()}")
        docs.append("")
        docs.append("## Overview")
        docs.append("")
        docs.append("This document describes the MOON-AI V13.0 API and its core capabilities.")
        docs.append("")
        docs.append("## Core Features")
        docs.append("")

        for feature in features:
            f_id = feature.get("feature_id", "unknown")
            name = feature.get("name", "Unnamed Feature")
            description = feature.get("description", "N/A")
            docs.append(f"### {name}")
            docs.append("")
            docs.append(f"**ID:** `{f_id}`")
            docs.append("")
            docs.append(f"{description}")
            docs.append("")
            docs.append("**Acceptance Criteria:**")
            docs.append("")
            for criterion in feature.get("acceptance_criteria", []):
                docs.append(f"- {criterion}")
            docs.append("")

        docs.append("## Endpoints")
        docs.append("")
        docs.append("### Agent Management")
        docs.append("")
        docs.append("| Method | Endpoint | Description |")
        docs.append("|--------|----------|-------------|")
        docs.append("| GET | `/api/agents` | List registered agents |")
        docs.append("| POST | `/api/agents/register` | Register a new agent |")
        docs.append("| DELETE | `/api/agents/{id}` | Remove an agent |")
        docs.append("")

        docs.append("### Task Management")
        docs.append("")
        docs.append("| Method | Endpoint | Description |")
        docs.append("|--------|----------|-------------|")
        docs.append("| POST | `/api/tasks/delegate` | Delegate a task |")
        docs.append("| GET | `/api/tasks` | List tasks |")
        docs.append("| GET | `/api/tasks/{id}` | Get task details |")
        docs.append("| PATCH | `/api/tasks/{id}` | Update task status |")
        docs.append("")

        return "".join(docs)

    async def generate_readme(self, project_info: dict[str, Any]) -> str:
        """Generate README.md content."""
        name = project_info.get("name", "Project")
        version = project_info.get("version", "0.0.0")
        description = project_info.get(
            "description", f"{name} V{version} - Professional AI Agent System"
        )
        install = project_info.get("install", "pip install -r requirements.txt")
        usage = project_info.get("usage", "python main.py")

        readme = []
        readme.append("# " + name)
        readme.append("")
        readme.append(f"Version {version}")
        readme.append("")
        readme.append("## Description")
        readme.append("")
        readme.append(description)
        readme.append("")
        readme.append("## Features")
        readme.append("")
        readme.append("- 🔬 Deep AI agent orchestration")
        readme.append("- 🤖 Universal agent connector with REST/WebSocket/IPC protocols")
        readme.append("- 📊 Advanced research workflows with citation tracking")
        readme.append("- 🌐 Browser and computer-use automation")
        readme.append("- 📚 Auto-generated API documentation")
        readme.append("- ✅ Comprehensive test suite with pytest")
        readme.append("")
        readme.append("## Installation")
        readme.append("")
        readme.append(f"```bash")
        readme.append(install)
        readme.append("```")
        readme.append("")
        readme.append("## Quick Start")
        readme.append("")
        readme.append(f"```bash")
        readme.append(usage)
        readme.append("```")
        readme.append("")
        readme.append("## Architecture")
        readme.append("")
        readme.append("The MOON-AI V13.0 architecture consists of:")
        readme.append("")
        readme.append("- **CYCLONE Server**: Node.js server (port 8765)")
        readme.append("- **MOON-AI Backend**: Python/FastAPI backend (port 8777)")
        readme.append("- **Connector**: Universal agent connector for agent orchestration")
        readme.append("- **Phase 1**: HERMES V13.0 protocol integration")
        readme.append("- **Phase 2**: Browser, Computer Use, and Research")
        readme.append("")
        readme.append("## License")
        readme.append("")
        readme.append("Proprietary - All rights reserved.")
        readme.append("")

        return "
".join(readme)

    async def generate_changelog(self, releases: list[dict[str, Any]]) -> str:
        """Generate CHANGELOG.md content."""
        changelog = []
        changelog.append("# Changelog")
        changelog.append("")
        changelog.append("All notable changes to this project will be documented in this file.")
        changelog.append("")
        changelog.append("The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).")
        changelog.append("")

        for release in sorted(releases, key=lambda r: r.get("version", ""), reverse=True):
            version = release.get("version", "unknown")
            date = release.get("date", datetime.now().isoformat())
            changelog.append(f"## [{version}] - {date}")
            changelog.append("")
            changelog.append("### Added")
            changelog.append("")
            for item in release.get("added", []):
                changelog.append(f"- {item}")
            changelog.append("")
            changelog.append("### Changed")
            changelog.append("")
            for item in release.get("changed", []):
                changelog.append(f"- {item}")
            changelog.append("")
            changelog.append("### Fixed")
            changelog.append("")
            for item in release.get("fixed", []):
                changelog.append(f"- {item}")
            changelog.append("")
            changelog.append("---")
            changelog.append("")

        return "
".join(changelog)

    async def generate_guidelines(self, project_name: str) -> str:
        """Generate CONTRIBUTING.md content."""
        guidelines = []
        guidelines.append("# Contributing to " + project_name)
        guidelines.append("")
        guidelines.append("Thank you for your interest in contributing to " + project_name + "!")
        guidelines.append("")
        guidelines.append("## Code of Conduct")
        guidelines.append("")
        guidelines.append("Please be respectful and constructive in all interactions.")
        guidelines.append("")
        guidelines.append("## How to Contribute")
        guidelines.append("")
        guidelines.append("1. Fork the repository")
        guidelines.append("2. Create a feature branch")
        guidelines.append("3. Make your changes")
        guidelines.append("4. Write tests")
        guidelines.append("5. Submit a pull request")
        guidelines.append("")
        guidelines.append("## Development Setup")
        guidelines.append("")
        guidelines.append("```bash")
        guidelines.append("git clone https://github.com/user/" + project_name + ".git")
        guidelines.append("cd " + project_name)
        guidelines.append("python -m venv .venv")
        guidelines.append("source .venv/bin/activate")
        guidelines.append("pip install -r requirements.txt")
        guidelines.append("```")
        guidelines.append("")
        guidelines.append("## Coding Standards")
        guidelines.append("")
        guidelines.append("- Follow PEP 8 for Python code")
        guidelines.append("- Write docstrings for all public functions")
        guidelines.append("- Keep functions focused and under 50 lines when possible")
        guidelines.append("- Use type hints for all new code")
        guidelines.append("- Write unit tests for new features")
        guidelines.append("")
        guidelines.append("## Testing")
        guidelines.append("")
        guidelines.append("```bash")
        guidelines.append("python -m pytest tests/ -v")
        guidelines.append("```")
        guidelines.append("")

        return "
".join(guidelines)

    async def generate_models(self, model_definitions: list[dict[str, Any]]) -> str:
        """Generate models documentation."""
        models_doc = []
        models_doc.append("# Data Models")
        models_doc.append("")
        models_doc.append("This document describes the core data models of the MOON-AI system.")
        models_doc.append("")

        for model in model_definitions:
            name = model.get("name", "Unknown")
            fields = model.get("fields", [])
            description = model.get("description", "")

            models_doc.append(f"## {name}")
            models_doc.append("")
            models_doc.append(f"{description}")
            models_doc.append("")
            models_doc.append("| Field | Type | Required | Description |")
            models_doc.append("|-------|------|----------|-------------|")
            for field in fields:
                f_name = field.get("name", "")
                f_type = field.get("type", "")
                f_required = field.get("required", False)
                f_desc = field.get("description", "")
                required = "Yes" if f_required else "No"
                models_doc.append(f"| {f_name} | {f_type} | {required} | {f_desc} |")
            models_doc.append("")

        return "
".join(models_doc)

    @property
    def generate_examples(self, templates: list[str]) -> str:
        """Generate examples directory content."""
        examples = []
        examples.append("# Examples")
        examples.append("")
        examples.append("This directory contains usage examples for the MOON-AI system.")
        examples.append("")
        for template in templates:
            examples.append(f"## {template}")
            examples.append("")
            examples.append(f"```")
            examples.append("Example code for " + template + "")
            examples.append("```")
            examples.append("")
        return "
".join(examples)


__all__ = ["DocumentationGeneratorImplementation"]
