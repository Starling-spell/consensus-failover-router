# Finalized StudioNet proof matrix

Contract: [0x12a2a1C2eb64fA24f7a7488a3789Cd8A0818f34A](https://explorer-studio.genlayer.com/address/0x12a2a1C2eb64fA24f7a7488a3789Cd8A0818f34A)

The deployed contract code, local contract file, and source at GitHub commit [`73e6926`](https://github.com/Starling-spell/consensus-failover-router/commit/73e6926) were byte-identical (SHA-256 `0455246e033d162aa99e6038ece78fbc0ad2c95c403615bad6534583b3ff9596`). Every transaction below was checked at `FINALIZED` with leader execution `SUCCESS`.

| Case | Transaction | Observed onchain result |
| --- | --- | --- |
| Deploy | [0xd2a7d3ab…](https://explorer-studio.genlayer.com/tx/0xd2a7d3ab024126e028a90640acb865e47a82421888424376a5ff4a4dfdf74581) | Contract created |
| Register backup route | [0x7cfe22d3…](https://explorer-studio.genlayer.com/tx/0x7cfe22d3a03d7ed618eb8b320e1ab11fceb179d877f354315987f206f82e75aa) | Starts `FROZEN` |
| Probe backup route | [0xefc8e1e4…](https://explorer-studio.genlayer.com/tx/0xefc8e1e44ac25681d0ec93b200266a250f15ed30ba324858067d22e1351da165) | Primary `MISMATCH`; backup `MATCH`; selects `BACKUP`, epoch 1; root `2205aea6c74f6cc7eea93346c16c6bc9325e2c0260bc75ea994051a3886f1802` |
| Register primary route | [0x6a1308ed…](https://explorer-studio.genlayer.com/tx/0x6a1308ed5c84b628019e5d4f795c04964d620a870f713ba8c98e322f219ba7b1) | Starts `FROZEN` |
| Probe primary route | [0x8b41acb0…](https://explorer-studio.genlayer.com/tx/0x8b41acb00c5a6794555a64fca6a30e92003b66954a60b056863f428fddce2ba0) | Primary `MATCH`; backup `MISMATCH`; selects `PRIMARY`, epoch 1; root `c878df247782a6b6ef35227e846f2e396fdab0e036dbf02179a7a5ba0f24fbc9` |
| Register frozen route | [0xf36ff417…](https://explorer-studio.genlayer.com/tx/0xf36ff4179a8206efa24a116da3c88436dd0b84a01549f046e8bd09da9ec72a6e) | Starts `FROZEN` |
| Probe frozen route | [0x5f8adfdb…](https://explorer-studio.genlayer.com/tx/0x5f8adfdbf12b1a8cb1bc4a3c85d4d1010862a0dc2e472bd791c780e21b6db0a7) | Both candidates `MISMATCH`; remains `FROZEN`, epoch 1; root `d9b0d5568dfed8f97197909c8544ff400f90b361863f97c923baf21550c8474d` |
| Register drift route | [0x43efc4c8…](https://explorer-studio.genlayer.com/tx/0x43efc4c86313daff69d5e46e9712a69b28ec4b6ba3c0f0323127cbf3fe63b9f8) | Reference commitment intentionally wrong |
| Probe drift route | [0x6ee35e4d…](https://explorer-studio.genlayer.com/tx/0x6ee35e4df7e803f1a6d6a423bacfa104441e619e2248bae89b96580195e5a76e) | Fetched reference hash mismatched commitment; both verdicts `UNKNOWN`; remains `FROZEN`, epoch 1; root `2a5687a2c335bec13f529c91578334ee4e8f0f44fa9f746696aa356f98e4b16e` |

Reference: [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.txt), full-response SHA-256 `b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0`. Candidate authorities: [IANA](https://www.iana.org/domains/reserved), [example.com](https://example.com/), and [example.net](https://example.net/). Probe reports showed HTTP 200 and the expected reference hash in the first three cases. `get_active_url` returned IANA for the selected backup and primary cases and an empty string for the frozen case.

These proofs establish the stated routing outcomes for these public documents. They do not establish private service delivery, continuous endpoint health, or reviewer acceptance. A consumer must check route freshness at use time.
