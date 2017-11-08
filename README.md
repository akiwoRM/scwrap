# scwrap
Cheap nodewrapper for maya

This script is for studying python class system.
```python
# ex.)
import scwrap.core as sc
sc.Node('pSphere1').tx.get()
sc.Node('pSphere1').tx.set(1.0)

sc.Node('pSphere1').tx = 1.0
sc.Node('pSphere1').t = [1.0, 2.0, 3.0]
sc.Node(‘pSphere1’).vtx[24]
sc.Node(‘pSphere1’).attr(‘rx’)

sc.Node('pSphere1').tx >> sc.Node(‘pSphere1’).ty
sc.Node(‘pSphere1’).ty.inputs()
sc.Node(‘pSphere1’).tx.outputs()

sc.Node('pSphere1').tx // sc.Node(‘pSphere1’).ty
```