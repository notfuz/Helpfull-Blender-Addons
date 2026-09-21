import bpy

bl_info = {
    "name": "Fly & Lock Camera",
    "author": "notfuz",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N-Panel) > Fly Cam",
    "description": "Enters Walk/Fly navigation and permanently locks the active camera to your final view position upon exiting.",
    "warning": "",
    "doc_url": "",
    "category": "Camera",
}

class VIEW3D_OT_fly_and_lock_camera_addon(bpy.types.Operator):
    """Enter Fly/Walk mode and force-lock the camera to the final position upon exit"""
    bl_idname = "view3d.fly_and_lock_camera_addon"
    bl_label = "Fly & Lock Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if context.mode not in {'OBJECT', 'EDIT'}: 
            return {'PASS_THROUGH'}

        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'SPACE', 'RET'}:
            space = context.space_data
            camera = context.scene.camera
            
            if space and space.type == 'VIEW_3D' and camera:
                view_matrix = space.region_3d.view_matrix.inverted()
                camera.matrix_world = view_matrix
                
                context.window_manager.event_timer_remove(self._timer)
                self.report({'INFO'}, "Camera locked to final fly position!")
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        camera = context.scene.camera
        if not camera:
            self.report({'ERROR'}, "No active camera found in the scene.")
            return {'CANCELLED'}

        space = context.space_data
        if space and space.type == 'VIEW_3D':
            if space.region_3d.view_perspective != 'CAMERA':
                space.region_3d.view_perspective = 'CAMERA'

        bpy.ops.view3d.walk("INVOKE_DEFAULT")
        
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class VIEW3D_PT_fly_lock_panel_addon(bpy.types.Panel):
    """Creates a dedicated tab in the N-Menu sidebar"""
    bl_label = "Camera Controls"
    bl_idname = "VIEW3D_PT_fly_lock_panel_addon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fly Cam'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.scale_y = 1.5  
        row.operator("view3d.fly_and_lock_camera_addon", icon='TRACKING')

def register():
    bpy.utils.register_class(VIEW3D_OT_fly_and_lock_camera_addon)
    bpy.utils.register_class(VIEW3D_PT_fly_lock_panel_addon)

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_fly_and_lock_camera_addon)
    bpy.utils.unregister_class(VIEW3D_PT_fly_lock_panel_addon)

if __name__ == "__main__":
    register()