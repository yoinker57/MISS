import xml.etree.ElementTree as ET
import xml.dom.minidom
import random

def parse_nodes_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    nodes = []
    for node in root.find('nodes').findall('node'):
        x = float(node.get('x'))
        y = float(node.get('y'))
        nodes.append([x, y])
    return nodes

def generate_population_xml(nodes, num_people, output_filename):
    root = ET.Element("plans")
    
    for person_id in range(1, num_people + 1):
        person = ET.SubElement(root, "person", employed="no", age=str(random.randint(10, 60)), id=str(person_id))
        plan = ET.SubElement(person, "plan", selected="yes")
        
        start_node, end_node = random.sample(nodes, 2)
        
        # Losowanie godziny startu od 5:00 do 12:00 (w sekundach)
        start_time = random.randint(5 * 3600, 12 * 3600)  # Losowa godzina między 5:00 a 12:00
        end_time = start_time + random.randint(3600, 8 * 3600)  # Musi być większy od start_time
        
        ET.SubElement(plan, "act", end_time=f"{start_time//3600:02}:{(start_time%3600)//60:02}:00", x=str(start_node[0]), y=str(start_node[1]), type="home")
        ET.SubElement(plan, "leg", mode="pt")
        ET.SubElement(plan, "act", end_time=f"{end_time//3600:02}:{(end_time%3600)//60:02}:00", x=str(end_node[0]), y=str(end_node[1]), type="home")
    
    rough_string = ET.tostring(root, encoding="utf-8")
    reparsed = xml.dom.minidom.parseString(rough_string)
    formatted_xml = "\n".join([line for line in reparsed.toprettyxml(indent="  ").split("\n")[1:] if line.strip()])
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd">\n')
        f.write(formatted_xml)


filename = "../config/network.xml"
nodes = parse_nodes_from_file(filename)

num_people = 400
generate_population_xml(nodes, num_people, "../config/population.xml")
