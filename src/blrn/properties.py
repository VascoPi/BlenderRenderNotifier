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
from bpy.props import BoolProperty, PointerProperty


class BLRN_Bot_properties(bpy.types.PropertyGroup):
    enable_notification: BoolProperty(
        name="Enable Notification",
        default=True,
    )
    enable_result: BoolProperty(
        name="Render Result",
        default=True
    )
    enable_frame: BoolProperty(
        name="Frame",
        default=True
    )
    enable_scene: BoolProperty(
        name="Scene",
        default=True
    )
    enable_file: BoolProperty(
        name="Filename",
        default=True
    )

    @classmethod
    def register(cls):
        bpy.types.WindowManager.blrn = bpy.props.PointerProperty(name="Blender Render Notifier Properties", type=cls)
