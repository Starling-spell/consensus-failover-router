# ConsensusFailoverRouter

A GenLayer primitive for switching a public information route only when independent validators observe that the selected endpoint satisfies a pinned reference requirement. It is a routing state machine, not a graph-edit workflow, claim certificate, or one-time authorization token.

## Problem and consensus boundary

A conventional failover monitor checks HTTP availability. A page can return HTTP 200 while serving an unrelated error, stale placeholder, or materially different document. Here, the contract owns the active routing decision. It fetches the reference and both candidate endpoint bodies during each permissionless probe, verifies the exact reference SHA-256, and asks leader and validators to independently classify each candidate against the reference and route requirement. The full normalized evidence report and selected route must agree exactly.

The operator supplies endpoint URLs and the requirement, but cannot supply a probe verdict, bypass a failed reference hash, or finalize a probe. All three HTTPS hostnames must differ. The reference document is content-addressed; changing it requires a new route ID. No endpoint is usable before a successful probe.

```text
register_route ──> FROZEN
                     │
            permissionless probe_route
                     │
        fetch reference + primary + backup
                     │
      independent semantic validator review
                     │
       PRIMARY / BACKUP / FROZEN
                     │
      expires after registered TTL
```

The candidate bodies are untrusted evidence, not instructions. A probe stores the status, full-response hash, bounded semantic verdict, selection, timestamp, and deterministic root. A new probe requires the current epoch; prior reports are immutable. If the pinned reference drifts, both endpoints fail, or semantic evidence is uncertain, the route freezes. `get_active_url` returns an empty string when frozen or expired. A caller may trigger a new probe without operator approval.

## API

- `register_route(route_id, primary_url, backup_url, reference_url, reference_hash, requirement, ttl_seconds)`
- `probe_route(route_id, expected_epoch, deadline)`
- `get_route(route_id)`, `get_active_url(route_id)`, `get_probe(route_id, epoch)`

## Demonstration

The pinned reference is [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.txt). A public [IANA reserved-domains page](https://www.iana.org/domains/reserved) is a candidate that discusses example domains; [example.com](https://example.com/) is a deliberately nonconforming candidate for the narrower route requirement. These are three distinct authorities. The demo tests backup selection, primary selection, frozen routing, and reference-hash drift without pretending that endpoint content proves service delivery beyond the stated documentation criterion. Finalized deployment and probe receipts are listed in [LIVE_PROOFS.md](LIVE_PROOFS.md).

## Verification

Run `genvm-lint check contracts/ConsensusFailoverRouter.py`, then `pytest tests/direct -q`. Direct tests cover source drift, failover, primary priority, immutable epoch replay, and the frozen-route consumer gate; they do not exercise full validator consensus or the passage of real TTL time. StudioNet execution provides separate consensus evidence. GenVM is pinned in the contract header.

Set the GenLayer CLI network to `studionet`, deploy `contracts/ConsensusFailoverRouter.py`, and inspect every transaction with `genlayer receipt <hash> --status FINALIZED`. A finalized transaction is not proof of execution success unless its leader receipt says `SUCCESS`. Compare `genlayer code <address>` to the committed source before citing a deployment.

## Security limits

This contract evaluates public documents, not private API behavior or service delivery. Distinct hostnames do not prove organizational independence; operators should choose separate providers. A malicious endpoint may change between validator fetches, preventing consensus. A source may change after a successful probe; consumers must use `get_active_url`, which enforces the registered TTL, and probe again for fresh routing. The onchain reference hash binds bytes, not the legitimacy of the chosen policy. The operator is responsible for choosing a meaningful reference and requirement.
