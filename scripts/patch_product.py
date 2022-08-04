from calendar import month
from unicodedata import category
from products import Products

MISSING_DATA = [
    {
        "category": "cpu",
        "month": "6",
        "marketplaces": ["shopee", "blibli"]
    },
    {
        "category": "cpu",
        "month": "7",
        "marketplaces": ["shopee", "tokopedia"]
    },
    {
        "category": "gpu",
        "month": "1",
        "marketplaces": ["shopee", "tokopedia", "blibli"]
    },
    {
        "category": "gpu",
        "month": "6",
        "marketplaces": ["shopee", "blibli"]
    },
    {
        "category": "gpu",
        "month": "7",
        "marketplaces": ["shopee", "tokopedia"]
    },
    {
        "category": "memory",
        "month": "6",
        "marketplaces": ["shopee", "tokopedia", "blibli"]
    },
    {
        "category": "memory",
        "month": "7",
        "marketplaces": ["shopee", "tokopedia"]
    },
    {
        "category": "memory",
        "month": "7",
        "marketplaces": ["shopee", "tokopedia"]
    },
    {
        "category": "case",
        "month": "5",
        "marketplaces": ["shopee"]
    },
    {
        "category": "case",
        "month": "6",
        "marketplaces": ["shopee", "blibli"]
    },
    {
        "category": "case",
        "month": "7",
        "marketplaces": ["shopee", "blibli"]
    },
    {
        "category": "storage",
        "month": "6",
        "marketplaces": ["shopee", "tokopedia", "blibli"]
    },
    {
        "category": "storage",
        "month": "7",
        "marketplaces": ["shopee"]
    },
    {
        "category": "motherboard",
        "month": "6",
        "marketplaces": ["shopee", "tokopedia", "blibli"]
    },
    {
        "category": "motherboard",
        "month": "7",
        "marketplaces": ["shopee"]
    },
]


def patch_missing_data():
    db_product = Products()
    for missing_product in MISSING_DATA:
        category = missing_product.get('category')
        current_month = int(missing_product.get('month'))
        month = current_month - 1
        if month < 1:
            month = 2
        markeplaces = missing_product.get('marketplaces')
        if len(markeplaces) == 3:
            products = get_patch_product(product=db_product,
                                         category=category,
                                         month=month,
                                         is_all=True
                                         )
            products = update_patch_date(products, month, current_month)
            db_product.add_products(products, category)

        else:
            products = []
            for marketplace in markeplaces:
                m_products = get_patch_product(product=db_product,
                                               category=category,
                                               month=month,
                                               marketplace=marketplace)
                products.extend(m_products)
            products = update_patch_date(products, month, current_month)
            db_product.add_products(products, category)


def get_patch_product(product: object, category: str, month: int, marketplace: str = None, is_all: bool = False):
    product = Products()
    if is_all:
        query = {
            "extraction_date": {"$regex": f"-0{month}-"}
        }

        products = product.get_products(category, '2022', True, query)
        return list(products)

    query = {
        "marketplace": {"$regex": marketplace},
        "extraction_date": {"$regex": f"-0{month}-"}
    }
    products = product.get_products(category, '2022', True, query)
    return list(products)


def update_patch_date(patch_products: list, from_month: str, to_month: str):
    fix_patch_products = []
    for patch_product in patch_products:
        old_date = patch_product.get('extraction_date')
        new_date = old_date.replace(f"-0{from_month}-", f"-0{to_month}-")

        patch_product['extraction_date'] = new_date
        del patch_product['_id']
        fix_patch_products.append(patch_product)
    return fix_patch_products


if __name__ == '__main__':
    patch_missing_data()
