from typing import List

from hana04.base.changeprop.versioned_subject import VersionedSubject


def largest_between_inc_self_and_deps(self: VersionedSubject, dependencies: List[VersionedSubject]) -> int:
    new_version = self.version() + 1
    if len(dependencies) == 0:
        return new_version
    else:
        return max(new_version, max([dep.version() for dep in dependencies]))