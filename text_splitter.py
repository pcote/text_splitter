# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

# (c) 2011 Phil Cote (cotejrp1)
import bpy
from pdb import set_trace

bl_info = {
    'name': 'Text Splitter',
    'author': 'Phil Cote, cotejrp1',
    'version': (0, 1),
    "blender": (2, 66, 3),
    "location": 'View3D > ',
    "description": "Splits up text objects into multiple words",
    "warning": "",
    "category": "Text"
}


class TextSplitOperator(bpy.types.Operator):
    """Text split operator"""
    bl_idname = "text.split"
    bl_label = "Text Splitter"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    shift_vector = bpy.props.FloatVectorProperty("Starting Shift Vector",
                                        min=-10, max=10,
                                        default=(0.0, 0.0, 0.0),
                                        description = "test xyz type",
                                        subtype='XYZ')

    offset_vector = bpy.props.FloatVectorProperty("Spacing Vector",
                                        min=-10, max=10,
                                        default=(0.0, 0.0, 0.0),
                                        description="test xyz type",
                                        subtype='XYZ')
    
    split_by_enum = bpy.props.EnumProperty(name="Not Yet Functional",
                                        description="Do not use yet. Does not work.",
                                        items=(("word", "word", "word",), 
                                                ("character", "character", "character",)))

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
        """
        if split_by_enum == "word":
            txt_list = txt_str.split()
        else:
            txt_list = list(txt_str)
         """
        txt_lst = txt_str.split()
        cur_x_offset, cur_y_offset, cur_z_offset = 0, 0, 0
        

        for the_word in txt_lst:
            txt_curve = bpy.data.curves.new(the_word, type="FONT")
            txt_curve.body = the_word
            new_ob = bpy.data.objects.new(the_word, txt_curve)
            scn.objects.link(new_ob)
            
            new_ob.name = "text_%s" % the_word.lower()
            new_ob.location = txt_ob.location + self.shift_vector
            new_ob.location.x += cur_x_offset
            new_ob.location.y += cur_y_offset
            new_ob.location.z += cur_z_offset

            cur_x_offset += self.offset_vector.x
            cur_y_offset += self.offset_vector.y
            cur_z_offset += self.offset_vector.z

        return {'FINISHED'}


class TextSplitPanel(bpy.types.Panel):

    """Text Splitting Tool"""
    bl_label = "Text Splitter"
    bl_idname = "SCENE_PT_splittext"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        layout.row().operator(TextSplitOperator.bl_idname)


def register():
    bpy.utils.register_class(TextSplitOperator)
    bpy.utils.register_class(TextSplitPanel)


def unregister():
    bpy.utils.unregister_class(TextSplitOperator)
    bpy.utils.unregister_class(TextSplitPanel)


if __name__ == "__main__":
    register()