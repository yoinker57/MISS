import xml.etree.ElementTree as ET
import xml.dom.minidom
from collections import defaultdict

def parse_stops_from_file(filename):
    stops = []
    with open(filename, 'r', encoding='utf-8') as f:
        # Pomiń pierwszą linię (nagłówek)
        next(f)
        for line in f:
            if line.strip():  # Ignorujemy puste linie
                data = line.strip().split(',')
                stop_name = data[2].strip().replace(" ", "").strip('"')
                stop_lat = data[4]
                stop_lon = data[5]
                stops.append((stop_name, stop_lat, stop_lon))
    return stops

def generate_network_xml(stops, output_filename):
    root = ET.Element("network")
    nodes_element = ET.SubElement(root, "nodes")
    
    stop_count = defaultdict(int)  # Słownik do liczenia wystąpień przystanków
    
    for stop_name, stop_lat, stop_lon in stops:
        stop_count[stop_name] += 1  # Zwiększ licznik dla przystanku
        node_id = f"{stop_name}{stop_count[stop_name]}"  # Tworzenie id na zasadzie 'NazwaPrzystankuNumer'
        
        # Konwersja na string (bez specjalnych znaków)
        node = ET.SubElement(nodes_element, "node", id=node_id, x=str(stop_lon), y=str(stop_lat))
    
    # Formatowanie XML
    rough_string = ET.tostring(root, encoding="utf-8", xml_declaration=False)
    reparsed = xml.dom.minidom.parseString(rough_string)
    formatted_xml = "\n".join([line for line in reparsed.toprettyxml(indent="  ").split("\n")[1:] if line.strip()])
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<!DOCTYPE network SYSTEM "http://matsim.org/files/dtd/network_v1.dtd">\n')
        f.write(formatted_xml)

# Przykład użycia
stops_filename = "../data/stops.txt"
stops = parse_stops_from_file(stops_filename)

output_filename = "../config/network2.xml"
generate_network_xml(stops, output_filename)
