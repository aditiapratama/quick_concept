# Copyright (C) 2024 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of quick_concept.
#
# quick_concept is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quick_concept is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with quick_concept.  If not, see <https://www.gnu.org/licenses/>.

from bpy.types import Panel
from .. import util as ut


class QC_PT_panel:
    """
    Panel in 3D Viewport Sidebar
    """

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Concept"


class QC_PT_tools(QC_PT_panel, Panel):
    bl_label = "Quick Concept"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        view = context.space_data

        col = layout.column(align=True)
        sub = col.column()
        sub.active = bool(
            view.region_3d.view_perspective != "CAMERA" or view.region_quadviews
        )

        sub.prop(view, "lock_object")
        lock_object = view.lock_object
        if lock_object:
            if lock_object.type == "ARMATURE":
                sub.prop_search(
                    view,
                    "lock_bone",
                    lock_object.data,
                    "edit_bones" if lock_object.mode == "EDIT" else "bones",
                    text="Bone",
                )

        if not lock_object:
            col.prop(view, "lock_cursor", text="To 3D Cursor")
        col = layout.column(heading="Lock", align=True)


class QC_PT_camera(QC_PT_panel, Panel):
    bl_label = "Camera Tools"
    bl_parent_id = "QC_PT_tools"
    # bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        view = context.space_data
        scn = context.scene
        cam = scn.camera.data if scn.camera else None
        indent = 0.05
        separator_fac = 1.25

        col = layout.column(align=False)
        row = ut._indent_row(col, indent, False)
        row.prop(scn, "camera", text="")
        if cam:
            row = ut._indent_row(col, indent, False)
            row.prop(cam, "type")

            row = ut._indent_row(col, indent, False)
            if cam.type == "PERSP":
                if cam.lens_unit == "MILLIMETERS":
                    row.prop(cam, "lens")
                elif cam.lens_unit == "FOV":
                    row.prop(cam, "angle")

                row = ut._indent_row(col, indent, False)
                row.prop(cam, "lens_unit")

            elif cam.type == "ORTHO":
                row.prop(cam, "ortho_scale")

            elif cam.type == "PANO":
                engine = context.engine
                if engine == "CYCLES":
                    ccam = cam.cycles
                    row.prop(ccam, "panorama_type")
                    if ccam.panorama_type == "FISHEYE_EQUIDISTANT":
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == "FISHEYE_EQUISOLID":
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_lens", text="Lens")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_fov")
                    elif ccam.panorama_type == "EQUIRECTANGULAR":
                        row = ut._indent_row(col, indent, False)
                        sub = row.column(align=True)
                        sub.prop(ccam, "latitude_min", text="Latitude Min")
                        sub.prop(ccam, "latitude_max", text="Max")
                        row = ut._indent_row(col, indent, False)
                        sub = row.column(align=True)
                        sub.prop(ccam, "longitude_min", text="longitude Min")
                        sub.prop(ccam, "longitude_max", text="max")
                    elif ccam.panorama_type == "FISHEYE_LENS_POLYNOMIAL":
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_fov")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_polynomial_k0", text="K0")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_polynomial_k1", text="K1")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_polynomial_k2", text="K2")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_polynomial_k3", text="K3")
                        row = ut._indent_row(col, indent, False)
                        row.prop(ccam, "fisheye_polynomial_k4", text="K4")

                elif engine in {
                    "BLENDER_RENDER",
                    "BLENDER_EEVEE",
                    "BLENDER_EEVEE_NEXT",
                    "BLENDER_WORKBENCH",
                    "BLENDER_WORKBENCH_NEXT",
                }:
                    if cam.lens_unit == "MILLIMETERS":
                        row.prop(cam, "lens")
                    elif cam.lens_unit == "FOV":
                        row.prop(cam, "angle")

                    row = ut._indent_row(col, indent, False)
                    row.prop(cam, "lens_unit")

            col.separator(factor=separator_fac)

            col = layout.column(heading="Camera", align=True)
            row = ut._indent_row(col, 0.05, False)
            row.prop(view, "lock_camera", text="Lock View")
            row = ut._indent_row(col, 0.45, False)
            row.operator("view3d.camera_to_view", text="Align to View")
            row = ut._indent_row(col, 0.45, False)
            row.operator("view3d.view_center_camera", text="Fit to View")

            col.separator(factor=separator_fac)
            col = layout.column(heading="Composition", align=False)
            row = ut._indent_row(col, indent, False)
            row.prop(
                cam,
                "show_passepartout",
                text="",
            )
            row.active = cam.show_passepartout
            row.prop(cam, "passepartout_alpha", text="")
            # row.prop_decorator(cam, "passepartout_alpha")

            row = ut._indent_row(col, indent, True)
            row.use_property_split = False
            row.prop(cam, "show_composition_thirds", toggle=True)
            row.prop(cam, "show_composition_center", toggle=True)
            row.prop(
                cam, "show_composition_center_diagonal", toggle=True, text="Diagonal"
            )

            row = ut._indent_row(col, indent, True)
            row.use_property_split = False
            row.prop(cam, "show_composition_golden", toggle=True, text="Golden")
            row.prop(cam, "show_composition_golden_tria_a", toggle=True, text="Tria A")
            row.prop(cam, "show_composition_golden_tria_b", toggle=True, text="Tria B")

            row = ut._indent_row(col, indent, True)
            row.use_property_split = False
            row.prop(
                cam, "show_composition_harmony_tri_a", toggle=True, text="Harmony A"
            )
            row.prop(
                cam, "show_composition_harmony_tri_b", toggle=True, text="Harmony B"
            )


class QC_PT_camera_dof_eevee(QC_PT_panel, Panel):
    bl_label = "Depth of Field"
    bl_options = {"DEFAULT_CLOSED"}
    COMPAT_ENGINES = {
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
        "BLENDER_WORKBENCH_NEXT",
    }
    bl_parent_id = "QC_PT_camera"

    def draw_header(self, context):
        scn = context.scene
        cam = scn.camera.data if scn.camera else None
        if cam:
            dof = cam.dof
            self.layout.prop(dof, "use_dof", text="")

    def draw(self, context):
        layout = self.layout


registry = [
    QC_PT_tools,
    QC_PT_camera,
    QC_PT_camera_dof_eevee,
]
