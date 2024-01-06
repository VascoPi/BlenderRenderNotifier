# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy


class BLRN_PT_panel(bpy.types.Panel):
    bl_label = "Blender Render Notifier"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw_header(self, context):
        self.layout.prop(context.window_manager.blrn, "enable_notification", text="")

    def draw(self, context):
        blrn_props = context.window_manager.blrn

        layout = self.layout
        layout.use_property_split = True

        col = layout.column()
        col.enabled = blrn_props.enable_notification

        col.prop(blrn_props, "enable_result")
        col.prop(blrn_props, "enable_frame")
        col.prop(blrn_props, "enable_scene")
        col.prop(blrn_props, "enable_file")
