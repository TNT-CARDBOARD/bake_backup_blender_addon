bl_info = {
    "name": "Auto Bake Backup",
    "author": "TNT_CARDBOARD",
    "version": (1, 0),
    "blender": (4, 2, 3),
    "location": "Preferences > Add-ons",
    "description": "Automatically saves a backup of images after a Bake operation to a 'bake_backups' folder.",
    "warning": "Experimental",
    "category": "System",
}

import bpy
import os
from datetime import datetime
from bpy.app.handlers import persistent

@persistent
def backup_bake_images(scene):
    blend_filepath = bpy.data.filepath
    if not blend_filepath:
        base_dir = bpy.app.tempdir
    else:
        base_dir = os.path.dirname(blend_filepath)
    backup_dir = os.path.join(base_dir, "bake_backups")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for img in bpy.data.images:
        if not img.has_data:
            continue
        name = img.name if img.name else f"Image_{timestamp}"
        fmt = getattr(img, 'file_format', 'PNG').lower()
        ext = fmt if fmt.startswith('.') else f".{fmt}"
        if ext not in ['.png', '.jpg', '.jpeg', '.exr', '.tga', '.bmp', '.dds']:
            ext = '.png'

        safe_name = ''.join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
        backup_path = os.path.join(backup_dir, f"{safe_name}_{timestamp}{ext}")

        try:
            img.save_render(filepath=backup_path)
            print(f"[Auto Bake Backup] Saved {img.name} to {backup_path}")
        except Exception as e:
            print(f"[Auto Bake Backup] Failed to save {img.name}: {e}")


def register():
    bpy.app.handlers.object_bake_complete.append(backup_bake_images)


def unregister():
    if backup_bake_images in bpy.app.handlers.object_bake_complete:
        bpy.app.handlers.object_bake_complete.remove(backup_bake_images)


if __name__ == "__main__":
    register()
