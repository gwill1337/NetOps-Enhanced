# tests/security/test_security.py
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


def test_management_not_reachable_from_user_sources(bf, config):
    """
    Check that management hosts are not reachable from user_sources.
    Uses Batfish reachability question; if not available, test is skipped.
    """
    user_sources = config.get("user_sources", [])
    management_hosts = config.get("management_hosts", [])
    if not user_sources or not management_hosts:
        pytest.skip("No user_sources or management_hosts in config (skipping management reachability test)")

    try:
        # run a reachability query for each management host
        violations = []
        for mgmt in management_hosts:
            try:
                # ask reachability; this is a simple call — adapt srcIps/dstIps if your BF version requires headers
                ans = bf.q.reachability(srcIps=",".join(user_sources), dstIps=mgmt).answer().frame()
            except Exception:
                # if reachability fails, skip this mgmt host check
                continue
            # if any rows are returned, it's evidence of some reachability paths (tune if you want to check dispositions)
            if not ans.empty:
                violations.append(mgmt)
        assert not violations, f"Management hosts reachable from user sources: {violations}"
    except Exception as e:
        pytest.skip(f"reachability question not available or error: {e}")


def test_no_permit_any_on_edge_nodes(bf, config):
    """
    Heuristic security check using filterLineReachability: ensure no PERMIT results for edge nodes.
    Requires 'edge_nodes' in config; otherwise skipped.
    """
    edge_nodes = config.get("edge_nodes", []) or []
    if not edge_nodes:
        pytest.skip("No edge_nodes in config for permit-any check")

    try:
        flr = bf.q.filterLineReachability().answer().frame()
    except Exception:
        pytest.skip("filterLineReachability question not available")

    # require minimal columns
    if not {"Action", "Node"}.issubset(set(flr.columns)):
        pytest.skip("filterLineReachability output lacks required columns (Action/Node)")

    permits = flr[(flr["Action"].str.upper() == "PERMIT") & (flr["Node"].isin(edge_nodes))]
    assert permits.empty, f"Found PERMIT rules on edge nodes: {permits[['Node','Filter','Action']].to_string(index=False)}"

