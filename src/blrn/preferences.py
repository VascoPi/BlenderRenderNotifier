import bpy


class BLRN_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    token: bpy.props.StringProperty(name="Token", maxlen=45)
    user: bpy.props.StringProperty(name="User ID")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "token")
        layout.prop(self, "user")


register, unregister = bpy.utils.register_classes_factory([
    BLRN_Preferences,
])
