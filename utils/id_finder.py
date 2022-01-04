def find_item_id(link:str):
    link = link.split("?")
    link = link[0].split("-i.")
    link = link[1].split(".")
    return link[1]

def find_shop_id(link:str):
    link = link.split("?")
    link = link[0].split("-i.")
    link = link[1].split(".")
    return link[0]