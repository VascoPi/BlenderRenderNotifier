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
import requests

from enum import Enum
from datetime import datetime

from .utils import get_preferences


class Bot_Status(Enum):
    START = "START RENDER FRAME"
    FINISH = "FINISH RENDER FRAME"
    CANCEL = "CANCEL RENDER"


class Telagram_Bot:
    start_time = None

    @classmethod
    def _generate_message(cls, status: Bot_Status):
        blrn_props = bpy.context.window_manager.blrn

        message = f"{status.value}\n"
        if blrn_props.enable_file and bpy.data.filepath:
            message += f"{bpy.data.filepath}"

        if blrn_props.enable_scene:
            message += f"{bpy.context.scene.name}\n"

        if blrn_props.enable_frame:
            frame = bpy.context.scene.frame_current
            frame_start = bpy.context.scene.frame_start
            frame_end = bpy.context.scene.frame_end
            frame_count = frame_end - frame_start
            message += f"{frame} / {frame_end}({frame_count})\n"

        if status == Bot_Status.START:
            cls.start_time = datetime.now()

        else:
            message += str(datetime.now() - cls.start_time).split('.')[0]
            cls.start_time = None

        return message

    @classmethod
    def _send_message(cls, status, *args, **kwargs):
        if not bpy.context.window_manager.blrn.enable_notification:
            return

        prefs = get_preferences()
        token = prefs.token
        chat_id = prefs.user
        if not all([token, chat_id]):
            return

        try:
            url = (f"https://api.telegram.org/bot{token}/"
                   f"sendmessage?chat_id={chat_id}&"
                   f"text={cls._generate_message(status)}")

            requests.get(url)

        except Exception as err:
            print(f"SEND MESSAGE: {err}")

    @classmethod
    def register(cls):
        bpy.app.handlers.render_pre.append(cls.render_pre)
        bpy.app.handlers.render_post.append(cls.render_post)
        bpy.app.handlers.render_cancel.append(cls.render_cancel)

    @classmethod
    def unregister(cls):
        bpy.app.handlers.render_pre.remove(cls.render_pre)
        bpy.app.handlers.render_post.remove(cls.render_post)
        bpy.app.handlers.render_cancel.remove(cls.render_cancel)

    @bpy.app.handlers.persistent
    def render_pre(self, *args, **kwargs):
        Telagram_Bot._send_message(Bot_Status.START, *args, **kwargs)

    @bpy.app.handlers.persistent
    def render_post(self, *args, **kwargs):
        Telagram_Bot._send_message(Bot_Status.FINISH, *args, **kwargs)

    @bpy.app.handlers.persistent
    def render_cancel(self, *args, **kwargs):
        Telagram_Bot._send_message(Bot_Status.CANCEL, *args, **kwargs)


bot = Telagram_Bot()
