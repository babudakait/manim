from manim import *
from helper import Vector

BUBBLE_SORT = """
void bubble_sort(int *arr, size_t n){
  int swapped;
  for (size_t i=0; i<n-1; i++){
    swapped = 0;
    for (size_t j=0; j<n-i-1; j++){
      if (arr[j] > arr[j+1]){
        swap(&arr[j], &arr[j+1]);
        swapped = 1;
      }
    }
    if (!swapped) break;
  }
}
"""

SELECTION_SORT = """
void selection_sort(int *arr, size_t n){
  for (size_t i=0; i<n-1; i++){
    int minidx = i;
    for (size_t j=i+1; j<n; j++){
      if (arr[j] < arr[minidx])
	minidx = j;
    }
    if (minidx != i)
      swap(&arr[i], &arr[minidx]);
  }
}
"""


def show_code(scene, code, language="C", scale=0.8, move_to=RIGHT):
    code = Code(code_string=code, language=language).scale(0.9)
    scene.play(Write(code))
    scene.wait(2)
    scene.play(code.animate.scale(scale).to_edge(move_to))
    scene.wait(1)
    return code


class BubbleSort(Scene):
    def construct(self):
        self.add(Text("Bubble Sort", font_size=30).to_edge(UP))
        
        code = show_code(self, BUBBLE_SORT)

        arr = Vector(data=[64, 34, 25, 12, 22, 11, 18]).next_to(
            code, LEFT, buff=0.6, aligned_edge=UP
        )
        self.play(Write(arr))
        self.wait(2)

        ilbl = Text("i", font_size=20).next_to(arr[0][2], UP, buff=0.2)
        self.play(Write(ilbl))

        n = arr.size
        for i in range(n):
            self.play(ilbl.animate.next_to(arr[i][2], UP, buff=0.2))
            cmp = arr.set_focus(0, 1, buff=0, color=BLUE)
            self.play(Write(cmp))
            swapped = False

            for j in range(0, n - i - 1):
                if j > 0:
                    self.play(cmp.animate.shift(RIGHT * arr.cell_width))

                if arr.data[j] > arr.data[j + 1]:
                    arr.swap(self, j, j + 1)
                    swapped = True

            self.play(Write(arr.set_focus(n - i - 1, buff=0)), FadeOut(cmp))

            if not swapped:
                break

        self.play(Write(arr.set_focus(buff=0)))
        self.wait(3)




class SelectionSort(Scene):
    def construct(self):
        self.add(Text("Selection Sort", font_size=30).to_edge(UP))
        
        code = show_code(self, SELECTION_SORT)

        arr = Vector(data=[64, 34, 25, 12, 22, 11, 18]).next_to(
            code, LEFT, buff=0.6, aligned_edge=UP
        )
        self.play(Write(arr))
        self.wait(2)

        n = arr.size
        for i in range(n - 1):
            minidx = i

            ibg = arr.set_focus(i, buff=0, color=RED)
            minbg = arr.set_focus(minidx, buff=0, color=GREEN)
            self.play(
                ibg.animate.move_to(arr[i][0].get_center()),
                minbg.animate.move_to(arr[minidx][0].get_center()),
            )

            for j in range(i + 1, n):
                if arr.data[j] < arr.data[minidx]:
                    minidx = j
                    self.play(minbg.animate.move_to(arr[minidx][0].get_center()))

            if minidx != i:
                arr.swap(self, i, minidx)

            self.play(FadeOut(minbg), FadeOut(ibg), Write(arr.set_focus(i, buff=0)))

        self.play(Write(arr.set_focus(n - 1, buff=0)))
        self.wait(3)
        
