import os
import xml.etree.ElementTree as ET


def convert_annotation(xml_file, txt_file, class_names, image_size):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    dw = 1.0 / image_size[0]
    dh = 1.0 / image_size[1]

    with open(txt_file, "w") as out_file:
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
            width = (x_max - x_min) * dw
            height = (y_max - y_min) * dh
            x_center = (x_min + width) * dw / 2
            y_center = (y_min + height) * dh / 2
            out_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


# Example usage:
class_names = ["UAV"]  # Replace with your class names
xml_dir = "/Users/sky/code/Dataset/Drones/val/xml"
txt_dir = "/Users/sky/code/Dataset/Drones/labels/val"
size = (1920, 1080)  # Replace with your image size

for xml_file in os.listdir(xml_dir):
    if xml_file.endswith(".xml"):
        txt_file = xml_file.replace(".xml", ".txt")
        convert_annotation(
            os.path.join(xml_dir, xml_file),
            os.path.join(txt_dir, txt_file),
            class_names,
            size,
        )
