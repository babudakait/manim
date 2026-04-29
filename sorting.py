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

INSERTION_SORT = """
void insertion_sort(int *arr, size_t n){
  for (size_t i=1; i<n-1; i++){
    int key = arr[i];
    int j = i-1;

    while (j >= 0 && key < arr[j]) j--;
    j = j+1;
    
    if (i != j){
      memmove(arr+j+1, arr+j, (i-j)*sizeof(int));
      arr[j] = key;
    }
  }
}
"""

LOMUTO_PARTITION = """
int lomuto_partition(int *arr, int low, int high){
  int pivot = arr[high];
  int i = low-1;

  for (int j = low; j <= high-1; j++){
    if (arr[j] < pivot){
      i++;
      swap(&arr[i], &arr[j]);
    }
  }
  swap(&arr[i+1], &arr[high]);
  return i+1;
}
"""

QUICKSORT = """
void quick_sort(int* arr, int low, int high) {
  if (low < high) {
    int pi = partition(arr, low, high);
    quick_sort(arr, low, pi - 1);
    quick_sort(arr, pi + 1, high);
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


class InsertionSort(Scene):
    def construct(self):
        self.add(Text("Insertion Sort", font_size=30).to_edge(UP))

        code = show_code(self, INSERTION_SORT, scale=0.75)

        arr = Vector(data=[64, 34, 25, 12, 22, 11, 18]).next_to(
            code, LEFT, buff=0.6, aligned_edge=UP
        )
        self.play(Write(arr))
        self.wait(2)

        ibg = arr.set_focus(1, buff=0, color=RED)

        n = arr.size
        for i in range(1, n):
            key = arr.data[i]
            j = i - 1

            jbg = arr.set_focus(i - 1, buff=0, color=BLUE)
            self.play(
                ibg.animate.move_to(arr[i][0].get_center()),
                FadeIn(arr.set_focus(i - 1, buff=0)),
            )
            self.play(FadeIn(jbg), run_time=0.1)

            while j >= 0 and key < arr.data[j]:
                j -= 1

            if i != j:
                self.play(jbg.animate.move_to(arr[j + 1][0].get_center()))
                arr.shift_and_swap(self, i, j + 1)

            self.play(FadeOut(jbg))

        self.play(Write(arr.set_focus(arr.size - 1, buff=0)), FadeOut(ibg))
        self.wait(3)


class QuickSort(Scene):
    def construct(self):
        title = Text("QuickSort", font_size=30).to_edge(UP)
        self.add(title)

        code = show_code(self, LOMUTO_PARTITION, scale=0.75)

        arr = Vector(data=[64, 34, 25, 12, 22, 11, 18]).next_to(
            code, LEFT, buff=0.6, aligned_edge=UP
        )
        self.play(Write(arr))
        self.wait(2)

        n = arr.size
        self.lomuto_partition(arr, 0, n - 1)
        self.wait(3)

        pos = code.get_corner
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob not in [title, arr]])

        self.play(FadeOut(arr))
        code2 = show_code(self, QUICKSORT, scale=0.75).shift(UP * 0.4)
        self.play(FadeIn(arr))
        self.run(arr, 0, n - 1)
        self.wait(3)

    def lomuto_partition(self, arr, low, high):
        pivot = arr.data[high]
        i = low - 1

        ilbl = (
            Text("i", font_size=22)
            .next_to(arr[i + 1][2].get_center(), UP)
            .shift(LEFT * arr.cell_width)
        )
        jlbl = Text("j", font_size=22).next_to(arr[low][0].get_center(), DOWN, buff=0.5)

        pivotbg = arr.set_focus(high, buff=0, color=RED)
        bg = arr.set_focus(low, high, color=BLUE, fill=False)

        self.play(Write(bg))
        self.play(Write(ilbl))
        self.play(Write(pivotbg))

        for j in range(low, high):
            if j > low:
                self.play(jlbl.animate.shift(RIGHT * arr.cell_width))
            if arr.data[j] < pivot:
                i += 1
                self.play(ilbl.animate.shift(RIGHT * arr.cell_width))
                arr.swap(self, i, j)

        arr.swap(self, i + 1, high)
        self.play(FadeOut(pivotbg), FadeIn(arr.set_focus(i + 1, buff=0, color=GREEN)))
        self.play(FadeOut(ilbl), FadeOut(jlbl), FadeOut(bg))
        return i + 1

    def run(self, arr, low, high):
        if low < high:
            pi = self.lomuto_partition(arr, low, high)
            self.run(arr, low, pi - 1)
            self.run(arr, pi + 1, high)
        else:
            self.play(Write(arr.set_focus(low, buff=0)))
