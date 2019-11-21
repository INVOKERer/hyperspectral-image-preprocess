import openslide as op
from openslide.deepzoom import DeepZoomGenerator


def tif_cut(tifway, x, k):
    slide = op.OpenSlide(tifway)
    # print(slide.level_dimensions)
    bigImg = DeepZoomGenerator(slide, tile_size=x-2, overlap=1, limit_bounds=False)

    count = bigImg.level_count - 1
    z = count - k                  # 倒着读取
    raw, col = bigImg.level_tiles[z]
    for i in range(raw-1):
        for j in range(col-1):
            img = bigImg.get_tile(z, (j, i))
            outputway = r'E:\HE+CAM5\tiff\test\rgb_{a}_{b}.png'.format(a=i, b=j)
            img.save(outputway)


if __name__ == '__main__':
    tif_way = r'E:\HE+CAM5\tiff\027378_HE+CAM52.tiff'
    a, n = 1024, 2       # a = 分割后图片边长  n = tif图片的第几个level
    tif_cut(tif_way, a, n)
