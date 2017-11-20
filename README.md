# scwrap
Cheap nodewrapper for maya

This script is for studying python class system.

developed by iPhone(almost)

```python
# ex.)
import scwrap.core as sc

sc.cmds.select('pSphere1')
sph = sc.ls(sl=1)[0]
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

sph | sc.wrap('pCube1')

sph.getTranslation(space='world')

```