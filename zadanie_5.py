import time
import os
import datetime
import random
import pandas
from functools import wraps
from collections import namedtuple

Row = namedtuple('DataRow', ['label', 'quick_sort', 'merge_sort', 'heap_sort'])


class DataRow:
    rows = []
    label = None
    quick_sort = None
    merge_sort = None
    heap_sort = None
    quick_sort_average = None
    merge_sort_average = None
    heap_sort_average = None
    quick_sort_std = None
    merge_sort_std = None
    heap_sort_std = None
    result = None


class DataGenerator:
    @staticmethod
    def random(count):
        return DataGenerator.generate_list_of_random_numbers(count)

    @staticmethod
    def sorted(count):
        temp_list = DataGenerator.generate_list_of_random_numbers(count)
        return sorted(temp_list)

    @staticmethod
    def reverse_sorted(count):
        temp_list = DataGenerator.generate_list_of_random_numbers(count)
        return sorted(temp_list, reverse=True)

    @staticmethod
    def generate_list_of_random_numbers(count):
        range_start = 1
        range_end = count * 2
        list_size = count
        return random.sample(range(range_start, range_end), list_size)


class Algorithms:
    def algorithm_timer(func):
        @wraps(func)
        def timer(*args, **kwargs):
            time_start = time.perf_counter()
            algorithm = func(*args, **kwargs)
            time_elapsed = time.perf_counter() - time_start
            kwargs['measurements'].append(time_elapsed)
            return algorithm

        return timer

    @algorithm_timer
    def quick_sort(test_data, measurements=[]):

        def random_index(low_index, high_index):
            return random.randint(low_index, high_index)

        def quick_sorting(array, low_index, high_index):
            if low_index < high_index:
                pivot = random_index(low_index, high_index-1)
                array[pivot], array[low_index] = array[low_index], array[pivot]
                pivot_index = partition(array, low_index, high_index)
                quick_sorting(array, low_index, pivot_index)
                quick_sorting(array, pivot_index + 1, high_index)

        def partition(array, low_index, high_index):
            pivot = array[low_index]
            left_wall = low_index
            for index in range(low_index, high_index):
                if array[index] < pivot:
                    left_wall += 1
                    array[index], array[left_wall] = array[left_wall], array[index]
            array[low_index], array[left_wall] = array[left_wall], array[low_index]
            return left_wall

        numbers = test_data.copy()
        quick_sorting(numbers, 0, len(numbers))
        return numbers

    @algorithm_timer
    def merge_sort(test_data, measurements=[]):

        def mergeSort(myList):
            if len(myList) > 1:
                mid = len(myList) // 2
                left = myList[:mid]
                right = myList[mid:]

                mergeSort(left)
                mergeSort(right)

                left_index, right_index, result_index  = 0, 0, 0
                while left_index < len(left) and right_index < len(right):
                    if left[left_index] < right[right_index]:
                        myList[result_index] = left[left_index]
                        left_index += 1
                    else:
                        myList[result_index] = right[right_index]
                        right_index += 1
                    result_index += 1
                while left_index < len(left):
                    myList[result_index] = left[left_index]
                    left_index += 1
                    result_index += 1
                while right_index < len(right):
                    myList[result_index] = right[right_index]
                    right_index += 1
                    result_index += 1

        numbers = test_data.copy()
        mergeSort(numbers)
        return numbers

    @algorithm_timer
    def heap_sort(test_data, measurements=[]):

        def perform_heapsort(array, number, count):
            max_val = count
            counter1 = 2 * count + 1
            counter2 = 2 * count + 2
            if counter1 < number and array[count] < array[counter1]:
                max_val = counter1
            if counter2 < number and array[max_val] < array[counter2]:
                max_val = counter2
            if max_val != count:
                array[count], array[max_val] = array[max_val], array[count]
                perform_heapsort(array, number, max_val)

        def heap_sorting(array):
            number = len(array)
            for count in range(number, -1, -1):
                perform_heapsort(array, number, count)
            for count in range(number-1, 0, -1):
                array[count], array[0] = array[0], array[count]
                perform_heapsort(array, count, 0)

        numbers = test_data.copy()
        heap_sorting(numbers)
        return numbers


