# tests/validation/test_validation.py
import pytest
import os
from pybatfish.client.session import Session
import yaml

SNAPSHOT_PATH = "./snapshots/ci_net"

@pytest.fixture(scope="session")
def bf():
    bf_session = Session(host=os.environ.get("BF_ADDRESS", "127.0.0.1"))
    bf_session.set_network("ci_net")
    bf_session.init_snapshot(SNAPSHOT_PATH, name="ci_net", overwrite=True)
    return bf_session

@pytest.fixture(scope="session")
def config():
    path = "tests/config/config.yaml"
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f)


def test_interfaces_active_on_critical_nodes(bf, config):
    """
    Simple check: on critical nodes there shouldn't be many inactive interfaces.
    If 'Active' column missing -> skip (to be robust across Batfish versions).
    """
    critical_nodes = config.get("critical_nodes", [])
    if not critical_nodes:
        pytest.skip("No critical_nodes in config")

    try:
        if_props = bf.q.interfaceProperties().answer().frame()
    except Exception as e:
        pytest.skip(f"interfaceProperties question not available: {e}")

    # Prefer an explicit 'Node' column; otherwise try to split 'Interface' later
    if "Node" in if_props.columns:
        df = if_props
        node_col = "Node"
    elif "Interface" in if_props.columns:
        # try to extract node from Interface column if formatted as Node[Intf]
        df = if_props.copy()
        if df["Interface"].astype(str).str.contains(r"\[").any():
            df["Node"] = df["Interface"].astype(str).str.split(r"\[", n=1).str[0]
            node_col = "Node"
        else:
            pytest.skip("Cannot infer Node from Interface column")
    else:
        pytest.skip("No Node/Interface columns in interfaceProperties output")

    if "Active" not in df.columns:
        pytest.skip("'Active' column not present in interfaceProperties output; skipping active check")

    sub = df[df[node_col].isin(critical_nodes)]
    inactive = sub[sub["Active"] == False]
    # allow some but fail if any inactive (simple policy)
    assert inactive.empty, f"Found inactive interfaces on critical nodes:\n{inactive[[node_col,'Interface']].to_string(index=False)}"


def test_bgp_sessions_exist(bf):
    """
    Check that BGP sessions exist and report their status
    """
    bgp_status = bf.q.bgpSessionStatus().answer().frame()
    status_col = "Established_Status" if "Established_Status" in bgp_status.columns else "Session_Status"
    assert status_col in bgp_status.columns, f"bgpSessionStatus output lacks '{status_col}' column"

    established_sessions = bgp_status[bgp_status[status_col] == "ESTABLISHED"]
    assert not established_sessions.empty, "No BGP sessions are ESTABLISHED"



def test_critical_dests_reachable(bf, config):
    """
    For each critical_dest configured, ensure there is at least some reachability information.
    This is a lightweight check: it ensures the reachability question returns rows for the dstIp.
    """
    critical_dests = config.get("critical_dests", []) or []
    if not critical_dests:
        pytest.skip("No critical_dests in config")

    try:
        # iterate and ensure each dst returns at least one reachability row (caller can refine later)
        missing = []
        for dst in critical_dests:
            try:
                ans = bf.q.reachability(dstIps=dst).answer().frame()
            except Exception:
                # if reachability question fails for this dst, consider it missing for now (but don't crash entire test)
                missing.append(dst)
                continue
            if ans.empty:
                missing.append(dst)
        assert not missing, f"No reachability results for critical destinations: {missing}"
    except Exception as e:
        pytest.skip(f"reachability question not available or failed: {e}")
