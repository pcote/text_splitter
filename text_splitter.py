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
from bpy_extras.object_utils import AddObjectHelper, object_data_add

bl_info = {
    'name': 'Text Splitter',
    'author': 'Phil Cote, cotejrp1',
    'version': (0,1),
    "blender": (2,66,3),
    "location": 'View3D > ',
    "description": "Splits up text objects into multiple words",
    "warning": "",
    "category": "Text"
}

class TextSplitOperator(bpy.types.Operator, AddObjectHelper):
    """Text split operator"""
    bl_idname = "text.split"
    bl_label = "Text Splitter"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    x_text_offset = bpy.props.FloatProperty(name="X Text Offset",
                                        description="X Offset of the text",
                                        min=-10, max=10, default=0)
    
    y_text_offset = bpy.props.FloatProperty(name="Y Text Offset",
                                        description="Y Offset of the text",
                                        min=-10, max=10, default=0)
    
    z_text_offset = bpy.props.FloatProperty(name="Z Text Offset",
                                        description="Z Offset of the text",
                                        min=-10, max=10, default=0)
    

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        is_valid = ob != None and ob.type == 'FONT'
        return is_valid

    def execute(self, context):
        scn = context.scene
        txt_ob = context.active_object
        txt_data = context.active_object.data
        txt_str = txt_data.body
        txt_lst = txt_str.split()
        
        cur_x_offset, cur_y_offset, cur_z_offset = 0,0,0
        
        for the_word in txt_lst:
            txt_curve = bpy.data.curves.new(the_word, type="FONT")
            txt_curve.body = the_word
            new_ob = bpy.data.objects.new(the_word, txt_curve)
            scn.objects.link(new_ob)
            new_ob.location = txt_ob.location
            new_ob.location.x += cur_x_offset
            new_ob.location.y += cur_y_offset
            new_ob.location.z += cur_z_offset
            
            cur_x_offset += self.x_text_offset
            cur_y_offset += self.y_text_offset
            cur_z_offset += self.z_text_offset

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
