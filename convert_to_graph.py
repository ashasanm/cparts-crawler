import time

from models.graphs import Graphs
from services.product_graphs import productGraphs
from services.category_graphs import categoryGraphs


def save_to_graph_db():
    categories = ['cpu', 'gpu', 'memory', 'motherboard', 'case', 'storage']

    graph = Graphs()

    for category in categories:
        product = productGraphs(category=category)
        minimum = product.get_minimum()
        average = product.get_average()
        maximum = product.get_maximum() # {category: categpry, maximum: array, minimum:array, average:array}
        graph.add_graph_data(maximum)

def save_to_category_graph():
    start_exec = time.time()
    categories = ['cpu', 'gpu', 'memory', 'motherboard', 'case', 'storage']
    calculators = ['average', 'minimum', 'maximum']

    for category_filter in categories:
        for calculator in calculators:
            category = categoryGraphs(category_filter)
            result = category.calculate_data(value_calculator=calculator)
            Graphs().add_category(result)


if __name__ == '__main__':
    # Graphs().refresh_graph()
    save_to_graph_db()
    # Graphs().refresh_category()
    save_to_category_graph()