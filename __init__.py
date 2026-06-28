bl_info = {
    "name": "IcePick",
    "author": "Rheez",
    "version": (0, 4, 0),
    "blender": (5, 0, 0),
    "location": "View3D",
    "description": "Fast Texture Paint Palette System",
    "category": "Paint",
}

import bpy
import colorsys

from bpy.types import (
    Operator,
    PropertyGroup,
)

from bpy.props import (
    FloatVectorProperty,
    IntProperty,
    CollectionProperty,
    StringProperty,
)


# ------------------------------------------------------------
# PAINT COLOR HELPERS
# ------------------------------------------------------------

def get_paint(context):
    return getattr(
        context.tool_settings,
        "image_paint",
        None
    )


def get_paint_color(context):

    paint = get_paint(context)

    if not paint:
        return (1.0, 1.0, 1.0)

    ups = paint.unified_paint_settings

    if ups.use_unified_color:
        return tuple(ups.color)

    if paint.brush:
        return tuple(paint.brush.color)

    return (1.0, 1.0, 1.0)


def set_paint_color(context, color):

    paint = get_paint(context)

    if not paint:
        return

    ups = paint.unified_paint_settings

    if ups.use_unified_color:
        ups.color = color

    elif paint.brush:
        paint.brush.color = color


# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------

class IP_ColorSlot(PropertyGroup):

    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0),
    )


class IP_Palette(PropertyGroup):

    name: StringProperty(
        name="Palette Name",
        default="New Palette"
    )

    colors: CollectionProperty(
        type=IP_ColorSlot
    )


# ------------------------------------------------------------
# INITIALIZATION
# ------------------------------------------------------------

def ensure(scene):

    if len(scene.icepick_palettes) > 0:
        return

    defaults = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (0.5, 0.5, 0.5),
        (1, 1, 1),
    ]

    for i in range(4):

        pal = scene.icepick_palettes.add()

        pal.name = f"Palette {i + 1}"

        for color in defaults:

            slot = pal.colors.add()
            slot.color = color


# ------------------------------------------------------------
# OPERATORS
# ------------------------------------------------------------
class IP_OT_capture_color(Operator):
    bl_idname = "icepick.capture_color"
    bl_label = "Capture Current Paint Color"

    def execute(self, context):

        scn = context.scene

        ensure(scn)

        pal = scn.icepick_palettes[
            scn.icepick_active_palette
        ]

        pal.colors[
            scn.icepick_active_slot
        ].color = get_paint_color(context)

        self.report(
            {'INFO'},
            "Captured Paint Color"
        )

        return {'FINISHED'}

class IP_OT_select_slot(Operator):
    bl_idname = "icepick.select_slot"
    bl_label = "Select Slot"

    slot_index: IntProperty()

    def execute(self, context):

        scn = context.scene

        ensure(scn)

        scn.icepick_active_slot = self.slot_index

        pal = scn.icepick_palettes[
            scn.icepick_active_palette
        ]

        set_paint_color(
            context,
            pal.colors[self.slot_index].color
        )

        return {'FINISHED'}
    class IP_OT_add_palette(Operator):
        bl_idname = "icepick.add_palette"
        bl_label = "Add Palette"

    def execute(self, context):

        scn = context.scene

        defaults = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1),
            (0.5, 0.5, 0.5),
            (1, 1, 1),
        ]

        pal = scn.icepick_palettes.add()

        pal.name = f"Palette {len(scn.icepick_palettes)}"

        for color in defaults:
            slot = pal.colors.add()
            slot.color = color

        scn.icepick_active_palette = (
            len(scn.icepick_palettes) - 1
        )

        self.report(
            {'INFO'},
            f"Created {pal.name}"
        )

        return {'FINISHED'}


