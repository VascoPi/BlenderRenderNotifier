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

from .properties import BLRN_Bot_properties
from .ui import BLRN_PT_panel
from .telegram_bot import bot


bl_info = {
    "name": "Blender Render Notifier",
    "author": "Vasyl Pidhirskyi",
    "version": (0, 0, 3),
    "blender": (4, 00, 0),
    "description": "Telegram notifies user about render status.",
    "location": "Rendertab -> Render Panel",
    "wiki_url": "https://github.com/VascoPi/BlenderRenderNotifier/blob/master/README.md",
    "category": "Render"
}


class BLRN_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    token: bpy.props.StringProperty(name="Token", maxlen=45)
    user: bpy.props.StringProperty(name="User ID")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "token")
        layout.prop(self, "user")


classes = (
    BLRN_Bot_properties,
    BLRN_PT_panel,
    BLRN_Preferences,
)

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)


def register():
    register_classes()
    bot.register()


def unregister():
    bot.unregister()
    unregister_classes()


if __name__ == "__main__":
    register()
