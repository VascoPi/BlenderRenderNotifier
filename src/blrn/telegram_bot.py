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


def verification(func):
    def inner(*arg, **kwargs):
        blrn_props = bpy.context.window_manager.blrn
        if not blrn_props.enable_notification:
            return

        prefs = get_preferences()
        if not all([prefs.token, prefs.user]):
            return

        if not bot.is_active():
            return

        print("Verification: ", bot.is_active(), func)

        return func(*arg, **kwargs)

    return inner


class Bot:
    def __init__(self):
        self.status = ""
        self.request = None
        self.message_id = -1
        self.render_time = []
        self.frame_time = []
        self.total_time = 0

    def connection_status(self):
        return f"Something went wrong: {self.request.reason}, {self.request.status_code}"

    def is_active(self):
        return self.request is None or self.request.reason == 'OK'

    def _generate_message(self, *args, **kwargs):
        blrn_props = bpy.context.window_manager.blrn
        message = f"status: {self.status}\n"

        if blrn_props.enable_file and bpy.data.filepath:
            message += f"file: {bpy.data.filepath}\n"

        scene = bpy.context.scene
        if blrn_props.enable_scene:
            message += f"scene: {scene.name}\n"

        if blrn_props.enable_frame:
            message += f"progress: {self.frame - scene.frame_start + 1}/{scene.frame_end - scene.frame_start}\n"

        if blrn_props.enable_frame:
            message += "".join(map(lambda i: f"frame {i[0]}: {str(i[1]).split('.')[0]}\n", self.frame_time))
            message += f"total: {str(self.total_time).split('.')[0]}\n"

        return message

    def send_message(self, message, edit=False):
        prefs = get_preferences()
        url = f"https://api.telegram.org/bot{prefs.token}"
        if edit:
            message_id = self.request.json()['result']['message_id']
            url += f"/editMessageText?chat_id={prefs.user}&text={message}&message_id={message_id}"

        else:
            url += f"/sendmessage?chat_id={prefs.user}&text={message}"

        self.request = requests.get(url)

    @verification
    def render_init(self):
        print("render_init")
        self.status = 'Rendering...'
        self.frame = bpy.context.scene.frame_start
        self.render_time.append(datetime.now())
        self.send_message(self._generate_message())

    # @verification
    # def render_pre(self):
    #     print("render_pre")

    @verification
    def render_post(self):
        print("render_post")
        self.frame = bpy.context.scene.frame_current
        self.render_time.append(datetime.now())
        self.frame_time.append((self.frame, self.render_time[-1] - self.render_time[-2]))
        self.total_time = self.render_time[-1] - self.render_time[0]
        self.send_message(self._generate_message(), True)

    @verification
    def render_cancel(self):
        print("render_cancel")
        self.frame = self.frame_time[-1][0]
        self.status = "Cancel"
        self.send_message(self._generate_message(), True)

    @verification
    def render_complete(self):
        print("render_complete")
        self.frame = self.frame_time[-1][0]
        self.status = "Complete"
        self.send_message(self._generate_message(), True)


@bpy.app.handlers.persistent
def render_init(*args, **kwargs):
    bot.render_init()

# @bpy.app.handlers.persistent
# def render_pre(*args, **kwargs):
#     bot.render_pre()


@bpy.app.handlers.persistent
def render_post(*args, **kwargs):
    bot.render_post()


@bpy.app.handlers.persistent
def render_cancel(*args, **kwargs):
    bot.render_cancel()


@bpy.app.handlers.persistent
def render_complete(*args, **kwargs):
    bot.render_complete()


def register():
    bpy.app.handlers.render_init.append(render_init)
    # bpy.app.handlers.render_pre.append(render_pre)
    bpy.app.handlers.render_post.append(render_post)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_complete.append(render_complete)


def unregister():
    bpy.app.handlers.render_init.remove(render_init)
    # bpy.app.handlers.render_pre.remove(render_pre)
    bpy.app.handlers.render_post.remove(render_post)
    bpy.app.handlers.render_cancel.remove(render_cancel)
    bpy.app.handlers.render_complete.remove(render_complete)

bot = Bot()
