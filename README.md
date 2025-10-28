# Schema Validator

A CLI tool to validate and parse JSON files against a workflow schema.

The schema is a mix of:
* the [BiaFlows subset](http://biaflows-doc.neubias.org/) (see section 3) of the (now deprecated) [original cytomine](https://github.com/cytomine/cytomine/blob/5f4f7cb3f90a244b8c95c064918fd6986a4de2cf/cytomine/utilities/descriptor_reader.py) schema
* the [new](https://github.com/cytomine/cytomine/blob/main/app-engine/src/main/resources/schemas/tasks/task.v0.json) cytomine App Engine task schema
* the [NIST fair-compute](https://github.com/usnistgov/fair-chain-compute-container/blob/master/schema/manifest.schema.json) schema
* the [Bilayers](https://bilayers.org/understanding-config/#defining-inputs) schema

## Installation

```bash
cd biomero_schema
pixi shell
```

## Usage

### help

```bash
biomero-schema --help
```

## Predefined Tasks

### Validate a JSON file against the schema

```bash
pixi test-validate
```

### Parse a JSON file into a Pydantic representation

```bash
# Basic parsing with summary
pixi run test-parse

# Pretty print the full parsed object
pixi run test-pparse

# Output as JSON
pixi run test-jparse
```

## Files

- `src/biomero_schema/schema.json` - JSON Schema definition generated from the pseudocode
- `src/biomero_schema/models.py` - Pydantic models for the schema
- `src/biomero_schema/cli.py` - CLI implementation
- `tests/example_workflow.json` - Example workflow file for testing

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

See `tests/example_workflow.json` for a complete example of a valid workflow definition.
