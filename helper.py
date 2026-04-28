from manim import *


class Node(VGroup):
    def __init__(
        self,
        value=" ",
        label=True,
        label_value=" ",
        label_pos=UP,
        is_rect=True,
        width=0.6,
        height=0.6,
        radius=0.3,
        font_size=22,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.value = value
        self.label = label
        self.label_value = label_value
        self.label_pos = label_pos
        self.is_rect = is_rect
        self.font_size = font_size
        self.label_size = font_size * 0.7

        node_cell = (
            Rectangle(width=width, height=height).set_fill(BLACK, opacity=1)
            if is_rect
            else Circle(radius=radius, color=WHITE).set_fill(BLACK, opacity=1)
        )
        node_text = Text(str(value), font_size=font_size, z_index=1).move_to(
            node_cell.get_center()
        )
        node_label = Text(str(label_value), font_size=self.label_size).next_to(
            node_cell, label_pos
        )

        self.add(node_cell, node_text)
        if label:
            self.add(node_label)

    def set_focus(self, color=GREEN, buff=0.1, buffer_factor=1):
        return (
            SurroundingRectangle(self[0], buff=buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
            if self.is_rect
            else Circle()
            .surround(self[0], buffer_factor=0.8 * buffer_factor)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
        )

    def set_node(self, scene=None, value=None, label=None, fill=None):
        value = self.value if value is None else value
        label = self.label_value if label is None else label

        bg = self.set_focus()
        if scene:
            scene.play(Write(bg))

        self[1].become(
            Text(str(value), font_size=self.font_size, z_index=1).move_to(
                self[0].get_center()
            )
        )

        if self.label:
            self[2].become(
                Text(str(label), font_size=self.label_size).next_to(
                    self[0], self.label_pos
                )
            )

        if fill:
            self[0].set_fill(fill, opacity=1)

        if scene:
            scene.play(FadeOut(bg))


class Vector(VGroup):
    def __init__(
        self,
        data=[" "],
        dir_right=True,
        index=True,
        index_from=0,
        index_step=1,
        index_pos=UP,
        is_rect=True,
        width=0.6,
        height=0.6,
        radius=0.3,
        font_size=22,
        buff=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.data = data
        self.size = len(data)

        self.is_rect = is_rect
        self.cell_width = width
        self.cell_height = height
        self.cell_radius = radius

        self.index = index
        self.index_from = index_from
        self.index_step = index_step
        self.index_pos = index_pos

        self.dir_right = dir_right
        self.direction = RIGHT if dir_right else UP

        self.font_size = font_size
        self.index_size = font_size * 0.7

        self.buff = buff

        self.add(*self._create_nodes(data))
        self._update_indices()

    def _get_indices_range(self):
        return range(
            self.index_from,
            self.index_from + (self.index_step * self.size),
            self.index_step,
        )

    def _create_nodes(self, data):
        return VGroup(
            *[
                Node(
                    value=str(x),
                    label=self.index,
                    label_value=str(i),
                    label_pos=self.index_pos,
                    width=self.cell_width,
                    height=self.cell_height,
                    radius=self.cell_radius,
                    is_rect=self.is_rect,
                    font_size=self.font_size,
                )
                for i, x in enumerate(data)
            ]
        ).arrange(self.direction, buff=self.buff)

    def _update_indices(self):
        if not self.index:
            return

        for idx, index in enumerate(self._get_indices_range()):
            self[idx].set_node(label=index)

    def _get_arc(self, arcfrom, arcto):
        return ArcBetweenPoints(
            self[arcfrom][0].get_center(), self[arcto][0].get_center(), angle=-PI
        )

    def set_focus(self, start=0, end=None, color=GREEN, buff=0.1, buffer_factor=1):
        end = start + 1 if end is None else end + 1
        node_cells = VGroup(*[node[0] for node in self[start:end]])
        return (
            SurroundingRectangle(node_cells, buff=buff)
            .set_fill(color, opacity=0.3)
            .set_stroke(color, width=3)
        )

    def swap(self, scene, swap_from, swap_to):
        if swap_from == swap_to:
            return

        arcup = self._get_arc(swap_from, swap_to)
        arcdwn = self._get_arc(swap_to, swap_from)

        scene.play(
            MoveAlongPath(self[swap_from][1], arcup),
            MoveAlongPath(self[swap_to][1], arcdwn),
        )

        self[swap_from].set_node(value=self.data[swap_to])
        self[swap_to].set_node(value=self.data[swap_from])
        self.data[swap_from], self.data[swap_to] = (
            self.data[swap_to],
            self.data[swap_from],
        )
