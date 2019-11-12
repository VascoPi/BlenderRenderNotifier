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

bl_info = {
    "name": "Blender Render Notifier",
    "author": "Vasyl Pidhirskyi",
    "version": (0, 0, 1),
    "blender": (2, 7, 9),
    "description": "Telegram notifies user about render status.",
    "location": "Rendertab -> Render Panel",
    "wiki_url": "https://github.com/VascoPi/BlenderRenderNotifier/blob/master/README.md",
    "support": "TESTING",
    "warning": "Testing, WIP",
    "category": "Render"
}

import sys, os, bpy
from datetime import datetime
import requests
from bpy.app.handlers import persistent

sys.path.append(os.path.dirname(__file__))
URL = "https://api.telegram.org/bot{token}/"


# addon pref
class BlenderRenderNotifierAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    telegram_toggle = bpy.props.BoolProperty(default=True)
    telegram_token = bpy.props.StringProperty(name="Token", maxlen=45)
    telegram_user = bpy.props.StringProperty(name="User ID")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "telegram_token")
        layout.prop(self, "telegram_user")


#  interface
class NotifierPanel(bpy.types.Panel):
    bl_label = "Blender Render Notifier"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    start_time = datetime.now()
    status = "START RENDER FRAME"
    text = "{}:\nfile: {}\nscene: {}\nframe: {}/{}  ({})\ntimestamp: {}\nduration: {}"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.user_preferences.addons[__name__].preferences, "telegram_toggle", text="")

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.user_preferences.addons[__name__].preferences,
                 'telegram_token')
        row = layout.row(align=True)
        row.prop(context.user_preferences.addons[__name__].preferences,
                 'telegram_user')

    @classmethod
    def get_info(cls):
        status = cls.status
        file = "Not saved" if not bpy.data.filepath else bpy.data.filepath.split("\\")[-1]
        scene = bpy.context.scene.name
        frame = bpy.context.scene.frame_current
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        timestamp = datetime.now()
        if cls.status != "START RENDER FRAME":
            duration = str(timestamp - cls.start_time).split('.')[0]
        else:
            duration = '---'
        return status, file, scene, frame, frame_end, frame_start, timestamp.strftime("%H:%M:%S"), duration

    @classmethod
    def set_info(cls, status):
        cls.status = status
        if status == "START RENDER FRAME":
            cls.start_time = datetime.now()


def send_message(self):
    token = bpy.context.user_preferences.addons[__name__].preferences.telegram_token
    chat_id = bpy.context.user_preferences.addons[__name__].preferences.telegram_user
    state = bpy.context.user_preferences.addons[__name__].preferences.telegram_toggle
    message_text = NotifierPanel.text.format(*NotifierPanel.get_info())
    if all([token, chat_id, state]):
        url = (URL + 'sendmessage?chat_id={chat_id}&text={text}').format(token=token, chat_id=chat_id, text=message_text)
        try:
            requests.get(url)
        except:
            pass


@persistent
def send_message_start(self):
    NotifierPanel.set_info("START RENDER FRAME")
    send_message(self)


@persistent
def send_message_end(self):
    NotifierPanel.set_info("COMPLETE RENDER FRAME")
    send_message(self)


@persistent
def send_message_cancel(self):
    NotifierPanel.set_info("CANCEL RENDER")
    send_message(self)


#  registration
def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.render_pre.append(send_message_start)
    bpy.app.handlers.render_post.append(send_message_end)
    bpy.app.handlers.render_cancel.append(send_message_cancel)


def unregister():
    bpy.app.handlers.render_pre.remove(send_message_start)
    bpy.app.handlers.render_post.remove(send_message_end)
    bpy.app.handlers.render_cancel.remove(send_message_cancel)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