class IP_OT_delete_palette(Operator):
    bl_idname = "icepick.delete_palette"
    bl_label = "Delete Palette"

    def execute(self, context):

        scn = context.scene

        if len(scn.icepick_palettes) <= 1:

            self.report(
                {'WARNING'},
                "Cannot delete last palette"
            )

            return {'CANCELLED'}

        idx = scn.icepick_active_palette

        scn.icepick_palettes.remove(idx)

        scn.icepick_active_palette = max(
            0,
            min(
                idx,
                len(scn.icepick_palettes) - 1
            )
        )

        return {'FINISHED'}


class IP_OT_next_palette(Operator):
    bl_idname = "icepick.next_palette"
    bl_label = "Next Palette"

    def execute(self, context):

        scn = context.scene

        ensure(scn)

        scn.icepick_active_palette += 1

        if scn.icepick_active_palette >= len(
            scn.icepick_palettes
        ):
            scn.icepick_active_palette = 0
            
        pal = scn.icepick_palettes[
            scn.icepick_active_palette
            
         ]
         
        self.report(
            {'INFO'},
            f"[{scn.icepick_active_palette + 1}/{len(scn.icepick_palettes)}] {pal.name}"
            )

        return {'FINISHED'}

class IP_OT_add_palette(Operator):
    bl_idname = "icepick.add_palette"
    bl_label = "Add Palette"

    def execute(self, context):

        scn = context.scene

        defaults = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1),
            (0.5, 0.5, 0.5),
            (1, 1, 1),
        ]

        pal = scn.icepick_palettes.add()

        pal.name = f"Palette {len(scn.icepick_palettes)}"

        for color in defaults:
            slot = pal.colors.add()
            slot.color = color

        scn.icepick_active_palette = (
            len(scn.icepick_palettes) - 1
        )

        self.report(
            {'INFO'},
            f"Created {pal.name}"
        )

        return {'FINISHED'}


class IP_OT_delete_palette(Operator):
    bl_idname = "icepick.delete_palette"
    bl_label = "Delete Palette"

    def execute(self, context):

        scn = context.scene

        if len(scn.icepick_palettes) <= 1:

            self.report(
                {'WARNING'},
                "Cannot delete last palette"
            )

            return {'CANCELLED'}

        idx = scn.icepick_active_palette

        scn.icepick_palettes.remove(idx)

        scn.icepick_active_palette = max(
            0,
            min(
                idx,
                len(scn.icepick_palettes) - 1
            )
        )

        return {'FINISHED'}

class IP_OT_prev_palette(Operator):
    bl_idname = "icepick.prev_palette"
    bl_label = "Previous Palette"

    def execute(self, context):

        scn = context.scene

        ensure(scn)

        scn.icepick_active_palette -= 1

        if scn.icepick_active_palette < 0:
            scn.icepick_active_palette = (
                len(scn.icepick_palettes) - 1
            )
            
        pal = scn.icepick_palettes[
            scn.icepick_active_palette
            ]
            
        self.report(
            {'INFO'},
            f"[{scn.icepick_active_palette + 1}/{len(scn.icepick_palettes)}] {pal.name}"
            )

        return {'FINISHED'}

class IP_OT_sort_palette(Operator):
    bl_idname = "icepick.sort_palette"
    bl_label = "Sort Palette"

    mode: StringProperty()

    def execute(self, context):

        scn = context.scene

        ensure(scn)

        pal = scn.icepick_palettes[
            scn.icepick_active_palette
        ]

        colors = [
            tuple(slot.color)
            for slot in pal.colors
        ]

        if self.mode == "HUE":

            colors.sort(
                key=lambda c:
                colorsys.rgb_to_hsv(*c)[0]
            )

        elif self.mode == "SAT":

            colors.sort(
                key=lambda c:
                colorsys.rgb_to_hsv(*c)[1]
            )

        elif self.mode == "VAL":

            colors.sort(
                key=lambda c:
                colorsys.rgb_to_hsv(*c)[2]
            )

        elif self.mode == "LUM":

            colors.sort(
                key=lambda c:
                (
                    0.2126 * c[0] +
                    0.7152 * c[1] +
                    0.0722 * c[2]
                )
            )

        for i, color in enumerate(colors):
            pal.colors[i].color = color

        self.report(
            {'INFO'},
            f"Sorted by {self.mode}"
        )

        return {'FINISHED'}
    
