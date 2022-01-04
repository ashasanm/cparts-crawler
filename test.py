import time

from services.product_graphs import productGraphs
from services.category_graphs import categoryGraphs

def product_graph(category):
    start_exec = time.time()
    product = productGraphs(category)
    
    # start_time = time.time()
    # minimum = product.get_minimum()
    # print(minimum)

    start_time = time.time()
    average = product.get_average()
    print(average)
    
    # start_time = time.time()
    # maximum = product.get_maximum()
    # for key, value in maximum.items():
    #     print(key, value)
    print("Get Total Execution time %s seconds" % (time.time() - start_exec))


def category_graph(category_filter: str):
    start_exec = time.time()
    category = categoryGraphs(category_filter)
    average = category.calculate_data(value_calculator="average")
    print(average)
    print("Get Total Execution time %s seconds" % (time.time() - start_exec))






if __name__ == '__main__':
    product_graph(category="cpu")
    # category_graph(category_filter="gpu")
    
