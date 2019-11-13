# scwrap
Cheap nodewrapper for maya

This script is for studying python class system.

Developed by iPhone(almost)
No debug (almost)

```python
# ex.)
import scwrap.core as sc

sc.file(f=1, new=1)

sc.polySphere()
sc.polyCube()

sc.select('pSphere1')
sc.select('pCube1', add=1)
sph = sc.ls(sl=1)[0]
cube = sc.ls(sl=1)[1]
sph.tx.get()
sph.tx.set(1.0)

sph.vtx[24]
sph.attr('rx')  # access attribute by string
# Result: [Attribute('pSphere1.rx')] #

sph.tx >> sph.ty  # connect attr
sph.ty.inputs()
# Result: [Transform('pSphere1')] #
sph.tx.outputs()
# Result: [Transform('pSphere1')] #

sph.tx // sph.ty  # disconnect attr

sph.getShape()[0].getParent()

sph | cube  # parent
cube.parent(w=1)

sph.getTranslation(space='world')
sph.setTranslation(1, 2, 3)

cube.matchTransform(sph)

sph = sph.rename("sph")  # rename

sph.freeze()
sph_par = sph.addParentNode(n=sph + '_par')

trs_obj = sc.node.Transform("trs", set={"ty": 1})
for i in range(3):
    trs_obj.attr_opt["set"]["tx"] = i
    trs_obj.create()

trsA_obj = sc.node.Transform("ctl", add=[{"ln": "display", "at": "enum", "en": "Hide:Show", "k": 1}])
trsA_obj.create()

sc.deleteNode(trsA_obj, "trsB_obj”)

```