import bpy

def main(context):
    pass    


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
        #main(context)
        scn = context.scene
        txt_ob = context.active_object.data
        txt_str = txt_ob.body
        txt_lst = txt_str.split()
        
        for the_word in txt_lst:
            txt_curve = bpy.data.curves.new(the_word, type="FONT")
            txt_curve.body = the_word
            new_ob = bpy.data.objects.new(the_word, txt_curve)
            scn.objects.link(new_ob)
                
        return {'FINISHED'}


def register():
    bpy.utils.register_class(TextSplitOperator)


def unregister():
    bpy.utils.unregister_class(TextSplitOperator)


if __name__ == "__main__":
    register()
