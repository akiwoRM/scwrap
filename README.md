# scwrap
Cheap nodewrapper for maya

This script is for studying python class system.

Developed by iPhone(almost)
No debug (almost)

```python
# ex.)
import scwrap.core as sc

sc.select('pSphere1')
sc.select('pCube1', add=1)
sph = sc.ls(sl=1)[0]
cube = sc.ls(sl=1)[1]
sph.tx.get()
sph.tx.set(1.0)

sph.tx = 1.0
sph.t = [1.0, 2.0, 3.0]
sph.vtx[24]
sph.attr('rx')

sph.tx >> sph.ty
sph.ty.inputs()
sph.tx.outputs()

sph.tx // sph.ty

sph.getShape()[0].getParent()

sph | cube
cube.parent(w=1)

sph.getTranslation(space='world')
sph.setTranslation(1, 2, 3)

cube.matchTransform(sph)

sph.freeze()
sph_par = sph.addParentNode(n=sph + '_par')

trs_obj = sc.node.Transform("trs")
for i in range(3):
    trs_obj.create()

```