class Tester:
    def __init__(self):
        self.quick_sort_results = []
        self.merge_sort_results = []
        self.heap_sort_results = []
        self.results = []

    def run_full_tests(self, data_generator, number_of_tests=5, number_of_subtests=10,
                       data_count=5000, count_increment=5000):
        current_test = 1
        count = data_count
        while current_test <= number_of_tests:
            current_subtest = 1
            while current_subtest <= number_of_subtests:
                test_data = data_generator(count)
                self.single_subtest(test_data)
                current_subtest += 1
            self.results.append(self.build_result(current_test, number_of_subtests, count))
            self.clear_partial_results()
            current_test += 1
            count += count_increment

    def single_subtest(self, test_data):
        Algorithms.quick_sort(test_data, measurements=self.quick_sort_results)
        Algorithms.merge_sort(test_data, measurements=self.merge_sort_results)
        Algorithms.heap_sort(test_data, measurements=self.heap_sort_results)

    def build_result(self, current_test, number_of_subtests, count):
        result = DataRow()
        result.rows = []
        result.count = count
        for current_subtest in range(number_of_subtests):
            label = f'{str(current_test)}-{str(current_subtest + 1)}'
            result.rows.append(Row(label,
                                   self.quick_sort_results[current_subtest],
                                   self.merge_sort_results[current_subtest],
                                   self.heap_sort_results[current_subtest])
                               )
        from statistics import mean
        result.quick_sort_average = mean(self.quick_sort_results)
        result.merge_sort_average = mean(self.merge_sort_results)
        result.heap_sort_average = mean(self.heap_sort_results)
        from statistics import pstdev
        result.quick_sort_std = pstdev(self.quick_sort_results)
        result.merge_sort_std = pstdev(self.merge_sort_results)
        result.heap_sort_std = pstdev(self.heap_sort_results)
        return result

    def clear_partial_results(self):
        self.quick_sort_results.clear()
        self.merge_sort_results.clear()
        self.heap_sort_results.clear()

    def clear_all_results(self):
        self.quick_sort_results.clear()
        self.merge_sort_results.clear()
        self.heap_sort_results.clear()
        self.results.clear()


class ExcelExporter:
    DataSheet = namedtuple('DataSheet', ['sheet_name', 'data_frame'])

    def __init__(self):
        self.filename = ExcelExporter.generate_filename()
        self.data_sheets = []

    @staticmethod
    def generate_filename():
        formatted_current_datetime = datetime.datetime.now().strftime("%y-%m-%d_%H_%M")
        return f"Sorting Algorithms Measurements_{formatted_current_datetime}"

    def export_file(self):
        with pandas.ExcelWriter(f"{self.filename}.xlsx") as file:
            for sheet_name, data_frame in self.data_sheets:
                data_frame.to_excel(file, sheet_name=f'{sheet_name}')

    def launch_file(self):
        os.system(f"start EXCEL.EXE \"{self.filename}.xlsx\"")

    def generate_sheet(self, data, sheet_name):
        data_frame = ExcelExporter.create_data_frame(data)
        self.data_sheets.append(self.DataSheet(sheet_name, data_frame))

    @staticmethod
    def create_data_frame(data):
        def pad_with_none(arr, target_length):
            return arr + [None] * (target_length - len(arr))

        test_numbers = []
        numbers_count = []
        quick_sort_results = []
        quick_sort_averages = []
        quick_sort_deviations = []
        merge_sort_results = []
        merge_sort_averages = []
        merge_sort_deviations = []
        heap_sort_results = []
        heap_sort_averages = []
        heap_sort_deviations = []
        for item in data:
            rows = len(item.rows)
            test_numbers.extend([row.label for row in item.rows])
            numbers_count.extend(pad_with_none([item.count], rows))
            quick_sort_results.extend([row.quick_sort for row in item.rows])
            quick_sort_averages.extend(pad_with_none([item.quick_sort_average], rows))
            quick_sort_deviations.extend(pad_with_none([item.quick_sort_std], rows))
            merge_sort_results.extend([row.merge_sort for row in item.rows])
            merge_sort_averages.extend(pad_with_none([item.merge_sort_average], rows))
            merge_sort_deviations.extend(pad_with_none([item.merge_sort_std], rows))
            heap_sort_results.extend([row.heap_sort for row in item.rows])
            heap_sort_averages.extend(pad_with_none([item.heap_sort_average], rows))
            heap_sort_deviations.extend(pad_with_none([item.heap_sort_std], rows))

        measurements_data = {
            'Test number': test_numbers,
            'Numbers count': numbers_count,
            'Quick Sort Results': quick_sort_results,
            'Quick Sort Avg': quick_sort_averages,
            'Quick Sort STD': quick_sort_deviations,
            'Merge Sort Results': merge_sort_results,
            'Merge Sort Avg': merge_sort_averages,
            'Merge Sort STD': merge_sort_deviations,
            'Heap Sort Results': heap_sort_results,
            'Heap Sort Avg': heap_sort_averages,
            'Heap Sort STD': heap_sort_deviations,
        }
        measurements_data_frame = pandas.DataFrame(measurements_data, dtype=float)
        measurements_data_frame = measurements_data_frame.set_index('Test number')
        return measurements_data_frame


RunConfig = namedtuple('RunConfig', ['sheet_name', 'generator'])


def main():
    run_configs = (
        RunConfig("Random order", DataGenerator.random),
        RunConfig("Sorted", DataGenerator.sorted),
        RunConfig("Reverse-sorted", DataGenerator.reverse_sorted),
    )

    exporter = ExcelExporter()
    for config in run_configs:
        tester = Tester()
        tester.run_full_tests(config.generator)
        exporter.generate_sheet(tester.results, config.sheet_name)
        tester.clear_all_results()
    exporter.export_file()
    exporter.launch_file()


if __name__ == '__main__':
    main()
