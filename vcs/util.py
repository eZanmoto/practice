import git
import svn

impls = {
    'git': git,
    'svn': svn,
}


def detect_all():
    global impls
    return [impl for impl in impls.values() if impl.detect()]
