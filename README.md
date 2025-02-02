# Align-Structures-with-RDKIT
This project provides code which aligns structures using RDKIT based on a MCS approach.
This issue has come up for me several times in different contexts where automation was desired for aligning structures.  I'd solved the issue to some extent using proprietary software which provided tools to automate it through python.  What if you don't have that proprietary software?  I was not able to easily find a solution online and many attempts resulted in irregular structures.

In this solution, I find the Maximum Common Substructure ( MCS ) between the structures.  Using the MCS as a reference, the structure depiction can be aligned with the reference molecule.  RDKIT has an issue with bond sizes or overlapping atoms for some molecules which will create structures which need to be normalized.  Setting coordinate preferences resolved the bond and overlap issue. 

### Input:
Aligning the second ( sample2.sdf ) structure to the first ( sample1.sdf ) reference structure:
![inputs]( https://github.com/mgarard/Align-Structures-with-RDKIT/blob/main/input.JPG)

### Output:
![outputs]( https://github.com/mgarard/Align-Structures-with-RDKIT/blob/main/output.JPG)

### Usage:<br>
If a RDKIT object is provided for the molecule to be aligned is given, a RDKIT object is returned.  If the SD text is provided for the molecule to be aligned, the SD text is returned.  The latter is useful with DBs where SD texts are saved.  The reference molecule requires predefined coordinates if a desired confirmation is desired.


```
from align_structures import custom_align

# as SD text
# Use structures with defined coordinates
with open( 'sample1.sdf', 'r' ) as f: mol1_sd = f.read()
with open( 'sample2.sdf', 'r' ) as f: mol2_sd = f.read()

# align the structures
aligned_sd = custom_align( mol = mol2_sd, ref = mol1_sd )

# output for visualization
with open( "temp.sdf", 'w' ) as f: f.write( aligned_sd )
```
```
from align_structures import custom_align

# as RDKIT mol objects
# open structure with coordinates, represents registered structures
mol1 = Chem.SDMolSupplier( 'sample1.sdf' )[0]
mol2 = Chem.SDMolSupplier( 'sample2.sdf' )[0]

# align the structures
aligned_sd = custom_align( mol = mol2, ref = mol1 )

# output for visualization
with Chem.SDWriter( "temp.sdf" ) as w: w.write( aligned_sd )
```

### Discussion:
This can be added to in many ways.  I’ll provide one example that comes to mind immediately; one big issue is more overlap between structures results in better alignment.  This can make cascading alignments result in some oddly oriented structures.  

One might immediately imagine that Tanimoto similarities could be used to rank alignment pair ordering based closets neighbors.  This may not always result in the best MCS as similarities diverge but would be an easy way to get closer.   Assessing MCS is not as straightforward as Tanimoto similarities. 

