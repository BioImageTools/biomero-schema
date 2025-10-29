# BIOMERO Schema

A CLI tool to validate and parse JSON files against a workflow schema.

The schema is a mix of:
* the [BiaFlows subset](http://biaflows-doc.neubias.org/) (see section 3) of the (now deprecated) [original cytomine](https://github.com/cytomine/cytomine/blob/5f4f7cb3f90a244b8c95c064918fd6986a4de2cf/cytomine/utilities/descriptor_reader.py) schema
* the [new](https://github.com/cytomine/cytomine/blob/main/app-engine/src/main/resources/schemas/tasks/task.v0.json) cytomine App Engine task schema
* the [NIST fair-compute](https://github.com/usnistgov/fair-chain-compute-container/blob/master/schema/manifest.schema.json) schema
* the [Bilayers](https://bilayers.org/understanding-config/#defining-inputs) schema

## Installation

`pixi` is used for installation and running some tasks. It's not strictly required, but recommended to [install pixi](https://pixi.sh/latest/installation/).

```bash
cd biomero_schema
pixi shell
```

Or use `pip install -e .` (or equivilant) in a virtual environment.

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
- **Probelm Class**: Optional [BIAFlows problem class](https://neubias-wg5.github.io/problem_class_ground_truth.html#steps-section)
- **Container**: container-image specification
- **Configuration**: Technical settings and resource requirements
- **Parameters**: inputs and outputs with type definitions
- **Command Line**: Template for execution

## Example

See `tests/example_workflow.json` for a complete example of a valid workflow definition.

## Spec

The following is json-ish psuedo-code that describes the spec:

```json
schema = 
{
  "name": "string",                      // Required. GitHub workflow repository name (without prefix). E.g. NucleiTracking-ImageJ
  "description": "string"                // Required. Description of workflow.
  "schema-version": "string"             // Required. Semver of schema version.
  "authors":                             // Optional. Authors list.
    [
      {
        "name": "string",                // Required. Full name of author.
        "email": "optional",             // Optional. Email address of author.
        "affiliations": "string[]"       // Optional. List of affiliations matching "id" of an instituttion in instititions list.
      }
    ],
  "institutions":                        // Optional. Institutions list.
    [
      {
        "id": "string",                  // Required. Unique institute identifier.
        "name": "string"                 // Optional. Name of the institions. Defaults to id.
      }
    ],
  "citations":                           // Optional. List of citations for the tool. Defaults to empty list.
    [
      {
        "name": "string",                // Required. Name of the tool being cited.
        "doi": "string",                 // Optional. DOI number of the tool being cited. Defaults to empty string.
        "license": "string",             // Required. License of the tool being cited.
        "description": "string"          // Optional. Description of the tool being cited. Defaults to empty string.
      }
    ],
  // corresponding to: https://neubias-wg5.github.io/problem_class_ground_truth.html#steps-section
  "problem-class":                       // Optional. Biaflows problem class ("object-segmentation" | "pixel-classification" | "object-counting" | "object-detection" | "filament-tree-tracing" | "filament-networks-tracing" | "landmark-detection" | "particle-tracking" | "object-tracking").
  "container-image":                     // Required. Base cotnainer description.
    {
      "image": "string",                 // Required. Image to match the name of your workflow GitHub repository (lower case only). E.g. neubiaswg5/w_nucleitracking-imagej:1.0.0
      "type": "string",                  // Required. "oci" | "singularity" (lower case only).
    },
  "configuration":                       // Optional. Technical configuration.
  {
    "input_folder": "string",            // Optional. Full path where the input folder must be mounted in the container. Defaults to "/inputs".
    "output_folder": "string",           // Optional. Full path where teh output folder must be mounted in the container. Defaults to "/outputs".
    "resources":                         // Optional.
      {
        "networking": "boolean",         // Optional. Whether internet connection is needed. Defaults to False.
        "ram-min": "number",             // Optional. Minimum RAM in mebibytes (Mi). Defaults to 0.
        "cores-min": "number",           // Optional. Minimum number of CPU cores. Defaults to 1.
        "gpu": "boolean",                // Optional. GPU/accelerator required. Defaults to False.
        "cuda-requirements":             // Optional. GPU Cuda-related requirements.
          {
            "device-memory-min": "number", // Optional. Minimum device memory. Defaults to 0.
            "cuda-compute-capability": "string|string[]", // Optional: The cudaComputeCapability Schema; single min value or list of valid values. Defaults to None.
          },
        "cpuAVX": "boolean",             // Optional. Advanced Vector Extensions (AVX) CPU capability required. Defaults to False.
        "cpuAVX2": "boolean",            // Optional. Advanced Vector Extensions 2 (AVX2) CPU capability required. Defaults to False.
      }
  }
  "inputs":                              // Required. List of parameter descriptors.
    [
      {
        // references to "@id" get the value of "id" in lowercase
        // references to "@ID" get the value of "id" in uppercase
        "id": "string",                  // Required. Unique parameter identifier.
        "type": "string",                // Required. Data type of the parameter (Number|String|ineger|flaot|boolean|string|file|image|array).
        "name": "string",                // Optional. Human-readable display name appearing in BIAFLOWS UI (paramater dialog box). Defaults to "@id".
        "description": "string",         // Optional. Description of paramater. Context help in BIAFLOWS UI (paramater dialog box). Soft Defaults to "".
        "value-key": "string",           // Optional. Substitution key in CLI. Defaults to "[@ID]".
        "command-line-flag": "string",   // Optional. CLI flag. Defaults to "--@id".
        "default-value": "string|number|boolean", // Optional. Default value in BIAFLOWS UI (paramater dialog box). Soft Defaults to empty string.
        "optional": "boolean",           // Optional. If true, parameter not required. Soft Defaults to False.
        "set-by-server": "boolean",      // Optional. If true, parameter is server-assigned. Soft Defaults to False.
      }
    ]
  "outputs":                           // Optional. List of output parameter descriptors.
    [
      {
        // references to "@id" get the value of "id" in lowercase
        // references to "@ID" get the value of "id" in uppercase
        "id": "string",                  // Required. Unique parameter identifier.
        "type": "string",                // Required. Data type of the parameter (Number|String).
        "name": "string",                // Optional. Human-readable display name appearing in BIAFLOWS UI (paramater dialog box). Defaults to "@id".
        "description": "string",         // Optional. Description of paramater. Context help in BIAFLOWS UI (paramater dialog box). Soft Defaults to "".
        "value-key": "string",           // Optional. Substitution key in CLI. Defaults to "[@ID]".
        "command-line-flag": "string",   // Optional. CLI flag. Defaults to "--@id".
        "default-value": "string|number|boolean", // Optional. Default value in BIAFLOWS UI (paramater dialog box). Soft Defaults to empty string.
        "optional": "boolean",           // Optional. If true, parameter not required. Soft Defaults to False.
        "set-by-server": "boolean",      // Optional. If true, parameter is server-assigned. Soft Defaults to False.
      }
    ]
  "command-line": "string"               // Required. e.g. "python wrapper.py CYTOMINE_HOST CYTOMINE_PUBLIC_KEY CYTOMINE_PRIVATE_KEY CYTOMINE_ID_PROJECT CYTOMINE_ID_SOFTWARE IJ_RADIUS IJ_THRESHOLD".
}

file =
{
  "format": "string"                    // Required. Extension of the file type (.csv).
}

image =
{
  "sub-type": "string",                 // Required. Image type (grayscale|color|binary|labeled|class).
  "format": "string"                    // Required. Extension of the image type (tif, png, jpg, jpeg, tiff, ometiff).
}

array =
{
  "format": "string"                    // Required. Extension of the file type (npy, npz)
}
```
