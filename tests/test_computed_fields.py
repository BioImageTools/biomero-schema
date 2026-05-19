"""Tests for WorkflowSchema.requires_zarr and requires_plate computed fields."""
import json
import pytest
from pathlib import Path
from biomero_schema.models import WorkflowSchema


TESTS_DIR = Path(__file__).parent


def load_example() -> dict:
    return json.loads((TESTS_DIR / "example_workflow.json").read_text())


def make_schema(image_inputs: list) -> WorkflowSchema:
    """Build a minimal WorkflowSchema with the given image input list."""
    base = load_example()
    base["inputs"] = image_inputs
    return WorkflowSchema.model_validate(base)


def image_input(fmt=None, subtype=None) -> dict:
    inp = {
        "id": "input_image",
        "type": "image",
        "name": "Input",
        "value-key": "[INPUT_IMAGE]",
        "command-line-flag": "--input",
    }
    if fmt is not None:
        inp["format"] = fmt
    if subtype is not None:
        inp["sub-type"] = subtype
    return inp


# ---------------------------------------------------------------------------
# requires_zarr
# ---------------------------------------------------------------------------

class TestRequiresZarr:
    def test_false_for_tiff(self):
        schema = make_schema([image_input(fmt="tif")])
        assert schema.requires_zarr is False

    def test_false_for_ometiff(self):
        schema = make_schema([image_input(fmt="ometiff")])
        assert schema.requires_zarr is False

    def test_false_for_png(self):
        schema = make_schema([image_input(fmt="png")])
        assert schema.requires_zarr is False

    def test_false_for_no_image_inputs(self):
        base = load_example()
        base["inputs"] = [
            {"id": "x", "type": "float", "value-key": "[X]", "command-line-flag": "--x"}
        ]
        schema = WorkflowSchema.model_validate(base)
        assert schema.requires_zarr is False

    def test_true_for_zarr(self):
        schema = make_schema([image_input(fmt="zarr")])
        assert schema.requires_zarr is True

    def test_true_for_omezarr(self):
        schema = make_schema([image_input(fmt="omezarr")])
        assert schema.requires_zarr is True

    def test_true_for_ome_zarr_dot(self):
        schema = make_schema([image_input(fmt="ome.zarr")])
        assert schema.requires_zarr is True

    def test_true_for_ome_zarr_dash(self):
        schema = make_schema([image_input(fmt="ome-zarr")])
        assert schema.requires_zarr is True

    def test_true_for_format_list_containing_zarr(self):
        schema = make_schema([image_input(fmt=["tif", "zarr"])])
        assert schema.requires_zarr is True

    def test_true_when_plate_subtype(self):
        """Plate implies ZARR."""
        schema = make_schema([image_input(fmt="omezarr", subtype="plate")])
        assert schema.requires_zarr is True

    def test_false_for_zarr_format_on_non_image_type(self):
        """format field on a non-image input should not trigger zarr."""
        base = load_example()
        base["inputs"] = [
            {"id": "x", "type": "file", "format": "zarr", "value-key": "[X]", "command-line-flag": "--x"}
        ]
        schema = WorkflowSchema.model_validate(base)
        assert schema.requires_zarr is False


# ---------------------------------------------------------------------------
# requires_plate
# ---------------------------------------------------------------------------

class TestRequiresPlate:
    def test_false_by_default(self):
        schema = make_schema([image_input(fmt="tif", subtype="grayscale")])
        assert schema.requires_plate is False

    def test_false_for_no_subtype(self):
        schema = make_schema([image_input(fmt="zarr")])
        assert schema.requires_plate is False

    def test_true_for_plate_subtype(self):
        schema = make_schema([image_input(fmt="omezarr", subtype="plate")])
        assert schema.requires_plate is True

    def test_true_for_plate_in_subtype_list(self):
        schema = make_schema([image_input(fmt="omezarr", subtype=["plate"])])
        assert schema.requires_plate is True

    def test_false_for_other_subtype(self):
        schema = make_schema([image_input(fmt="tif", subtype="grayscale")])
        assert schema.requires_plate is False

    def test_plate_also_sets_zarr(self):
        """Plate always implies requires_zarr too."""
        schema = make_schema([image_input(fmt="omezarr", subtype="plate")])
        assert schema.requires_zarr is True
        assert schema.requires_plate is True


# ---------------------------------------------------------------------------
# Serialisation — flags appear in model_dump(by_alias=True)
# ---------------------------------------------------------------------------

class TestSerialisedOutput:
    def test_keys_present_in_dump(self):
        schema = make_schema([image_input(fmt="zarr", subtype="plate")])
        data = schema.model_dump(by_alias=True)
        assert "requires-zarr" in data
        assert "requires-plate" in data

    def test_values_correct_in_dump(self):
        schema = make_schema([image_input(fmt="zarr", subtype="plate")])
        data = schema.model_dump(by_alias=True)
        assert data["requires-zarr"] is True
        assert data["requires-plate"] is True

    def test_false_values_in_dump(self):
        schema = make_schema([image_input(fmt="tif")])
        data = schema.model_dump(by_alias=True)
        assert data["requires-zarr"] is False
        assert data["requires-plate"] is False


# ---------------------------------------------------------------------------
# Round-trip through example_workflow.json (tiff input → both False)
# ---------------------------------------------------------------------------

def test_example_workflow_no_zarr():
    schema = WorkflowSchema.model_validate(load_example())
    assert schema.requires_zarr is False
    assert schema.requires_plate is False
