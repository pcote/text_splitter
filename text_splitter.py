import bpy


class TextSplitOperator(bpy.types.Operator):
    """Text split operator"""
    bl_idname = "text.split"
    bl_label = "Text Splitter"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        is_valid = ob is not None and ob.type == 'FONT'
        return is_valid

    def execute(self, context):
        scn = context.scene
        txt_ob = context.active_object
        txt_data = context.active_object.data
        txt_str = txt_data.body
        txt_lst = txt_str.split()

        for the_word in txt_lst:
            txt_curve = bpy.data.curves.new(the_word, type="FONT")
            txt_curve.body = the_word
            new_ob = bpy.data.objects.new(the_word, txt_curve)
            scn.objects.link(new_ob)
            new_ob.location = txt_ob.location

        return {'FINISHED'}


class TextSplitPanel(bpy.types.Panel):
    """Text Splitting Tool"""
    bl_label = "Text Splitter"
    bl_idname = "SCENE_PT_splittext"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        layout.operator(TextSplitOperator.bl_idname)


def register():
    bpy.utils.register_class(TextSplitOperator)
    bpy.utils.register_class(TextSplitPanel)


def unregister():
    bpy.utils.unregister_class(TextSplitOperator)
    bpy.utils.unregister_class(TextSplitPanel)


if __name__ == "__main__":
    register()
