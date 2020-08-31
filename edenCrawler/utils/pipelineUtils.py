import utils.constants as constants
from io import BytesIO


def convertImgToPNG(im):
    with BytesIO() as f:
        im.save(f, format='PNG')
        return f.getvalue()


def convertVarCategoriesToGUI():
    accum = ""
    for variantId in constants.variant_categories:
        accum = ("%s: %s | " % (variantId, constants.variant_categories[variantId]))
    return accum

#File to builds varientId

