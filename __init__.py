"""
Copyright (C) 2024 aditiavfx
aditia.ap@gmail.com

Created by aditiavfx

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "Quick Concept",
    "author": "aditiavfx",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "",
    "description": "Render Outline Quick for Concept",
    "warning": "",
    "doc_url": "",
    "category": "Pipeline",
}

import importlib
from bpy.utils import register_class, unregister_class
from typing import List
from . import (
    operators,
    ui,
)

modules = (
    operators,
    ui,
)


#! REGISTRATION
def register_unregister_modules(modules: List, register: bool):
    """Recursively register or unregister modules by looking for either
    un/register() functions or lists named `registry` which should be a list of
    registerable classes.
    """
    register_func = register_class if register else unregister_class

    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, "registry"):
            for c in m.registry:
                try:
                    register_func(c)
                except Exception as e:
                    un = "un" if not register else ""
                    print(f"Warning: Failed to {un}register class: {c.__name__}")
                    print(e)

        if hasattr(m, "modules"):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, "register"):
            m.register()
        elif hasattr(m, "unregister"):
            m.unregister()


def register():
    register_unregister_modules(modules, True)


def unregister():
    register_unregister_modules(modules, False)
