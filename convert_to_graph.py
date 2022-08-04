import time

from models.graphs import Graphs
from services.product_graphs import productGraphs
from services.category_graphs import categoryGraphs


def save_to_graph_db():
    categories = ['cpu', 'gpu', 'memory', 'motherboard', 'case', 'storage']

    graph = Graphs()

    for category in categories:
        product = productGraphs(category=category)
        for year_filter in ['2022', '2021']:
            product.get_monthly('avg', year_filter)
            product.get_monthly('min', year_filter)
            product.get_monthly('max', year_filter)
            graph.add_graph_data(product.monthly)
            # minimum = product.get_minimum(year_filter)
            # average = product.get_average(year_filter)
            # maximum = product.get_maximum(year_filter) # {category: categpry, maximum: array, minimum:array, average:array}
            # graph.add_graph_data(maximum)

def save_to_category_graph():
    start_exec = time.time()
    categories = ['cpu', 'gpu', 'memory', 'motherboard', 'case', 'storage']
    # calculators = ['average', 'minimum', 'maximum']
    calculators = ['avg', 'min', 'max']

    for category_filter in categories:
        for calculator in calculators:
            category = categoryGraphs(category_filter)
            for year_filter in ['2022', '2021']:
                # result = category.calculate_data(value_calculator=calculator, year_filter=year_filter)
                category.calculate_data_v2(calculator, year_filter)
                Graphs().add_category(category.monthly)


if __name__ == '__main__':
    # Graphs().refresh_graph()
    # save_to_graph_db()
    Graphs().refresh_category()
    save_to_category_graph()