# Copyright (C) 2024 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of quick_concept.
#
# quick_concept is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quick_concept is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with quick_concept.  If not, see <https://www.gnu.org/licenses/>.


def _get_view3d(context):
    view3d = [a for a in context.screen.areas if a.type == "VIEW_3D"]
    if not view3d:
        return None
    space3d = [s for s in view3d[0].spaces]
    return view3d[0], space3d[0]


def _indent_row(column, fac=0.050, align=False):
    sub = column.split(factor=fac)
    sub.row()
    return sub.row(align=align)
