# %%
from build123d import *
from ocp_vscode import *

# %%
class ModelPushbuttonJHF58(BasePartObject):
    body_x = 5.8
    body_y = 5.8
    body_z = 5.2
    shaft_length = 2.17 + 2.34
    leg_x = 0.6
    leg_y = 0.26
    leg_z = 3.36
    def __init__(
            self,
            rotation: RotationLike = (0, 0, 0),
            align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
            mode: Mode = Mode.ADD
        ):
        self.label = "ModelPushbuttonJHF58"

        with BuildPart() as part:
            with BuildSketch() as body:
                Rectangle(self.body_x, self.body_y)
            extrude(amount=self.body_z)
            with BuildSketch(body.faces().group_by(Axis.Z)[0]) as legs:
                with Locations((-1.28, 2.25), (0, 2.25), (1.28, 2.25), (-1.28, -2.25), (0, -2.25), (1.28, -2.25)):
                    Rectangle(self.leg_x, self.leg_y)
            extrude(amount=-self.leg_z)
            with BuildSketch(part.faces().group_by(Axis.Z)[-1]) as push0:
                Rectangle(3.45, 2.85)
            extrude(amount=2.17)
            with BuildSketch(part.faces().group_by(Axis.Z)[-1]) as push1:
                Rectangle(2.44, 2)
            extrude(amount=2.34)
        super().__init__(part.part, rotation=rotation, align=align, mode=mode)





# %%
class ModelPushbuttonJHF58Cutout(BasePartObject):
    clearance = 0.254
    body_x = ModelPushbuttonJHF58.body_x + clearance
    body_y = ModelPushbuttonJHF58.body_y + clearance
    body_z = ModelPushbuttonJHF58.body_z + clearance
    leg_x = ModelPushbuttonJHF58.leg_x + clearance
    leg_y = ModelPushbuttonJHF58.leg_y + clearance * 2
    leg_z = ModelPushbuttonJHF58.leg_z + clearance

    def __init__(
            self,
            rotation: RotationLike = (0, 0, 0),
            align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
            mode: Mode = Mode.ADD
        ):
        self.label = "ModelPushbuttonJHF58Cutout"

        with BuildPart() as part:
            with BuildSketch() as body:
                Rectangle(self.body_x, self.body_y)
            extrude(amount=self.body_z)
            with BuildSketch(body.faces().group_by(Axis.Z)[0]) as legs:
                with Locations((0, 2.25), (0, -2.25)):
                    Rectangle(self.body_x, self.leg_y)
            extrude(amount=-self.leg_z)
        super().__init__(part.part, rotation=rotation, align=align, mode=mode)


# cutout = ModelPushbuttonJHF58Cutout()
# print(cutout.clearance)
# show(ModelPushbuttonJHF58Cutout())


# %%
class ModelPushbuttonJHF58BigButton(BasePartObject):
    def __init__(
            self,
            rotation: RotationLike = (0, 0, 0),
            align: tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.CENTER),
            mode: Mode = Mode.ADD
        ):
        self.label = "ModelPushbuttonJHF58BigButton"

        part = Cylinder(5.9/2, 7)
        part -= Pos(0, 0, -(7-6.4)/2) * Box(3, 2, 6.4)

        super().__init__(part, rotation=rotation, align=align, mode=mode)




