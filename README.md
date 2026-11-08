# pump.fun launch data: free 7-day sample

Per-launch evidence about how pump.fun tokens were launched: who bought in the first slots and the first second, serial
snipers, bundled wallets, early buyers who share a funding wallet, what the creator did, and whether the name, symbol or
image was copied from another launch. Every row also carries a SAFE / WARN / DANGER label with its reason codes, computed
from published fixed thresholds.

This repo holds a free, verifiable sample: **7,430 launches** (1 in 32 of all pump.fun launches, 30 Oct to 5 Nov 2026 UTC),
**37 columns**, 0.65 MB. Public Solana chain data only: no personal or off-chain data.

## Check it in one minute

```bash
sha256sum -c SHA256SUMS 2>/dev/null | grep csv.gz   # pumpfun-launch-sample-20261030-20261105.csv.gz: OK
python3 stats.py                                     # standard library only
```

`stats.py` prints:

```
rows: 7,430 launches (1 in 32 of all pump.fun launches, 30 Oct-5 Nov 2026 UTC); 5,610 with launch-tape features
sampling rule holds for every row: True
a buyer within 1 second of the mint: 49.3% of 5,610 launches with tape
at least one serial sniper among the first buyers: 43.9% of 5,610
name, symbol or image reused within 7 days: 32.8%
graduated from the bonding curve: 169 (2.27%); median time to graduate 36.4 s
verdicts: SAFE 1,305 (17.6%), WARN 3,784 (50.9%), DANGER 2,341 (31.5%)
```

The sample is deterministic: a mint is in it when `int(md5(mint)[0:8], 16) % 32 == 0`. Anyone can rebuild the same set
from chain data and compare.

```python
import pandas as pd
df = pd.read_csv("pumpfun-launch-sample-20261030-20261105.csv.gz", parse_dates=["created_at", "graduated_at"])
df.groupby("verdict")["graduated_at"].apply(lambda s: s.notna().mean())
```

## Columns

| Column | Meaning |
|---|---|
| mint, symbol, creator, created_at, graduated_at | token, creator wallet, launch time, bonding-curve graduation time (UTC; empty = not graduated) |
| initial_buy_tokens | the creator's buy in the create transaction (supply is 1,000,000,000) |
| creator_prior_launches, creator_prior_graduations | the creator's launches and graduations before this one |
| creator_sold_by_10m | the creator sold within 10 minutes |
| window_s, tape_complete, tape_note | launch-tape window length (s) and whether the tape had a gap |
| pct_supply_first_2_slots, creator_supply_pct | % of supply bought in the first 2 slots, by anyone and by the creator |
| creation_slot_buyers, first2_slot_buyers, early_1s_buyers | distinct non-creator buyers in the creation slot, first 2 slots, first second |
| serial_snipers | early buyers already seen sniping other launches |
| bundle_txs, bundled_wallets, bundled_supply_pct | multi-buyer bundled transactions at launch and the supply they took |
| largest_funder_group, shared_funder_wallets | early buyers that share a funding wallet |
| creator_sold_in_window, cohort_deployer_funded | creator sold inside the window; early buyers funded by the deployer |
| name_collisions_7d, symbol_collisions_7d, image_collisions | metadata reused by other launches (clone detection) |
| creator_launches, creator_graduations | the creator wallet's lifetime totals |
| cluster_size, cluster_launches, cluster_graduations | the creator's funding cluster |
| top10_ex_pool_pct | RugCheck top-10 holders excluding the pool (after graduation only) |
| verdict, reason_codes, verdict_basis | label, pipe-separated reasons, and what the label was computed from |

The thresholds behind every reason code are published at
`https://agents.avasis.ai/v1/sol/launch-intel/info`. No evidence is never SAFE.

## Honest limits

- **Not a prediction or trading advice.** In this sample, DANGER launches graduated more often (5.6%) than WARN (1.0%) or
  SAFE (1 of 1,305): launches that take off attract snipers and bundles. A label describes how a launch was run.
- Snipers, bundles and funder links are heuristics over observed transactions.
- 24.5% of rows have no batch tape features (no trades in the window); those are WARN or DANGER, never SAFE.
- The continuous record starts 30 Aug 2026. Nothing earlier exists as a continuous record.

## The full data

About 31,000-40,000 launches a day, every launch, since 30 Aug 2026 (about 1.7 million so far, one more day each night).
Buy from any wallet that holds USDC on Base (no account) at
**https://avasis.ai/data/pumpfun-launch-intel/#buy**, or pay per call from code over x402:

| What | Price |
|---|---|
| One finished UTC day, csv.gz | $5 |
| Last 7 days / last 30 days, one csv.gz | $25 / $79 |
| Data licence: live API, SSE firehose, every daily file, 30 days | $199 |
| Full history since 30 Aug 2026, one tar with a sha256 manifest | $999 |
| Per call: trap check $0.02, creator record $0.01, firehose poll $0.002 | x402 |

Free API answers, no key:

```bash
curl https://agents.avasis.ai/v1/sol/launch-intel/sample/trap-check
curl https://agents.avasis.ai/v1/sol/launch-intel/sample/creator
curl https://agents.avasis.ai/v1/sol/launch-intel/sample/launch-firehose
```

Enterprise, resale or redistribution: abhay@avasis.ai.

## Licence

The sample files in this repository: see `LICENSE`. The full dataset and the API are licensed separately for internal use and
research (no resale or redistribution without written permission).
