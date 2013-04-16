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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
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
    "location": 'View3D > Tools',
    "description": "Splits up text objects into multiple words or characters",
    "warning": "",
    "category": "Text"
}


class TextSplitOperator(bpy.types.Operator):
    """Text split operator"""
    bl_idname = "text.split"
    bl_label = "Text Splitter"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    choices = [("word", "word", "word",),
              ("character", "character", "character",)]

    split_by_enum = bpy.props.EnumProperty(name="Split By Character or Word",
                                description="Split by character or letter",
                                items=choices)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        is_valid = ob is not None and ob.type == 'FONT'
        return is_valid

    def word_by_word_create(self, scn, target_txt):

        spline = 0
        target_words = target_txt.data.body.split()

        for target_word in target_words:
            new_txt_data = target_txt.data.copy()
            new_txt_data.body = target_word
            new_word_name = "txt_%s" % target_word
            new_word_ob = bpy.data.objects.new(new_word_name, new_txt_data)
            scn.objects.link(new_word_ob)
            scn.frame_set(scn.frame_current)

            # place the new word in the right spot
            pos = target_txt.data.splines[spline].bezier_points[0].co
            new_loc = pos - new_txt_data.splines[0].bezier_points[0].co
            new_word_ob.location = new_loc
            spline += len(new_word_ob.data.splines)

    def letter_by_letter_create(self, scn, target_txt):
        spline = 0

        pos = target_txt.location[0]
        col = target_txt.dimensions[0]
        if target_txt.data.align == 'CENTER':
            pos -= col / 2
        if target_txt.data.align == 'RIGHT':
            pos -= col

        # text creation logic for individual letters.
        letter_count = len(target_txt.data.body)

        for i in range(letter_count):

            # core creation of the new text object data.
            chr = target_txt.data.body[i:i+1]
            if chr.isspace():
                continue
            new_txt_dat = target_txt.data.copy()
            new_txt_dat.body = chr

            # text creation step
            name = "text_%s" % new_txt_dat.body
            new_txt_ob = bpy.data.objects.new(name, new_txt_dat)
            scn.objects.link(new_txt_ob)
            scn.frame_set(scn.frame_current)

            # place the new character text ob in the right spot.
            pos = target_txt.data.splines[spline].bezier_points[0].co
            new_loc = pos - new_txt_ob.data.splines[0].bezier_points[0].co
            new_txt_ob.location = new_loc

            spline += len((new_txt_ob.data.splines))

    def execute(self, context):
        scn = bpy.context.scene
        target_txt = bpy.context.object
        if "word" == self.split_by_enum:
            self.word_by_word_create(scn, target_txt)
        else:
            self.letter_by_letter_create(scn, target_txt)
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
