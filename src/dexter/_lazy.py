"""Helpers for lazy attribute imports (PEP 562) and per-package help().

Keeping imports lazy means `import dexter` stays fast: pyomo, scipy, sympy,
pandas and plotly only load when something that needs them is first used.
"""

import builtins
import importlib


def lazy_exports(package, exports):
    """Return ``(__getattr__, __dir__, help)`` for a package.

    ``exports`` maps each public name to ``(submodule, summary)``. The
    submodule is relative to ``package``; ``None`` means the name is itself a
    subpackage. Nothing is imported until the attribute is first used, and
    ``help()`` prints the summaries without importing anything.
    """
    def _module():
        return importlib.import_module(package)

    def __getattr__(name):
        if name not in exports:
            raise AttributeError(f"module {package!r} has no attribute {name!r}")
        module = exports[name][0]
        if module is None:
            value = importlib.import_module(f".{name}", package)
        else:
            value = getattr(importlib.import_module(f".{module}", package), name)
        _module().__dict__[name] = value  # cache, so __getattr__ runs once per name
        return value

    def __dir__():
        return sorted(set(_module().__dict__) | set(exports))

    def help(name=None):
        """Print what this package offers, or the full docs for one name."""
        if name is not None:
            return builtins.help(__getattr__(name) if name in exports else name)

        doc = (_module().__doc__ or "").strip().splitlines()
        lines = [package, doc[0] if doc else ""]
        subpackages = {n: s for n, (m, s) in exports.items() if m is None}
        contents = {n: s for n, (m, s) in exports.items() if m is not None}
        width = max(map(len, exports)) + 2
        for title, entries in (("Subpackages", subpackages), ("Contents", contents)):
            if entries:
                lines += ["", f"{title}:"]
                lines += [f"  {n:<{width}}{s}" for n, s in entries.items()]
        lines += ["", f"{package}.help('<name>') shows the full docs for one name."]
        if subpackages:
            lines.append(f"{package}.<subpackage>.help() lists that subpackage.")
        print("\n".join(lines))

    return __getattr__, __dir__, help
