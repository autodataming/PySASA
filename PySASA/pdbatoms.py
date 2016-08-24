#!  python 3


import copy
from . import v3
from . import data
class Atom:
    """
    This is the basic object to hold Atom information.
 
    The attributes are basically those of a PDB atom field.
    However, pos and vel are proper vectors that can be manipulated
    with the v3 3d-vector geometry library.  
    """
 
    def __init__(self, pos=None, atom_type="", res_num=None):
       """
       Normally initialized as an empty container, and filled
       up progressively as fields are read by parsers.
       """
       self.is_hetatm = False
       self.pos = v3.vector() if pos is None else pos
       self.vel = v3.vector()
       self.mass = 0.0
       self.charge = 0.0
       self.type = ""
       self.element = ""
       self.chain_id = " "
       self.res_type = ""
       self.res_num = ""
       self.res_insert = ""
       self.bfactor = 0.0
       self.occupancy = 0.0
       self.num = 0
       self.alt_conform = " "
 
    def copy(self):
       return copy.deepcopy(self)
 
    def type_str(self):
        """
        Format atom_type to write to a PDB file's atom line.
        """
        atom_type = self.type.strip()
        if len(atom_type) == 1:
            atom_type = " %s  " % atom_type
        elif len(atom_type) == 2:
            if atom_type[0].isdigit():
               atom_type = "%s  " % atom_type
            else:
                atom_type = " %s " % atom_type
        elif len(atom_type) == 3:
            if atom_type[0].isdigit():
                atom_type = "%s " % atom_type
            else:
                atom_type = " %s" % atom_type
        return atom_type    
 
    def pdb_str(self):
        """
        Returns a string for output to an PDB file.
        """
        if self.is_hetatm:
            field = "HETATM"
        else:
            field = "ATOM  "
        x, y, z = self.pos
        s = "%6s%5s %4s %-4s%1s%4s%1s   %8.3f%8.3f%8.3f%6.2f%6.2f" % \
          (field, 
           str(self.num)[-5:], 
           self.type_str(),
           self.res_type, 
           self.chain_id,
           str(self.res_num)[-4:], 
           self.res_insert,
           x, y, z,
           self.occupancy, 
           self.bfactor)
        return s
                
    def res_tag(self):
        tag = ""
        if self.chain_id != " " and self.chain_id != "":
            tag += self.chain_id + ":"
            tag += str(self.res_num)
        if self.res_insert:
            tag += self.res_insert
        return tag  
 
    def __str__(self):
        x, y, z = self.pos
        return "%s:%s-%s" %  \
         (self.res_tag(), self.res_type, self.type)
 
    def transform(self, matrix):
        """
        Transforms the pos vector by a v3.transform matrix.
        """
        new_pos = v3.transform(matrix, self.pos)
        v3.set_vector(self.pos, new_pos)




def add_radii(atoms):
   """
   Lookup and assign atom.radius for atoms.
   """
   for atom in atoms:
     if atom.element in data.radii:
       atom.radius = data.radii[atom.element]
     else:
       atom.radius = data.radii['.']



def read_pdb(fname):
    """
    Reads a list of Atoms from a PDB file.
    """
    atoms = []
    for line in open(fname, 'r'):
        if line.startswith(("ENDMDL", "END")):
            break
        if line.startswith(("ATOM", "HETATM")):
            atoms.append(AtomFromPdbLine(line))
    return atoms
  
def AtomFromPdbLine(line):
    """
    Returns an Atom object from an atom line in a pdb file.
    """
    atom = Atom()
    if line.startswith('HETATM'):
        atom.is_hetatm = True
    else:
        atom.is_hetatm = False
    atom.num = int(line[6:11])
    atom.type = line[12:16].strip(" ")
    atom.alt_conform = line[16]
    atom.res_type = line[17:21].strip()
    atom.element = data.guess_element(atom.res_type, atom.type)
    atom.chain_id = line[21]
    atom.res_num = int(line[22:26])
    atom.res_insert = line[26]
    if atom.res_insert == " ":
      atom.res_insert = ""
    x = float(line[30:38])
    y = float(line[38:46])
    z = float(line[46:54])
    v3.set_vector(atom.pos, x, y, z)
    try:
        atom.occupancy = float(line[54:60])
    except:
        atom.occupancy = 100.0
    try:
        atom.bfactor = float(line[60:66])
    except:
        atom.bfactor = 0.0
    return atom