# separate letters and keep kerning
# notes: This came from a blenderartists response to my initial addon post.
# Interesting property is that it preserves text character traits which I 
# think would be pretty important to my own addon.

# I think there should be a way to use this will remaining a split up of words instead
# of individual letters like this script does. 

import bpy
sce = bpy.context.scene
txt = bpy.context.object

spline = 0
spaces = []

if txt.type == 'FONT':
    pos = txt.location[0]
    col = txt.dimensions[0]
    if txt.data.align == 'CENTER': pos -= col / 2
    if txt.data.align == 'RIGHT': pos -= col

    for i in range(len(txt.data.body)):
        chr = txt.data.body[i:i+1]
        if chr.isspace(): continue
        dat = txt.data.copy()
        dat.body = chr
        name = "let_%03d_%s" % (dat.splines[spline].character_index, dat.body)
        let = bpy.data.objects.new(name, dat)
        sce.objects.link(let)
        sce.frame_set(sce.frame_current)
        pos = txt.data.splines[spline].bezier_points[0].co
        let.location = pos - let.data.splines[0].bezier_points[0].co
        spline += len((let.data.splines))

    sce.objects.active = txt
    txt.select = True