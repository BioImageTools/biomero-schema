"""Pydantic models for the workflow schema."""
from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field


class Author(BaseModel):
    """Author model."""
    name: str = Field(..., description="Full name of author")
    email: Optional[str] = Field(None, description="Email address of author")
    affiliations: Optional[List[str]] = Field(None, description="List of affiliations matching 'id' of an institution in institutions list")


class Institution(BaseModel):
    """Institution model."""
    id: str = Field(..., description="Unique institute identifier")
    name: Optional[str] = Field(None, description="Name of the institution. Defaults to id")


class Citation(BaseModel):
    """Citation model."""
    name: str = Field(..., description="Name of the tool being cited")
    doi: Optional[str] = Field(None, description="DOI number of the tool being cited. Defaults to empty string")
    license: str = Field(..., description="License of the tool being cited")
    description: Optional[str] = Field(None, description="Description of the tool being cited. Defaults to empty string")


class ContainerImage(BaseModel):
    """Container image model."""
    image: str = Field(..., description="Image to match the name of your workflow GitHub repository (lower case only)")
    type: Literal["oci", "singularity"] = Field(..., description="Container type")


class CudaRequirements(BaseModel):
    """CUDA requirements model."""
    device_memory_min: Optional[float] = Field(None, alias="device-memory-min", description="Minimum device memory. Defaults to 0")
    cuda_compute_capability: Optional[Union[str, List[str]]] = Field(None, alias="cuda-compute-capability", description="The cudaComputeCapability Schema; single min value or list of valid values. Defaults to None")


class Resources(BaseModel):
    """Resources model."""
    networking: Optional[bool] = Field(None, description="Whether internet connection is needed. Defaults to False")
    ram_min: Optional[float] = Field(None, alias="ram-min", description="Minimum RAM in mebibytes (Mi). Defaults to 0")
    cores_min: Optional[float] = Field(None, alias="cores-min", description="Minimum number of CPU cores. Defaults to 1")
    gpu: Optional[bool] = Field(None, description="GPU/accelerator required. Defaults to False")
    cuda_requirements: Optional[CudaRequirements] = Field(None, alias="cuda-requirements")
    cpuAVX: Optional[bool] = Field(None, description="Advanced Vector Extensions (AVX) CPU capability required. Defaults to False")
    cpuAVX2: Optional[bool] = Field(None, description="Advanced Vector Extensions 2 (AVX2) CPU capability required. Defaults to False")


class Configuration(BaseModel):
    """Configuration model."""
    input_folder: Optional[str] = Field(None, description="Full path where the input folder must be mounted in the container. Defaults to '/inputs'")
    output_folder: Optional[str] = Field(None, description="Full path where the output folder must be mounted in the container. Defaults to '/outputs'")
    resources: Optional[Resources] = Field(None)


class FileParameter(BaseModel):
    """File parameter specific fields."""
    format: str = Field(..., description="Extension of the file type (.csv)")


class ImageParameter(BaseModel):
    """Image parameter specific fields."""
    sub_type: Literal["grayscale", "color", "binary", "labeled", "class"] = Field(..., alias="sub-type", description="Image type")
    format: Literal["tif", "png", "jpg", "jpeg", "tiff", "ometiff"] = Field(..., description="Extension of the image type")


class ArrayParameter(BaseModel):
    """Array parameter specific fields."""
    format: Literal["npy", "npz"] = Field(..., description="Extension of the file type")


class Parameter(BaseModel):
    """Parameter model."""
    id: str = Field(..., description="Unique parameter identifier")
    type: Literal["Number", "String", "integer", "float", "boolean", "string", "file", "image", "array"] = Field(..., description="Data type of the parameter")
    name: Optional[str] = Field(None, description="Human-readable display name appearing in BIAFLOWS UI (parameter dialog box). Defaults to '@id'")
    description: Optional[str] = Field(None, description="Description of parameter. Context help in BIAFLOWS UI (parameter dialog box). Soft Defaults to ''")
    value_key: Optional[str] = Field(None, alias="value-key", description="Substitution key in CLI. Defaults to '[@ID]'")
    command_line_flag: Optional[str] = Field(None, alias="command-line-flag", description="CLI flag. Defaults to '--@id'")
    default_value: Optional[Union[str, float, bool]] = Field(None, alias="default-value", description="Default value in BIAFLOWS UI (parameter dialog box). Soft Defaults to empty string")
    optional: Optional[bool] = Field(None, description="If true, parameter not required. Soft Defaults to False")
    set_by_server: Optional[bool] = Field(None, alias="set-by-server", description="If true, parameter is server-assigned. Soft Defaults to False")
    
    # Type-specific fields
    format: Optional[str] = Field(None, description="Format for file/image/array types")
    sub_type: Optional[str] = Field(None, alias="sub-type", description="Sub-type for image parameters")


class OutputParameter(BaseModel):
    """Output parameter model."""
    id: str = Field(..., description="Unique parameter identifier")
    type: Literal["Number", "String"] = Field(..., description="Data type of the parameter")
    name: Optional[str] = Field(None, description="Human-readable display name appearing in BIAFLOWS UI (parameter dialog box). Defaults to '@id'")
    description: Optional[str] = Field(None, description="Description of parameter. Context help in BIAFLOWS UI (parameter dialog box). Soft Defaults to ''")
    value_key: Optional[str] = Field(None, alias="value-key", description="Substitution key in CLI. Defaults to '[@ID]'")
    command_line_flag: Optional[str] = Field(None, alias="command-line-flag", description="CLI flag. Defaults to '--@id'")
    default_value: Optional[Union[str, float, bool]] = Field(None, alias="default-value", description="Default value in BIAFLOWS UI (parameter dialog box). Soft Defaults to empty string")
    optional: Optional[bool] = Field(None, description="If true, parameter not required. Soft Defaults to False")
    set_by_server: Optional[bool] = Field(None, alias="set-by-server", description="If true, parameter is server-assigned. Soft Defaults to False")


class WorkflowSchema(BaseModel):
    """Main workflow schema model."""
    name: str = Field(..., description="GitHub workflow repository name (without prefix). E.g. NucleiTracking-ImageJ")
    description: str = Field(..., description="Description of workflow")
    schema_version: str = Field(..., alias="schema-version", description="Semver of schema version")
    authors: Optional[List[Author]] = Field(None, description="Authors list")
    institutions: Optional[List[Institution]] = Field(None, description="Institutions list")
    citations: List[Citation] = Field(..., min_length=1, description="List of citations for the tool. At least one required")
    container_image: ContainerImage = Field(..., alias="container-image", description="Base container description")
    configuration: Optional[Configuration] = Field(None, description="Technical configuration")
    inputs: List[Parameter] = Field(..., description="List of parameter descriptors")
    outputs: Optional[List[OutputParameter]] = Field(None, description="List of output parameter descriptors")
    command_line: str = Field(..., alias="command-line", description="Command line template")

    class Config:
        populate_by_name = True
        validate_by_name = True
