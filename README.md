- [A Security Engineer's Guide to Getting Ready for an Audit!](https://www.0xkato.xyz/Get-ready-for-an-audit/)
- [The Linux Boot Process: From Power Button to Kernel](https://www.0xkato.xyz/linux-boot/) — [[Featured on HN (peak rank 1)]](https://news.ycombinator.com/item?id=45707658)
- [A Friendly Tour of Process Memory on Linux](https://www.0xkato.xyz/linux-process-memory/) — [[Featured on HN (peak rank 3)]](https://news.ycombinator.com/item?id=45805539)
- [The Life of a Packet in the Linux kernel](https://www.0xkato.xyz/Get-ready-for-an-audit/](https://www.0xkato.xyz/life-of-a-packet-in-the-linux-kernel/))
- [How CPU Caches Work](https://www.0xkato.xyz/How-CPU-Caches-Work/](https://www.0xkato.xyz/How-CPU-Caches-Work/))


### Vulnerability Research

| Protocol | description | link |
| -------- | ---- |  ---------|
| [fmt](https://github.com/fmtlib/fmt) | Command injection in `fmt::say()` on macOS | [link](https://github.com/fmtlib/fmt/security/advisories/GHSA-65g5-63wg-xjh4) |
| [keepassxc](https://github.com/keepassxreboot/keepassxc) | Missing check for duplicate group UUID causes crash | [link](https://github.com/keepassxreboot/keepassxc/issues/12706) |
| [prometheus](https://github.com/prometheus/prometheus) | tsdb: guard chunk length overflow in head chunk reader | [link](https://github.com/prometheus/prometheus/pull/17533#event-20963840575) |
| [prometheus](https://github.com/prometheus/prometheus) | missing size caps to all important Snappy/OTLP remote read/write decoders | [link](https://github.com/prometheus/prometheus/pull/17545) |
| [prometheus](https://github.com/prometheus/prometheus) | iterating over histogram buckets can panic | [link](https://github.com/prometheus/prometheus/pull/17559) |
| [prometheus](https://github.com/prometheus/prometheus) | Missing histogram validation in remote-read and during reducing resolution | [link](https://github.com/prometheus/prometheus/pull/17561) |
| [serialize](https://github.com/mas-bandwidth/serialize) | Buffer Overflow in Serialize Library | [link](https://github.com/mas-bandwidth/serialize/pull/9) |

# 0xkato's security reviews

This repo is made to showcase some of the security reviews that I have done/participated in

### Espresso Audits
| Protocol | Protocol Type | Report |
| ---- |  ---------| ---------|
| [Espresso Systems](https://www.espressosys.com/) | HotShot Consensus Protocol | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/HotShot/EspressoHotshot2024.pdf)
| [Espresso Systems](https://www.espressosys.com/) | HotStuff Consensus Mechanism | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/HotShot/EspressoHotstuff22025.pdf)
| [Espresso Systems](https://www.espressosys.com/) | Consensus Rewards Mechanism | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/HotShot/Rewards2025.pdf)
| [Espresso Systems](https://www.espressosys.com/) | Nitro Caffeinated Node | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/Integration/EspressoNitroCaffeinatedNode2025.pdf)
| [Espresso Systems](https://www.espressosys.com/) | Nitro Stateless Batcher V1 | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/Integration/StatelessBatcherV12025.pdf)
| [Espresso Systems](https://www.espressosys.com/) | Fee Contract | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/Sequencer/EspressoFeeContract2024.pdf)
| [Espresso Systems](https://www.espressosys.com/) | Espresso Sequencer | [Report](https://github.com/0xkato/Portfolio/blob/main/Espresso/Sequencer/EspressoSequencer2024.pdf)

### Guardian audits

| Protocol | Protocol Type | Report |
| ---- |  ---------| ---------|
| [GMX](https://gmx.io/#/) | Derivatives | [Reports](Guardian/GMX)
| [Abracadabra](https://abracadabra.money/) | CDP | [Report](https://github.com/0xkato/Portfolio/blob/main/Guardian/11-14-2023_Abracadabra_GMXV2.pdf)
| [Poolshark](https://www.poolshark.fi/) | Dex | [Reports](Guardian/Poolshark)
| [IVX](https://www.ivx.fi/) | Options | [Report](https://github.com/0xkato/Portfolio/blob/main/Guardian/09-13-2023-IVX.pdf)
| [PariFi](https://parifi.org/) | Perpetuals | [Report](https://github.com/0xkato/Portfolio/blob/main/Guardian/09-03-2023-PariFi.pdf)
| [Ambit](https://ambit.finance/) | Lending | [Report](https://github.com/0xkato/Portfolio/blob/main/Guardian/2023-12-06_Ambit.pdf)
| [Umami](https://umami.finance/) | Yield | [Report](https://github.com/0xkato/Portfolio/blob/main/Guardian/2024-01-10_Umami.pdf)

### Private audits

| Protocol | Protocol Type | Report |
| ---- |  ---------| ---------|
| [Lexer Markets](https://www.lexer.markets/) | Derivatives | [Report](https://github.com/0xkato/Portfolio/blob/main/Solo/Security_Review_Lexer_Markets_Final_Report.pdf)
| [Ambit](https://ambit.finance/) | Lending | [Report](https://docs.ambit.finance/audits/0xweiss-feb24.pdf)
| [Ceden Network](https://ceden.network/) |  | 
| [Hyperstable](https://hyperstable.xyz/) |  | 

### Contact

If you want to talk security I can be reached [@0xkato](http://twitter.com/0xkato).