class IP_OT_drag_slot(Operator):
    bl_idname = "icepick.drag_slot"
    bl_label = "Drag Slot Selector"

    start_x = 0
    start_slot = 0
    current_slot = 0

    def invoke(self, context, event):

        scn = context.scene

        ensure(scn)

        self.start_x = event.mouse_x
        self.start_slot = scn.icepick_active_slot
        self.current_slot = self.start_slot

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):

        if event.type == 'MOUSEMOVE':

            delta = event.mouse_x - self.start_x

            slot = self.start_slot + int(delta / 50)

            slot = max(0, min(7, slot))

            if slot != self.current_slot:

                self.current_slot = slot

                scn = context.scene

                scn.icepick_active_slot = slot

                pal = scn.icepick_palettes[
                    scn.icepick_active_palette
                ]

                set_paint_color(
                    context,
                    pal.colors[slot].color
                )

                self.report(
                    {'INFO'},
                    f"Slot {slot + 1}"
                )

        elif event.type == 'E' and event.value == 'RELEASE':

            return {'FINISHED'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}


class IP_OT_popup(Operator):
    bl_idname = "icepick.popup"
    bl_label = "IcePick"

    def invoke(self, context, event):

        ensure(context.scene)

        return context.window_manager.invoke_popup(
            self,
            width=450
        )

    def draw(self, context):

        scn = context.scene

        ensure(scn)

        pal = scn.icepick_palettes[
            scn.icepick_active_palette
        ]

        layout = self.layout

        layout.prop(
            pal,
            "name",
            text=""
        )

        layout.label(
            text=f"Palette {scn.icepick_active_palette + 1}"
        )

        layout.label(
            text=f"Slot {scn.icepick_active_slot + 1}"
        )

        row = layout.row(align=True)

        row.operator(
            "icepick.prev_palette",
            text="<"
        )

        row.operator(
            "icepick.next_palette",
            text=">"
        )
    
        row = layout.row(align=True)
        
        row.operator(
        "icepick.add_palette",
        text="+ New"
        
        )
        
        row.operator(
        "icepick.delete_palette",
        text="Delete"
        
        )
        layout.label(text="Sort Slots")

        row = layout.row(align=True)

        op = row.operator(
            "icepick.sort_palette",
            text="Hue"
        )
        op.mode = "HUE"

        op = row.operator(
            "icepick.sort_palette",
            text="Sat"
        )
        op.mode = "SAT"

        op = row.operator(
            "icepick.sort_palette",
            text="Val"
        )
        op.mode = "VAL"

        op = row.operator(
            "icepick.sort_palette",
            text="Lum"
        )
        op.mode = "LUM"
            
        layout.operator(
            "icepick.capture_color",
            text="Capture Current Paint Color"
        )

        layout.separator()

        box = layout.box()

        labels = [
            "ONE",
            "TWO",
            "THREE",
            "FOUR",
            "FIVE",
            "SIX",
            "SEVEN",
            "EIGHT",
        ]

        for row_start in (0, 4):

            row = box.row(align=True)

            for i in range(row_start, row_start + 4):

                col = row.column(align=True)

                op = col.operator(
                    "icepick.select_slot",
                    text=labels[i]
                )

                op.slot_index = i

                col.prop(
                    pal.colors[i],
                    "color",
                    text=""
                )

        layout.separator()

        layout.label(
            text="Active Slot Color"
        )

        layout.prop(
            pal.colors[
                scn.icepick_active_slot
            ],
            "color",
            text=""
        )

    def execute(self, context):
        return {'FINISHED'}


# ------------------------------------------------------------
# KEYMAPS
# ------------------------------------------------------------

addon_keymaps = []


