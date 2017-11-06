# scwrap
cheap nodewrapper for maya

```python
# ex.)
import scwrap.core as sc
sc.Node('pSphere1').tx.get()
sc.Node('pSphere1').tx.set(1.0)

sc.Node('pSphere1').tx = 1.0
sc.Node('pSphere1').t = [1.0, 2.0, 3.0]
sc.Node(‘pSphere1’).vtx[24]
sc.Node(‘pSphere1’).attr(‘rx’)
```