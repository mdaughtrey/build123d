# %%
from itertools import product

from build123d import *
from ocp_vscode import *

from models.helpers import *

# %%
class ModelESP32D1Mini(BasePartObject):
    pcb_x = 39
    pcb_y = 31.35
    pcb_z = 1.6
    def __init__(
        self,
        rotation: RotationLike = (0, 0, 0),
        align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD
    ):
        # print(f"pcb {self.pcb().bounding_box()}")
        # print(f"wifi {self.wifi_module().bounding_box()}")
        pcb = self.pcb()
        part = pcb
        part += Pos(align_to_left(pcb, wifi := self.wifi_module()), 0, align_to_bottom(pcb, wifi) + self.pcb_z) * wifi
        part += Pos(align_to_right(pcb, usb := self.usb_connector()) + 1.3, 0, align_to_bottom(pcb, usb) + self.pcb_z) * usb
        led = Box(1.4, 3.3, 0.6)
        part += Pos(align_to_right(pcb, led) - 4.3, align_to_back(pcb, led) - 0.8, align_to_bottom(pcb, led) + self.pcb_z) * led
        part += Pos(align_to_right(pcb, led) - 1.8, align_to_back(pcb, led) - 0.8, align_to_bottom(pcb, led) + self.pcb_z) * led
        # Pushbutton
        pushbutton = Box(4.5, 3.8, 1.8)
        part += Pos(align_to_right(pcb, pushbutton) - 0.8, align_to_front(pcb, pushbutton) + 1.9, align_to_bottom(pcb, pushbutton) + self.pcb_z) * pushbutton

        usb_chip = Box(4.8, 4.8, 0.72)
        part += Pos(align_to_right(pcb, usb_chip) - 6.3, align_to_front(pcb, usb_chip) + 6.0, align_to_bottom(pcb, usb_chip) + self.pcb_z) * usb_chip
        # Misc
        part += Pos(align_to_right(pcb, misc := Box(1.25, 2.06, 1)) - 8.75, align_to_back(pcb, misc) - 10.75, align_to_bottom(pcb, misc) + self.pcb_z) * misc
        part += Pos(align_to_right(pcb, misc := Box(3, 2.25, 1.2)) - 1.54, align_to_back(pcb, misc) - 6, align_to_bottom(pcb, misc) + self.pcb_z) * misc

        super().__init__(part, rotation=rotation, align=align, mode=mode)


    def usb_connector(self):
        return Box(5.6, 7.5, 2.2)

    def wifi_module(self):
        wm = Box(25.55, 17.87, 0.88)
        wm += Pos(align_to_right(wm, module := Box(17.64, 15.68, 2.24)) - 0.75, 0, 0.88) * module
        return wm

    def pcb(self):
        corner_cutout = 2.5
        pcb_points = [(-self.pcb_x/2, -(self.pcb_y/2) + corner_cutout),
            (-self.pcb_x/2, (self.pcb_y/2) - corner_cutout),
            (-self.pcb_x/2+corner_cutout, self.pcb_y/2),
            (self.pcb_x/2, self.pcb_y/2),
            (self.pcb_x/2, (self.pcb_y/2) - corner_cutout), 
            (self.pcb_x/2, -(self.pcb_y/2) + 2.5),
            (self.pcb_x/2 - 6.5, -self.pcb_y/2 + 2.5),
            (self.pcb_x/2 - 6.5, -self.pcb_y/2),
            (-self.pcb_x/2 + corner_cutout, -(self.pcb_y/2)),
            (-self.pcb_x/2, -(self.pcb_y/2) + corner_cutout)
        ]
        self.label = "ModelESP32D1Mini"
        pcb = Polyline(pcb_points)
        pcb = make_face(Plane.XY * pcb)

        # Holes
        coords = product(range(10), [self.pcb_y/2 - 1.8, self.pcb_y/2 - 1.8 - 2.54, -self.pcb_y/2 + 1.8, -self.pcb_y/2 + 1.8 + 2.54])
        holes = [Circle(0.5).translate((-(self.pcb_x/2) + 7.9 + (x * 2.54), y)) for x, y in coords]

        pcb -= holes
        pcb = extrude(pcb, self.pcb_z)
        return pcb

# model = ModelESP32D1Mini()
# show(model)

# %%