def register_keymaps():

    wm = bpy.context.window_manager

    kc = wm.keyconfigs.addon

    if not kc:
        return

    km = kc.keymaps.new(
        name="3D View",
        space_type='VIEW_3D'
    )
    km.keymap_items.new(
    "icepick.drag_slot",
    type='E',
    value='PRESS'
)

    keys = [
        "ONE",
        "TWO",
        "THREE",
        "FOUR",
        "FIVE",
        "SIX",
        "SEVEN",
        "EIGHT",
    ]

    for i, key in enumerate(keys):

        kmi = km.keymap_items.new(
            "icepick.select_slot",
            type=key,
            value='PRESS',
            shift=True
        )

        kmi.properties.slot_index = i

    km.keymap_items.new(
        "icepick.next_palette",
        type='W',
        value='PRESS',
        alt=True
    )

    km.keymap_items.new(
        "icepick.prev_palette",
        type='W',
        value='PRESS',
        alt=True,
        shift=True
    )

    km.keymap_items.new(
        "icepick.popup",
        type='B',
        value='PRESS'
    )

    addon_keymaps.append(km)


def unregister_keymaps():

    wm = bpy.context.window_manager

    kc = wm.keyconfigs.addon

    if kc:

        for km in addon_keymaps:
            kc.keymaps.remove(km)

    addon_keymaps.clear()


# ------------------------------------------------------------
# REGISTER
# ------------------------------------------------------------

classes = (
    IP_ColorSlot,
    IP_Palette,
    IP_OT_select_slot,
    IP_OT_next_palette,
    IP_OT_prev_palette,

    IP_OT_add_palette,
    IP_OT_delete_palette,
    IP_OT_sort_palette,

    IP_OT_capture_color,
    IP_OT_drag_slot,
    IP_OT_popup,
)

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.icepick_palettes = CollectionProperty(
        type=IP_Palette
    )

    bpy.types.Scene.icepick_active_palette = IntProperty(
        default=0
    )

    bpy.types.Scene.icepick_active_slot = IntProperty(
        default=0
    )

    # Blender 5 addon-safe.
    # Don't access bpy.context.scene here.
    # Don't access bpy.data.scenes here.

    try:
        register_keymaps()
    except Exception as e:
        print("IcePick keymap registration:", e)


def unregister():

    try:
        unregister_keymaps()
    except:
        pass

    if hasattr(bpy.types.Scene, "icepick_palettes"):
        del bpy.types.Scene.icepick_palettes

    if hasattr(bpy.types.Scene, "icepick_active_palette"):
        del bpy.types.Scene.icepick_active_palette

    if hasattr(bpy.types.Scene, "icepick_active_slot"):
        del bpy.types.Scene.icepick_active_slot

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    # Addon-install safe:
    # Don't access bpy.context.scene
    # Don't access bpy.data.scenes

    try:
        register_keymaps()
    except Exception as e:
        print("IcePick keymap registration:", e)
    try:
        register_keymaps()
    except Exception as e:
        print("IcePick keymap registration:", e)


def unregister():

    try:
        unregister_keymaps()
    except:
        pass

    if hasattr(bpy.types.Scene, "icepick_palettes"):
        del bpy.types.Scene.icepick_palettes

    if hasattr(bpy.types.Scene, "icepick_active_palette"):
        del bpy.types.Scene.icepick_active_palette

    if hasattr(bpy.types.Scene, "icepick_active_slot"):
        del bpy.types.Scene.icepick_active_slot

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


def unregister():

    try:
        unregister_keymaps()
    except:
        pass

    if hasattr(bpy.types.Scene, "icepick_palettes"):
        del bpy.types.Scene.icepick_palettes

    if hasattr(bpy.types.Scene, "icepick_active_palette"):
        del bpy.types.Scene.icepick_active_palette

    if hasattr(bpy.types.Scene, "icepick_active_slot"):
        del bpy.types.Scene.icepick_active_slot

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)