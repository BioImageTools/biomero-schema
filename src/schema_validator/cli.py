"""CLI for schema validation and parsing."""
import json
import sys
from pathlib import Path
from typing import Any, Dict

import click
import jsonschema
from rich.console import Console
from rich.pretty import pprint

from .models import WorkflowSchema

console = Console()


def load_schema() -> Dict[str, Any]:
    """Load the JSON schema from file."""
    schema_path = Path(__file__) / "schema.json"
    if not schema_path.exists():
        console.print(f"[red]Error: Schema file not found at {schema_path}[/red]")
        sys.exit(1)
    
    with open(schema_path) as f:
        return json.load(f)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file and return parsed content."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[red]Error: File '{file_path}' not found[/red]")
        sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON in '{file_path}': {e}[/red]")
        sys.exit(1)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Schema validator CLI tool."""
    pass


@cli.command()
@click.argument("json_file", type=click.Path(exists=True))
def validate(json_file: str):
    """Validate a JSON file against the schema."""
    console.print(f"[blue]Validating {json_file}...[/blue]")
    
    # Load schema and JSON file
    schema = load_schema()
    data = load_json_file(json_file)
    
    try:
        jsonschema.validate(data, schema)
        console.print("[green]✓ Validation successful![/green]")
    except jsonschema.ValidationError as e:
        console.print("[red]✗ Validation failed:[/red]")
        console.print(f"[red]  {e.message}[/red]")
        if e.absolute_path:
            console.print(f"[yellow]  Path: {' -> '.join(str(p) for p in e.absolute_path)}[/yellow]")
        sys.exit(1)
    except jsonschema.SchemaError as e:
        console.print(f"[red]Error: Invalid schema: {e.message}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("json_file", type=click.Path(exists=True))
@click.option("--pretty", is_flag=True, help="Pretty print the parsed object")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def parse(json_file: str, pretty: bool, output_json: bool):
    """Parse a JSON file into a Pydantic representation."""
    console.print(f"[blue]Parsing {json_file}...[/blue]")
    
    # Load and validate JSON file
    data = load_json_file(json_file)
    
    try:
        # Parse into Pydantic model
        workflow = WorkflowSchema.model_validate(data)
        
        console.print("[green]✓ Parsing successful![/green]")
        
        if output_json:
            # Output as JSON
            json_output = workflow.model_dump_json(indent=2, by_alias=True)
            console.print(json_output)
        elif pretty:
            # Pretty print the Pydantic object
            console.print("\n[bold]Parsed Workflow Object:[/bold]")
            pprint(workflow)
        else:
            # Default: show structured representation
            console.print("\n[bold]Workflow Schema:[/bold]")
            console.print(f"Name: {workflow.name}")
            console.print(f"Description: {workflow.description}")
            console.print(f"Schema Version: {workflow.schema_version}")
            console.print(f"Container Image: {workflow.container_image.image} ({workflow.container_image.type})")
            console.print(f"Citations: {len(workflow.citations)} citation(s)")
            console.print(f"Inputs: {len(workflow.inputs)} parameter(s)")
            if workflow.outputs:
                console.print(f"Outputs: {len(workflow.outputs)} parameter(s)")
            if workflow.authors:
                console.print(f"Authors: {len(workflow.authors)} author(s)")
            if workflow.institutions:
                console.print(f"Institutions: {len(workflow.institutions)} institution(s)")
            
    except Exception as e:
        console.print(f"[red]✗ Parsing failed: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
