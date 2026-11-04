from build123d import *
from ocp_vscode import *
from enum import IntFlag


def height(part):
    return part.bounding_box().size.Z

def width(part):
    return part.bounding_box().size.X

def top_of(part): 
    return part.bounding_box().max.Z

def bottom_of(part):
    return part.bounding_box().min.Z

def front_of(part):
    return part.bounding_box().min.Y

def back_of(part):
    return part.bounding_box().max.Y

def left_of(part):
    return part.bounding_box().min.X

def right_of(part):
    return part.bounding_box().max.X

def align_to_bottom(part, other):
    return bottom_of(part) - bottom_of(other)

def align_to_top(part, other):
    return top_of(part) - top_of(other)

def align_to_right(part, other):
    return right_of(part) - right_of(other)

def align_to_left(part, other):
    return left_of(part) - left_of(other)

def align_to_front(part, other):
    # other += Pos(0, front_of(other) - front_of(part), 0) * part
    return front_of(part) - front_of(other)

def align_to_back(part, other):
    # other += Pos(0, back_of(other) - back_of(part), 0) * part
    return back_of(part) - back_of(other)

def stack_up(tostack):
    stack = tostack[0]
    for part in tostack[1:]:
        top_z = stack.bounding_box().max.Z
        stack += Pos(0, 0, top_z + part.bounding_box().size.Z/2) * part
    return stack

def stack_left(tostack):
    stack = tostack[0]
    for part in tostack[1:]:
        left_x = stack.bounding_box().min.X
        offset = left_x - part.bounding_box().size.X/2
        stack += Pos(offset, 0, 0) * part
    return stack

class Anchor(IntFlag):
    CENTER = 0

    LEFT   = 1 << 0
    RIGHT  = 1 << 1

    BACK   = 1 << 2
    FRONT  = 1 << 3

    BOTTOM = 1 << 4
    TOP    = 1 << 5

TOP    = Anchor.TOP
BOTTOM = Anchor.BOTTOM
LEFT   = Anchor.LEFT
RIGHT  = Anchor.RIGHT
FRONT  = Anchor.FRONT
BACK   = Anchor.BACK
CENTER = Anchor.CENTER


class Positioner:

    @staticmethod
    def anchor_point(
        obj: Part,
        anchor: Anchor = CENTER,
    ) -> Vector:
        """
        Calculate the world-space point associated with a bbox anchor.
        """

        bb = obj.bounding_box()

        # X

        if anchor & LEFT:
            x = bb.min.X
        elif anchor & RIGHT:
            x = bb.max.X
        else:
            x = (bb.min.X + bb.max.X) / 2

        # Y

        if anchor & FRONT:
            y = bb.min.Y
        elif anchor & BACK:
            y = bb.max.Y
        else:
            y = (bb.min.Y + bb.max.Y) / 2

        # Z

        if anchor & BOTTOM:
            z = bb.min.Z
        elif anchor & TOP:
            z = bb.max.Z
        else:
            z = (bb.min.Z + bb.max.Z) / 2

        return Vector(x, y, z)

    @classmethod
    def attach(
        cls,
        obj: Part,
        obj_anchor: Anchor,
        target: Part,
        target_anchor: Anchor,
        offset=(0, 0, 0),
    ) -> Part:
        """
        Move obj so that:

            obj_anchor --> target_anchor
        """

        p_obj = cls.anchor_point(obj, obj_anchor)
        p_target = cls.anchor_point(target, target_anchor)

        translation = (
            p_target
            - p_obj
            + Vector(*offset)
        )

        return obj.moved(Location(translation))


# ======================================================================
# Fluent Wrapper
# ======================================================================

class Positioned:
    def __init__(self, part: Part):
        self.part = part

    def to(
        self,
        target: Part,
        my: Anchor,
        their: Anchor,
        offset=(0, 0, 0),
    ):
        self.part = Positioner.attach(
            self.part,
            my,
            target,
            their,
            offset,
        )

        return self
