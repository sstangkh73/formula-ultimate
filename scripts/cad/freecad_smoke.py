"""Create and export a disposable reference solid with FreeCADCmd."""

from __future__ import annotations

import json
import os
import sys

import FreeCAD as App
import Part


def main() -> int:
    output_path = os.environ.get("FORMULA_ULTIMATE_FREECAD_OUTPUT")
    if not output_path and len(sys.argv) >= 2:
        output_path = sys.argv[-1]
    if not output_path:
        raise SystemExit(
            "set FORMULA_ULTIMATE_FREECAD_OUTPUT or pass OUTPUT.step"
        )
    document = App.newDocument("FormulaUltimateWork005Smoke")
    try:
        shape = Part.makeBox(10.0, 20.0, 30.0)
        feature = document.addObject("PartDesign::Feature", "ReferenceBox")
        feature.Shape = shape
        document.recompute()
        Part.export([feature], output_path)

        bounds = shape.BoundBox
        evidence = json.dumps(
            {
                "output": output_path,
                "volume_mm3": shape.Volume,
                "solid_count": len(shape.Solids),
                "bounds_mm": [bounds.XLength, bounds.YLength, bounds.ZLength],
            },
            indent=2,
            sort_keys=True,
        )
        with open(output_path + ".json", "w", encoding="utf-8") as evidence_file:
            evidence_file.write(evidence + "\n")
        App.Console.PrintMessage(evidence + "\n")
    finally:
        App.closeDocument(document.Name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
