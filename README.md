# Schema Validator

A CLI tool to validate and parse JSON files against a workflow schema.

The schema is a mix of a [subset](http://biaflows-doc.neubias.org/) (see section 3) of the [original (now deprecated)](https://github.com/cytomine/cytomine/blob/5f4f7cb3f90a244b8c95c064918fd6986a4de2cf/cytomine/utilities/descriptor_reader.py) cytomine schema,
the [new](https://github.com/cytomine/cytomine/blob/main/app-engine/src/main/resources/schemas/tasks/task.v0.json) cytomine schema,
the [fair-compute](https://github.com/usnistgov/fair-chain-compute-container/blob/master/schema/manifest.schema.json) schema,
and the [bilayers](https://bilayers.org/understanding-config/#defining-inputs) schema.

## Installation

```bash
cd schema_validator
pip install -e .
```

## Usage

### Validate a JSON file against the schema

```bash
schema-validator validate example_workflow.json
```

### Parse a JSON file into a Pydantic representation

```bash
# Basic parsing with summary
schema-validator parse example_workflow.json

# Pretty print the full parsed object
schema-validator parse example_workflow.json --pretty

# Output as JSON
schema-validator parse example_workflow.json --json
```

## Files

- `schema.json` - JSON Schema definition generated from the pseudocode
- `src/schema_validator/models.py` - Pydantic models for the schema
- `src/schema_validator/cli.py` - CLI implementation
- `example_workflow.json` - Example workflow file for testing

## Schema Structure

The schema defines a workflow with the following main components:

- **Basic Info**: name, description, schema-version
- **People & Organizations**: authors, institutions
- **Citations**: Required list of tool citations
- **Container**: container-image specification
- **Configuration**: Technical settings and resource requirements
- **Parameters**: inputs and outputs with type definitions
- **Command Line**: Template for execution

## Parameter Types

The schema supports several parameter types:
- `integer`, `float`, `boolean`, `string` - Basic types
- `file` - Files with format specification
- `image` - Images with sub-type and format
- `array` - Arrays with format (npy, npz)

## Example

See `example_workflow.json` for a complete example of a valid workflow definition.
