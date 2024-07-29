# Marc Garard June 2024
from rdkit import Chem
from rdkit.Chem import rdFMCS, rdDepictor
from io import BytesIO, StringIO
from rdkit.Chem.MolStandardize import rdMolStandardize

# takes molecules as sdf - returns sdf of alligned strcture or original structure if failed.
def custom_align( mol, ref ):
    mol0 = mol # save orginal for return for fail
    return_sd = False
    try:
        # catch and convert string sd format to rdkit objects
        if isinstance( mol, str ):
            return_sd = True
            mol = [ m for m in Chem.ForwardSDMolSupplier( BytesIO( mol.encode() ), strictParsing=False ) ][0]

        if isinstance( ref, str ):
            ref = [ m for m in Chem.ForwardSDMolSupplier( BytesIO( ref.encode() ), strictParsing=False ) ][0]

        mcs = rdFMCS.FindMCS( [ ref, mol ], completeRingsOnly=True ) # find maximum common substructure between mol and reference
        mcs = Chem.MolFromSmarts( mcs.smartsString )# convert to Mol
        print( Chem.MolToSmiles(  mcs ) )
        Chem.SanitizeMol( mcs ) # conanicalize for smiles output
        # print( Chem.MolToSmiles(  mcs ) )

        try: 
            rdDepictor.SetPreferCoordGen(True) # ensures a good 2D depictons
            rdDepictor.GenerateDepictionMatching2DStructure( mol, ref, -1, mcs )
        except: print("align failed")

        if return_sd:
            try:
                molio = StringIO()
                with Chem.SDWriter( molio ) as w: w.write( mol )
                aligned_sdf = molio.getvalue()
                molio.close()
                print("aligned")
                return aligned_sdf
            except: return mol0
        else: return mol0
    except:
        return mol0
