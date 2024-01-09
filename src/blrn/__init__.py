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

from . import (
    properties,
    preferences,
    telegram_bot,
    ui,
)


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


def register():
    properties.register()
    preferences.register()
    telegram_bot.register()
    ui.register()


def unregister():
    ui.unregister()
    telegram_bot.unregister()
    preferences.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
