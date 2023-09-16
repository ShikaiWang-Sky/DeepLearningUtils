import os
import xml.etree.ElementTree as ET


# This script converts Pascal VOC XML annotations to YOLO format
def convert_annotation(xml_file, txt_file, class_names):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(txt_file, "w") as out_file:
        dw, dh = 0, 0
        for size in root.iter("size"):
            original_width = int(size.find("width").text)
            original_height = int(size.find("height").text)
            dw = 1.0 / original_width
            dh = 1.0 / original_height

        for obj in root.iter("object"):
            class_name = obj.find("name").text
            if class_name not in class_names:
                continue
            class_id = class_names.index(class_name)
            bndbox = obj.find("bndbox")
            x_min = int(bndbox.find("xmin").text)
            y_min = int(bndbox.find("ymin").text)
            x_max = int(bndbox.find("xmax").text)
            y_max = int(bndbox.find("ymax").text)

            # Convert to YOLO format: x_center, y_center, width, height
            _width = x_max - x_min
            _height = y_max - y_min
            width = _width * dw
            height = _height * dh
            x_center = (x_min + _width) * dw / 2
            y_center = (y_min + _height) * dh / 2
            out_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


# Example usage:
class_names = ["UAV"]  # Replace with your class names
xml_dir = "/Users/sky/code/Dataset/Drones/train/xml"
txt_dir = "/Users/sky/code/Dataset/Drones/labels/train"

for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        txt_file = xml_file.replace(".xml", ".txt")
        convert_annotation(
            os.path.join(xml_dir, xml_file),
            os.path.join(txt_dir, txt_file),
            class_names,
        )
