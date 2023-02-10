from csv import DictReader, writer
from dataclasses import dataclass
from decimal import Decimal
import os
import re

@dataclass
class Piece():
    name: str
    thickness: Decimal
    width: Decimal
    length: Decimal
    decor: str

def piece_from_dict(row:dict) -> Piece:
    """
    returns a Piece object if the 'Part Name' field of the dict starts with an 
    uppercase letter and an underscore:
    eg.:
    S_foo_bar
    None otherwise

    thickness is defined as the smalles of the three dimensions. length as the longest.

    """
    name = row["Part Name"]
    if not re.match("[A-Z]_.+",name):
        return None
    
    dims = sorted(map(lambda d: round(d,1),map(Decimal,[row["Length (mm)"],row["Width (mm)"],row["Height (mm)"]])))
    thickness,width,length = dims[0],dims[1],dims[2]
    decor = row["Material"]
    return Piece(name,thickness,width,length,decor)

def find_file(pattern):
    files = sorted([f for f in os.listdir('.') if os.path.isfile(f) and re.match(pattern,f)])
    return files[-1]


input_csv = find_file(r'Schrank_Flur v\d+-BOM \(By Component\).csv')

with open(input_csv, newline='') as csvfile:
    reader = DictReader(csvfile)
    pieces = filter(lambda s: s is not None,map(piece_from_dict,reader))
    
    with open('stueckliste.csv', 'w', newline='') as csvfile:
        writer = writer(csvfile, delimiter=';')
        writer.writerow(["name","staerke","laenge","breite","decor"])
        for p in pieces:
            print(p.name)
            writer.writerow([p.name,p.thickness,p.length,p.width,p.decor])



