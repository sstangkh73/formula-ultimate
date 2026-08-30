from __future__ import annotations

from dataclasses import replace
import unittest

from formula_ultimate.structural import CylindricalInterface, LoadedInterfacePlateSpec, MeshData, StructuralEvidenceError, consistent_interface_load, map_cylindrical_interfaces


def spec() -> LoadedInterfacePlateSpec:
    return LoadedInterfacePlateSpec("p", 4.0, 4.0, 1.0, 70e9, 0.3, 2700, "m", "synthetic", (100.0, 0.0, 0.0), (CylindricalInterface("load", "loaded", 2.0, 0.0, 1.0), CylindricalInterface("support", "support", 0.5, -1.0, 0.2)), 0.1)


class LoadedInterfaceTests(unittest.TestCase):
    def test_cylindrical_mapping_and_consistent_resultant_close(self) -> None:
        mesh = MeshData({1:(3.0,0.0,0.0),2:(2.0,1.0,0.0),3:(1.0,0.0,1.0),4:(0.7,-1.0,0.0),5:(0.5,-0.8,0.0),6:(0.3,-1.0,1.0)}, {1:(1,2,3,4)}, {1:(1,2,3),2:(4,5,6)})
        mapped = map_cylindrical_interfaces(spec(), mesh, radial_tolerance_m=1e-12)
        loads = consistent_interface_load(spec(), mesh, mapped["load"])
        self.assertAlmostEqual(100.0, sum(value[0] for value in loads.values()))
        self.assertEqual({"load", "support"}, set(mapped))

    def test_duplicate_zero_area_and_ligament_fail_closed(self) -> None:
        with self.assertRaisesRegex(StructuralEvidenceError, "duplicated"):
            replace(spec(), interfaces=(spec().interfaces[0], replace(spec().interfaces[1], interface_id="load")))
        with self.assertRaises(StructuralEvidenceError):
            replace(spec().interfaces[0], radius_m=0.0)
        with self.assertRaisesRegex(StructuralEvidenceError, "ligament"):
            replace(spec(), interfaces=(replace(spec().interfaces[0], center_x_m=3.95), spec().interfaces[1]))

    def test_missing_interface_mapping_and_disconnected_mesh_fail_closed(self) -> None:
        mesh = MeshData({1:(3.0,0.0,0.0),2:(2.0,1.0,0.0),3:(1.0,0.0,1.0),4:(0.0,0.0,0.0)}, {1:(1,2,3,4)}, {1:(1,2,3)})
        with self.assertRaisesRegex(StructuralEvidenceError, "zero mapped area"):
            map_cylindrical_interfaces(spec(), mesh, radial_tolerance_m=1e-12)
        with self.assertRaisesRegex(StructuralEvidenceError, "disconnected"):
            MeshData({1:(0,0,0),2:(1,0,0),3:(0,1,0),4:(0,0,1),5:(3,0,0),6:(4,0,0),7:(3,1,0),8:(3,0,1)}, {1:(1,2,3,4),2:(5,6,7,8)}, {1:(1,2,3)})


if __name__ == "__main__":
    unittest.main()
