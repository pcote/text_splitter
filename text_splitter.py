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

bl_info = {
    'name': 'Text Splitter',
    'author': 'Phil Cote, cotejrp1',
    'version': (0, 1),
    "blender": (2, 66, 3),
    "location": 'View3D > ',
    "description": "Splits up text objects into multiple words or characters",
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

    choices = [("word", "word", "word",),
              ("character", "character", "character",)]

    split_by_enum = bpy.props.EnumProperty(name="Split By Character or Letter",
                                description="Option to split by character or letter",
                                items=choices)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        is_valid = ob is not None and ob.type == 'FONT'
        return is_valid

    def execute(self, context):
        scn = bpy.context.scene
        target_txt = bpy.context.object
        
        spline = 0
        
        pos = target_txt.location[0]
        col = target_txt.dimensions[0]
        if target_txt.data.align == 'CENTER': pos -= col / 2
        if target_txt.data.align == 'RIGHT': pos -= col
        
        # text creation logic for individual letters.
        target_size = len(target_txt.data.body)
        
        for i in range(target_size):
            
            # core creation of the new text object data.
            chr = target_txt.data.body[i:i+1]
            if chr.isspace(): continue
            new_txt_dat = target_txt.data.copy()
            new_txt_dat.body = chr
            
            # boilerplate text creation
            name = "text_%s" % new_txt_dat.body
            new_txt_ob = bpy.data.objects.new(name, new_txt_dat)
            scn.objects.link(new_txt_ob)
            scn.frame_set(scn.frame_current)
            
            # place the new character text ob in the right spot.
            pos = target_txt.data.splines[spline].bezier_points[0].co
            new_txt_ob.location = pos - new_txt_ob.data.splines[0].bezier_points[0].co
            
            spline += len((new_txt_ob.data.splines))
    
        scn.objects.active = target_txt
        target_txt.select = True

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