# 图像总高度和宽度
total_height = 
total_width = 

plates_info = {} # 检测的车牌坐标
vanishing_point = (x, x)

def calculate_plate_height(plate):
    top_left = plate["top_left"]
    bottom_right = plate["bottom_right"]
    height = abs(top_left[1] - bottom_right[1])
    return height

height1 = calculate_plate_height(plates_info["plate1"])
height2 = calculate_plate_height(plates_info["plate2"])

# 切分 x 个条带
zone_width =vanishing_point[0] / x
zones = [
    {"range": (i, i + zone_width), "height": 0} for i in range(0, int(1358.0), int(zone_width))
]

def calculate_zone_plate_height(zone, vanishing_point, known_height, known_y):
    y_v = vanishing_point[1]
    y_avg = (zone["range"][0] + zone["range"][1]) / 2
    if y_avg > y_v:
        return 0
    height_change_ratio = known_height / abs(known_y - y_v)
    estimated_height = height_change_ratio * abs(y_avg - y_v)
    return estimated_height

known_y1 = (plates_info["plate1"]["top_left"][1] + plates_info["plate1"]["bottom_right"][1]) / 2
known_height1 = height1
zone_ranges = []
heights = []
for zone in zones:
    height_change = calculate_zone_plate_height(zone, vanishing_point, known_height1, known_y1)
    zone_ranges.append((zone['range'][0], zone['range'][1]))
    heights.append(round(height_change, 1))
print(f"zones = {zone_ranges}")
print(f"heights = {heights}")