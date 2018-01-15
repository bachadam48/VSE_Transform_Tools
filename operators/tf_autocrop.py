import bpy
import math

from .tf_utils import get_group_box
from .tf_utils import reposition_strip
from .tf_utils import reposition_transform_strip
from .tf_utils import get_nontransformed_strips
from .tf_utils import get_transform_strips

class TF_Autocrop(bpy.types.Operator):
    bl_idname = "sequencer.tf_autocrop"
    bl_label = "Collapse scene resolution to match clip size"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        if (scene.sequence_editor and
            context.space_data.type == 'SEQUENCE_EDITOR' and
            context.space_data.view_type == 'PREVIEW' and
            context.space_data.display_mode == 'IMAGE' and 
            len(scene.sequence_editor.sequences) > 0):
            return True
        return False
    
    def execute(self, context):
        scene = context.scene
        strips = list(scene.sequence_editor.sequences)
        
        i = 0
        while i < len(strips):
            if strips[i].mute or strips[i].type == 'SOUND':
                strips.pop(i)
            else:
                i += 1
        
        group_box = get_group_box(strips)
        
        min_left, max_right, min_bottom, max_top = group_box 

        total_width = max_right - min_left
        total_height = max_top - min_bottom
        
        nontransformed_strips = get_nontransformed_strips(strips)
        for strip in nontransformed_strips:
            reposition_strip(strip, group_box)
        
        transform_strips = get_transform_strips(strips)
        for strip in transform_strips:
            reposition_transform_strip(strip, group_box)
        
        scene.render.resolution_x = total_width
        scene.render.resolution_y = total_height

        return {'FINISHED'}
