bl_info = {
    "name": "Blender Render Notifier",
    "author": "Vasyl Pidhirskyi",
    "version": (0, 0, 1),
    "blender": (2, 7, 9),
    "description": "Telegram notifies user about render status.",
    "location": "Rendertab -> Render Panel",
    "warning": "Testing, WIP",
    "category": "Render"
}

import sys, os, bpy
from datetime import datetime
import requests
from bpy.app.handlers import persistent

sys.path.append(os.path.dirname(__file__))
URL = "https://api.telegram.org/bot{token}/"


def get_token(self):
    return self['telegram_token']


def set_token(self, value):
    self['telegram_token'] = value


def get_user_id(self):
    return self['telegram_user']


def set_user_id(self, value):
    self['telegram_user'] = value


bpy.types.Scene.telegram_token = bpy.props.StringProperty(name="Token",
                                                          maxlen=45,
                                                          get=get_token,
                                                          set=set_token)
bpy.types.Scene.telegram_user = bpy.props.StringProperty(name="User ID",
                                                         get=get_user_id,
                                                         set=set_user_id)


def send_message(self, text):
    token = bpy.context.user_preferences.addons[__name__].preferences.telegram_token
    chat_id = bpy.context.user_preferences.addons[__name__].preferences.telegram_user
    url = (URL + 'sendmessage?chat_id={chat_id}&text={text}').format(
        token=token, chat_id=chat_id, text=text)
    requests.get(url)


@ persistent
def send_message_start(self):
    print('START')
    text = "START RENDER:\nscene: {name}\nframe: {frame}\nstarts at: {time}".format(
        name=bpy.context.scene.name,
        frame=bpy.context.scene.frame_current,
        time=datetime.now().strftime("%H:%M:%S %Z"))
    send_message(self, text)


@persistent
def send_message_end(self):
    print('END')
    text = "FINISH RENDER:\nscene: {name}\nframe: {frame}\nends at: {time}".format(
        name=bpy.context.scene.name,
        frame=bpy.context.scene.frame_current,
        time=datetime.now().strftime("%H:%M:%S %Z"))
    send_message(self, text)


# addon pref
class BlenderRenderNotifierAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    telegram_token = bpy.props.StringProperty(name="Token", maxlen=45,
                                              get=get_token, set=set_token)
    telegram_user = bpy.props.StringProperty(name="User ID", get=get_user_id,
                                             set=set_user_id)

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

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.user_preferences.addons[__name__].preferences,
                 'telegram_token')
        row = layout.row(align=True)
        row.prop(context.user_preferences.addons[__name__].preferences,
                 'telegram_user')


#  registration
def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.render_pre.append(send_message_start)
    bpy.app.handlers.render_post.append(send_message_end)


def unregister():
    bpy.app.handlers.render_pre.remove(send_message_start)
    bpy.app.handlers.render_post.remove(send_message_end)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
