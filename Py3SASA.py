#! python3

#encoding: utf-8

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import re

from PySASA import pdbatoms
from PySASA.asa import calculate_asa


class SASA(Frame):
    def __init__(self):
        Frame.__init__(self)    # creat Tk root,and frame in it
        self.pack(expand=YES,fill=BOTH)
        self.master.title("Calculation of Solvent Accesible Surfece Areas")
        
        pdbF=Frame(self)
        pdbF.pack(side=TOP,fill=BOTH,expand=YES)
        Label(pdbF,text="Please select your PDB file:",width=50).pack(side=LEFT)
        Button(pdbF,text="浏览···",command=self.askopenfilename).pack(side=LEFT)
        self.fileL_var=StringVar()
        self.fileL_var.set("未选择文件。")   
        self.fileL=Label(pdbF,textvariable=self.fileL_var)
        self.fileL.pack(side=LEFT)
        
                        
        probeF=Frame(self)
        probeF.pack(side=TOP,fill=BOTH,expand=YES)
        Label(probeF,text="Please enter radius of the solvent probe(A): ",width=50).pack(side=LEFT)        
        self.radius_var=DoubleVar()
        self.radius_var.set(1.4)
        ray_ent=Entry(probeF,textvariable=self.radius_var,width=30)
        ray_ent.pack(side=LEFT)


        sphereF=Frame(self)
        sphereF.pack(side=TOP,fill=BOTH,expand=YES)
        Label(sphereF,text="Please enter number of points the spherical dot-density : ",width=50).pack(side=LEFT) 
        self.nsphere_var=IntVar()
        self.nsphere_var.set(960)
        nsphere_ent=Entry(sphereF,textvariable=self.nsphere_var,width=30)
        nsphere_ent.pack(side=LEFT)
        
        
        areaF=Frame(self)
        areaF.pack(side=TOP,fill=BOTH,expand=YES)
        Label(areaF,text="The suface areas is: ",width=50).pack(side=LEFT)
        self.area_var=DoubleVar()
        area_ent=Entry(areaF,textvariable=self.area_var,width=30)
        area_ent.pack(side=LEFT) 
        self.area_var.set(0.0)
        
        outputF=Frame(self)
        #hide outputF
        #outputF.pack(side=TOP,fill=BOTH,expand=YES)
        Label(outputF,text="Please enter the output file position and name: ",width=50).pack(side=LEFT)
        self.outfile_var=StringVar()
        out_ent=Entry(outputF,textvariable=self.outfile_var,width=30)
        out_ent.pack(side=LEFT)    
        temp=self.fileL_var.get()
        temp2=re.sub('pdb','txt',temp)
        self.outfile_var.set(temp2)
        
        
        
        buttonF=Frame(self)
        buttonF.pack(side=TOP,fill=BOTH,expand=YES)
        Button(buttonF,text="run",command=self.calcASA).pack( )
        
        noteF=Frame(self)
        noteF.pack(side=BOTTOM,fill=BOTH,expand=YES)
        Label(noteF,text="Contact me: 744891290.com").pack(side=LEFT)
    
    def askopenfilename(self):
        filename=askopenfilename(filetypes=[("pdb files","*.pdb")])
        if filename:
            self.fileL_var.set(filename)           
            temp=self.fileL_var.get()
            temp2=re.sub('pdb','txt',temp)
            self.outfile_var.set(temp2)
            	
            
                
    def calcASA(self):
        pdbfile=self.fileL_var.get()
        radius_probe=self.radius_var.get()
        nsphere=self.nsphere_var.get()
        atoms = pdbatoms.read_pdb(pdbfile)
        pdbatoms.add_radii(atoms)
        asas = calculate_asa(atoms, 1.4, nsphere)
        print (asas)
        self.area_var.set(asas)
     
        
        


if __name__ == '__main__':
    SASA().mainloop()
    