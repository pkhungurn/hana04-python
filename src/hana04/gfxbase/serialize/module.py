from jyuusu.binder import Module as JyuusuModule, Binder

import hana04.gfxbase.serialize.gfxtype.vector2d
import hana04.gfxbase.serialize.gfxtype.vector3d
import hana04.gfxbase.serialize.gfxtype.vector4d
import hana04.gfxbase.serialize.gfxtype.point2d
import hana04.gfxbase.serialize.gfxtype.point3d
import hana04.gfxbase.serialize.gfxtype.quat4d
import hana04.gfxbase.serialize.gfxtype.point3i
import hana04.gfxbase.serialize.gfxtype.matrix4d
import hana04.gfxbase.serialize.gfxtype.transform
import hana04.gfxbase.serialize.gfxtype.aabb2d
import hana04.gfxbase.serialize.gfxtype.aabb3d


class HanaGfxbaseSerializeModule(JyuusuModule):
    def configure(self, binder: Binder):
        binder.install_module(hana04.gfxbase.serialize.gfxtype.vector2d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.vector3d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.vector4d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.point2d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.point3d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.quat4d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.point3i.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.matrix4d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.transform.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.aabb2d.Module)
        binder.install_module(hana04.gfxbase.serialize.gfxtype.aabb3d.Module)
