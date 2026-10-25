"""macOS Accessibility API reader entry point.
Implement and test this on the Mac with Accessibility permission enabled.
Windows cannot inspect macOS TextEdit controls through this module.
"""

def read_controls():
    try:
        from ApplicationServices import (
            AXUIElementCreateApplication, AXUIElementCopyAttributeValue,
            kAXChildrenAttribute, kAXRoleAttribute, kAXTitleAttribute,
            kAXPositionAttribute, kAXSizeAttribute, kAXEnabledAttribute
        )
        from Cocoa import NSWorkspace
    except ImportError as exc:
        raise RuntimeError("This live reader must run on macOS with PyObjC installed.") from exc
    # The exact PyObjC AXValue unpacking can vary by macOS/PyObjC version.
    # First validate permission and frontmost-app discovery, then walk the AX tree.
    app = NSWorkspace.sharedWorkspace().frontmostApplication()
    pid = app.processIdentifier()
    ax_app = AXUIElementCreateApplication(pid)
    err, role = AXUIElementCopyAttributeValue(ax_app, kAXRoleAttribute, None)
    return [{
        "id": "frontmost-app",
        "name": f"Frontmost app: {app.localizedName()}",
        "role": str(role),
        "x": 0, "y": 0, "w": 1, "h": 1, "enabled": True
    }]
