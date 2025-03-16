import xml.etree.ElementTree as ET

# Wczytaj pliki XML
network_tree = ET.parse('config/network2.xml')
schedule_tree = ET.parse('config/transitSchedule2.xml')

# Parsowanie plików
network_root = network_tree.getroot()
schedule_root = schedule_tree.getroot()

# Zbieranie wszystkich linków z network.xml
network_links = {link.get('id') for link in network_root.findall('.//link')}

# Sprawdzanie linków w transitSchedule.xml
missing_links = []
for stop in schedule_root.findall('.//stopFacility'):
    link_ref = stop.get('linkRefId')
    if link_ref not in network_links:
        missing_links.append(link_ref)

if missing_links:
    print("Brakujące linki:", missing_links)
else:
    print("Wszystkie linki są obecne.")