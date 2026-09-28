import hashlib
import json
import time


REFERENCE = "Specification: ALPHA and BETA are reserved examples."
PRIMARY = "Unrelated endpoint content."
BACKUP = "ALPHA and BETA are reserved examples."
REF_URL = "https://reference.example.org/spec"
PRIMARY_URL = "https://primary.example.com/data"
BACKUP_URL = "https://backup.example.net/data"


def setup_route(vm, deploy, alice, expected_hash=None):
    vm.mock_web(r"reference\.example\.org/spec", {"status": 200, "body": REFERENCE})
    vm.mock_web(r"primary\.example\.com/data", {"status": 200, "body": PRIMARY})
    vm.mock_web(r"backup\.example\.net/data", {"status": 200, "body": BACKUP})
    vm.mock_llm(r".*CANDIDATE=Unrelated endpoint content.*",
                json.dumps({"verdict": "MISMATCH"}))
    vm.mock_llm(r".*CANDIDATE=ALPHA and BETA are reserved examples.*",
                json.dumps({"verdict": "MATCH"}))
    contract = deploy("contracts/ConsensusFailoverRouter.py")
    vm.sender = alice
    contract.register_route("demo", PRIMARY_URL, BACKUP_URL, REF_URL,
                            expected_hash or hashlib.sha256(REFERENCE.encode()).hexdigest(),
                            "The document explicitly identifies ALPHA and BETA as reserved examples.", 3600)
    return contract


def test_failover_is_evidence_bound_and_replay_safe(direct_vm, direct_deploy, direct_alice):
    contract = setup_route(direct_vm, direct_deploy, direct_alice)
    assert contract.get_route("demo")["active"] == "FROZEN"
    assert contract.get_active_url("demo") == ""
    contract.probe_route("demo", 0, int(time.time()) + 3000)
    assert contract.get_route("demo")["active"] == "BACKUP"
    assert contract.get_active_url("demo") == BACKUP_URL
    report = json.loads(contract.get_probe("demo", 0))
    assert report["primary"]["verdict"] == "MISMATCH"
    assert report["backup"]["verdict"] == "MATCH"
    assert report["selected"] == "BACKUP"
    with direct_vm.expect_revert("current epoch"):
        contract.probe_route("demo", 0, int(time.time()) + 3000)


def test_reference_drift_freezes_route(direct_vm, direct_deploy, direct_alice):
    contract = setup_route(direct_vm, direct_deploy, direct_alice, "f" * 64)
    contract.probe_route("demo", 0, int(time.time()) + 3000)
    assert contract.get_route("demo")["active"] == "FROZEN"
    assert contract.get_active_url("demo") == ""
    report = json.loads(contract.get_probe("demo", 0))
    assert not report["reference"]["match"]
    assert report["selected"] == "FROZEN"


def test_primary_priority(direct_vm, direct_deploy, direct_alice):
    contract = setup_route(direct_vm, direct_deploy, direct_alice)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r"reference\.example\.org/spec", {"status": 200, "body": REFERENCE})
    direct_vm.mock_web(r"primary\.example\.com/data", {"status": 200, "body": BACKUP})
    direct_vm.mock_web(r"backup\.example\.net/data", {"status": 200, "body": PRIMARY})
    direct_vm.mock_llm(r".*CANDIDATE=ALPHA and BETA are reserved examples.*",
                       json.dumps({"verdict": "MATCH"}))
    direct_vm.mock_llm(r".*CANDIDATE=Unrelated endpoint content.*",
                       json.dumps({"verdict": "MISMATCH"}))
    contract.probe_route("demo", 0, int(time.time()) + 3000)
    assert contract.get_route("demo")["active"] == "PRIMARY"
    assert contract.get_active_url("demo") == PRIMARY_URL
