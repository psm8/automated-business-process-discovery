from process_discovery.gate.lop_gate import LopGate
from process_discovery.gate.xor_gate import XorGate
from process_discovery.util.util import in_by_is


def get_parent_lop(gate):
    if gate.parent is not None:
        if isinstance(gate.parent, LopGate):
            return gate.parent
        return get_parent_lop(gate.parent)
    else:
        return None


def is_any_parent_enabled_xor(gate, x, previous_events) -> bool:
    return not any(isinstance(y, XorGate) and any(in_by_is(z, previous_events) for z in y.elements) for y in
                   gate.find_child_parents(x))


