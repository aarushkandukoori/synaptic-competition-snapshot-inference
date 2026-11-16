# Inferring Synaptic Competition Dynamics from Static Connectomic Snapshots: A Simulation-Based Inference Framework

**Aarush Kandukoori** (Carnegie Mellon University) — Lead Student Author  
**Aditya Kandukoori** (Poolesville High School) — Co-Author

> **Status: early-stage research proposal.** No experimental results
> are claimed. We are actively seeking expert feedback.

## Abstract

Connectomic reconstructions give highly detailed but static views of neural wiring, whereas developmental synaptic competition, such as the elimination of all but one of the axonal inputs to each neuromuscular junction, unfolds over time. Complete neuromuscular connectomes reconstructed from birth through postnatal development now make multi-age snapshots of this process available. We outline an early-stage framework that treats cross-sectional connectomic snapshots at different ages as samples from an underlying stochastic competition process. A simple replicator-style model of input-share dynamics at each junction is paired with simulation-based Bayesian inference to recover the competition parameters that are identifiable from snapshot statistics. We describe the model, work out which parameter combinations are and are not identifiable, outline a variant in which each axon carries a single advantage shared by all the junctions it innervates, and plan an evaluation on clearly-labeled synthetic data only. No experiments have been run, and we are seeking expert feedback on whether the formulation matches how connectomics researchers think about synapse elimination. AI tools (Claude) were used for literature synthesis, ideation, and draft preparation, and the authors reviewed and take responsibility for all content.

## Introduction & Motivation

During early postnatal development, each neuromuscular junction (NMJ) is initially innervated by several motor axons, and all but one of these inputs are later eliminated. This is a classic case of synaptic competition. Time-lapse in vivo imaging can watch it directly, but only in accessible preparations and for limited durations. Connectomic reconstruction, by serial-section electron microscopy or light microscopy, instead gives complete wiring diagrams, but each animal contributes only one frozen moment.

Recent work makes this setting concrete: complete connectomes between motor neurons and muscle fibers have been reconstructed in small mouse muscles from birth through successive stages of postnatal development, and the loss of axons was related to the recruitment order of the innervating axons [meirovitch2026]. Complete wiring at several ages, with each reconstruction frozen at one moment, is exactly the kind of data our framework takes as input.

This proposal is **early-stage** and asks one narrow question: *given connectomic snapshots from animals at several ages, which parameters of a competition process can be recovered, and with what uncertainty?* We do not claim to answer it. An explicit dynamical model would complement analyses such as those in [meirovitch2026] by making it possible to ask which rates and thresholds snapshots can and cannot pin down. We want feedback on whether the question is well posed, whether the model is too simple to be useful, and what data a connectomics group would actually have available.

Contributions we aim for, to our knowledge as a small and modest step: (1) a minimal, mathematically checkable competition model at single junctions, with an axon-level variant motivated by the rank-ordered co-innervation reported in [meirovitch2026]; (2) an explicit identifiability analysis; (3) a plan for amortized simulation-based inference with calibration checks, all on synthetic data.

## Related Work

**Developmental neuromuscular connectomics.** Meirovitch et al. [meirovitch2026] report an approximately 6.5-fold decrease in the number of axons innervating each NMJ during postnatal development, ending in single innervation of every junction; the elimination of most of the extra junctions on muscle fibers that start with more than one; and a link between both kinds of loss and the recruitment order of the innervating axons, reflected in a rank-ordered pattern of co-innervation. They argue that competition both within and between junctions is activity-mediated. These findings motivate two choices below: the unit of competition is a single junction, and, in a variant, the advantage of an input is a property of its axon that is shared by all the junctions that axon innervates.

**Connectomic reconstruction.** Saturated EM reconstruction of neural tissue [kasthuri2015] and automated segmentation methods such as flood-filling networks [januszewski2018] and 3D convolutional approaches [lee2017] produce the axon-to-target wiring and synapse-size data that our framework would take as input. We model segmentation errors only crudely (see the observation model) and list them under limitations.

**Activity-dependent plasticity theory.** Competition-style rules in synaptic plasticity have a long history, for example the BCM theory [bienenstock1982]. Our replicator-style model is far simpler and is intended as a statistical scaffold rather than a biophysical claim.

**Learning on graphs.** Wiring data is naturally a bipartite graph (axons and targets). Inductive graph neural networks such as GraphSAGE [hamilton2017] provide a baseline summary network. Such a summary matters most in the axon-level variant, where one axon connects many junctions.

**Simulation-based inference.** When a likelihood is intractable but a simulator exists, neural conditional density estimation [papamakarios2016] and the broader SBI toolkit [cranmer2020] allow posterior estimation, and simulation-based calibration [talts2018] provides a check that posteriors are self-consistent.

## Proposed Framework

**Setup.** Consider one target, a single neuromuscular junction $j$, with $n$ competing axonal inputs $i \in \{1,\dots,n\}$ present at the reference time and positive input strengths $w_i(t)$ (for instance, the synaptic area each axon occupies at the junction). Time $t \ge 0$ is measured from a reference age, which we take to be birth, so $t$ is postnatal age. Let $W=\sum_i w_i$ and the share $p_i = w_i / W$.

**Replicator-style competition.** Suppose each input has an effective advantage $a_i$, a dimensionless latent scalar. It could summarize, for example, activity-timing differences such as the recruitment order that [meirovitch2026] relate to synaptic fate, but we do not assume a mechanism. Let
$$\frac{dw_i}{dt} = \eta\, w_i\,(a_i - \bar a),\qquad \bar a = \sum_k p_k a_k ,$$
where $\eta>0$ is a rate constant with units of 1/time.
Checks: (i) $\frac{dW}{dt} = \eta \sum_i w_i (a_i-\bar a) = \eta W(\bar a - \bar a)=0$, so total strength is conserved. (ii) Shares then obey the replicator equation $\dot p_i = \eta\, p_i (a_i-\bar a)$.

**Closed form.** For constant $a_i$, $p_i(t) = p_i(0)e^{\eta a_i t} / \sum_k p_k(0)e^{\eta a_k t}$. Hence for any pair, $\log\frac{p_i(t)}{p_k(t)} = \log\frac{p_i(0)}{p_k(0)} + \eta (a_i-a_k)\,t$.

**Elimination.** Shares are always computed over all $n$ initial inputs of a junction, and an input counts as eliminated at age $t$ if $p_i(t) < \theta$, where $\theta \in (0,\tfrac12)$ is a fixed elimination threshold; the largest input is always kept. Because $\frac{d}{dt}\log p_i = \eta(a_i-\bar a)$ and $\frac{d\bar a}{dt} = \eta\sum_k p_k (a_k-\bar a)^2 \ge 0$, each $\log p_i(t)$ is concave in $t$, so an input that starts above $\theta$ and later falls below it stays below: for such inputs, being below $\theta$ at the observation age is the same as having crossed $\theta$ earlier. For two inputs with $x(t)=\log(p_1/p_2)$, $p_2 = 1/(1+e^{x})$, so $p_2<\theta \iff x > \log\frac{1-\theta}{\theta}$. With $\Delta=a_1-a_2>0$ and $x(0)=x_0<\log\frac{1-\theta}{\theta}$, the elimination time is
$$t^* = \frac{\log\frac{1-\theta}{\theta} - x_0}{\eta\,\Delta}.$$

**Identifiability.** The dynamics have two symmetries. (1) *Scaling:* $(\eta, a)\to(c\eta, a/c)$ for any $c>0$ leaves every product $\eta a_i$, and hence every $p_i(t)$, unchanged. (2) *Shift:* $a_i \to a_i + c$ for all $i$ at a target leaves $p_i(t)$ unchanged, because $\bar a$ moves by the same constant $c$ and $a_i-\bar a$ is unchanged (equivalently, the common factor $e^{\eta c t}$ cancels in the closed form). Therefore, from snapshots, at most the scaled within-target differences $\eta(a_i-a_k)$ are identifiable; $\eta$ is not separately identifiable without time-lapse data or an independent time scale, and the overall level of the advantages is not identifiable at all.

We therefore parameterize directly in terms of identifiable quantities. For each target, define the relative advantages $\beta_i = \eta\,(a_i - \bar a_{\text{target}})$, where $\bar a_{\text{target}} = \frac1n\sum_{k=1}^n a_k$ is the unweighted mean advantage over the inputs of that target, so that $\sum_i \beta_i = 0$ within each target and $p_i(t)\propto p_i(0)\,e^{\beta_i t}$. In the simulator we draw $b_i \sim \mathcal N(0,\sigma_\beta^2)$ independently and set $\beta_i = b_i - \frac1n\sum_k b_k$, which places the population prior on within-target differences only. The observation time $t_{\text{age}}$ is known from animal age. The parameters of interest are $\phi=(\sigma_\beta,\theta,\sigma_0)$: $\sigma_\beta$ is the spread of relative advantages, $\theta$ the elimination threshold, and $\sigma_0$ the spread of initial log-shares, where $\log p_i(0)$ is drawn as $\mathcal N(0,\sigma_0^2)$ before normalizing to sum to one. A population mean of the advantages is not part of $\phi$ because it is not identifiable from snapshots.

**Axon-level variant (planned extension, not yet in the reference code).** The basic model draws advantages independently at every junction, whereas [meirovitch2026] report a rank-ordered pattern of co-innervation across a muscle, which suggests that an input's advantage is partly a property of its axon. In the variant, the motor axons of one animal's muscle are indexed by $m \in \{1,\dots,M\}$, input $i$ at a junction comes from axon $m(i)$, and the per-input draw above is replaced by $b_i = u_{m(i)}$, where $u_m \sim \mathcal N(0,\sigma_\beta^2)$ is drawn once per axon; as before, $\beta_i = b_i - \frac1n\sum_k b_k$ within each junction. In the synthetic setting, each junction's $n$ initial axons are drawn uniformly without replacement from the $M$ axons; a newborn connectome could replace this draw. Here $u_m$ plays the role of $\eta a$ for axon $m$, so the scaling symmetry is already factored out, and the shift symmetry becomes one constant added to every $u_m$ of the muscle. At most the differences $u_m - u_{m'}$ are therefore identifiable, and only between axons linked by chains of junctions at which they competed. Because the two-input elimination time $t^*$ is inversely proportional to the advantage difference, the variant implies that axons still sharing a junction at a given age tend to have similar $u_m$. If $u_m$ changed monotonically with recruitment rank, co-innervation at intermediate ages would then tend to concentrate among axons adjacent in that rank, qualitatively like the pattern reported in [meirovitch2026]. The $u_m$ are animal-specific latent variables, while $\phi$ is shared across animals.

**Observation model.** At age $t$, a snapshot yields for each target $j$ the number of surviving inputs and their size shares, with measurement noise from segmentation (multiplicative log-normal noise on $w_i$, and a small probability of missed or falsely merged inputs). The summary of a snapshot is the empirical distribution of innervation numbers and of the largest-to-second-largest log ratio per target, by age. In the axon-level variant, the snapshot also records which axon supplies each input, and the summary adds the matrix that counts, for each pair of axons, the junctions they share at that age.

**Inference.** Because the likelihood marginalizes over latent $\beta_i$ (in the variant, the $u_m$) and thresholded elimination, we use simulation-based inference: draw $\phi$ from a prior, simulate snapshot data at the observed ages, and train a conditional density estimator $q_\psi(\phi \mid s)$, with network parameters $\psi$, on summaries $s$ [papamakarios2016, cranmer2020]. The summary network is either hand-built statistics or a graph network over the axon-target bipartite graph [hamilton2017].

## Methodology

**Simulator.** Implement the closed-form share dynamics above for many targets in parallel, with per-target random initial shares, a random number of initial inputs, and elimination at threshold $\theta$ evaluated at the observation age. The current synthetic configuration draws 2 to 6 initial inputs per target; because [meirovitch2026] report an approximately 6.5-fold reduction in the number of axons per junction between birth and single innervation, a configuration meant to resemble newborn muscle would use larger counts. Add a segmentation-noise layer. The axon-level variant would add an axon label to each input and the per-axon draws $u_m$.

**Estimators compared.** (a) Moment matching on the summary statistics; (b) ABC rejection; (c) neural posterior estimation on hand-crafted summaries; (d) neural posterior estimation with a graph-network summary.

**Synthetic data statement.** The proposed repository uses **clearly-labeled synthetic/mock data only**, generated by the simulator. No real connectomic data, animal data, or data from any laboratory is used or implied.

**AI Assistance Disclosure.** AI tools (Claude) were used for literature synthesis, ideation, and draft preparation. The authors reviewed and take responsibility for all content, including the model, derivations, and citations.

**Reproducibility.** Seeds, simulator parameters, and prior ranges will be fixed in versioned config files.

## Planned Evaluation & Baselines

This section describes a protocol only; no results exist yet.

1. **Parameter recovery on synthetic data.** Generate datasets from known $\phi^\ast$, run each estimator, and compare posterior summaries to $\phi^\ast$ (error and coverage of credible intervals) across dataset sizes (number of targets) and numbers of ages.
2. **Calibration.** Apply simulation-based calibration rank tests [talts2018] to the neural estimators.
3. **Identifiability check.** Verify empirically that datasets simulated with $(\eta, a)$ and $(c\eta, a/c)$ give indistinguishable posteriors (scaling symmetry), and that datasets simulated with $a_i$ and $a_i + c$ (a constant shift applied to all inputs of a target) give identical share trajectories $p_i(t)$ and indistinguishable posteriors (shift symmetry), as the analysis predicts.
4. **Robustness to noise.** Vary segmentation noise rate and merge/split probabilities, and measure degradation.
5. **Misspecification.** Simulate from a different generator (e.g., time-varying $a_i$, or an additional stochastic jump term) and fit the constant-advantage model, to see whether the posterior flags the mismatch.
6. **Axon-level variant.** In simulations of the variant, check that co-innervation at intermediate ages concentrates among axons adjacent in the order of the simulated $u_m$, as the variant implies; test whether that order can be recovered from one snapshot's co-innervation matrix (for example by a simple seriation of the matrix); and compare posteriors over $\phi$ with those of the per-input model.

Baselines (moment matching, ABC) are the simple reference points. Any claim of improvement would be made only after these experiments are actually run.

## Limitations & Open Questions

- **Model simplicity.** Constant per-input advantages and total-strength conservation are strong assumptions. Real competition likely depends on activity patterns, position, and molecular factors.
- **Cross-sectional inference.** Different animals at different ages are not a trajectory; between-animal variability is confounded with dynamics.
- **Identifiability.** Only scaled within-target differences of advantages are identifiable from snapshots, as shown above. Absolute rates need other data, and the mean (overall level) of the advantages is not recoverable at all because of the shift symmetry.
- **Segmentation error.** Input counts and sizes depend on reconstruction quality, which we model only crudely.
- **Independent junctions and interjunctional competition.** The basic model treats junctions as independent, whereas [meirovitch2026] report rank-ordered co-innervation across a muscle; the axon-level variant addresses this only through one constant advantage per axon and random initial wiring. They also report the elimination of entire junctions on muscle fibers that start with more than one, which our model, limited to competition within a junction, does not describe.
- **Generality.** The model is framed around many-to-one convergence; other connectivity-development settings may need different formulations.
- **Open questions for experts.** What snapshot summaries are routinely available, for example the synaptic area of each axon at a junction, or only which axons are present? Which ages would be sampled? Is the elimination threshold a sensible abstraction? Would an explicit competition model be useful alongside rank-order analyses of co-innervation such as those in [meirovitch2026]?

## References

- [meirovitch2026] Meirovitch et al., *Connectomic evidence that ordered activity drives neuromuscular network formation*, Nature Neuroscience 2026. https://doi.org/10.1038/s41593-026-02344-7
- [kasthuri2015] Kasthuri et al., *Saturated Reconstruction of a Volume of Neocortex*, Cell 2015. https://doi.org/10.1016/j.cell.2015.06.054
- [januszewski2018] Januszewski et al., *High-precision automated reconstruction of neurons with flood-filling networks*, Nature Methods 2018. https://doi.org/10.1038/s41592-018-0049-4
- [lee2017] Lee et al., *Superhuman Accuracy on the SNEMI3D Connectomics Challenge*, arXiv preprint 2017. https://arxiv.org/abs/1706.00120
- [hamilton2017] Hamilton et al., *Inductive Representation Learning on Large Graphs*, NeurIPS 2017. https://arxiv.org/abs/1706.02216
- [bienenstock1982] Bienenstock et al., *Theory for the development of neuron selectivity: orientation specificity and binocular interaction in visual cortex*, Journal of Neuroscience 1982. https://doi.org/10.1523/JNEUROSCI.02-01-00032.1982
- [cranmer2020] Cranmer et al., *The frontier of simulation-based inference*, Proceedings of the National Academy of Sciences 2020. https://doi.org/10.1073/pnas.1912789117
- [papamakarios2016] Papamakarios et al., *Fast $ε$-free Inference of Simulation Models with Bayesian Conditional Density Estimation*, NeurIPS 2016. https://arxiv.org/abs/1605.06376
- [talts2018] Talts et al., *Validating Bayesian Inference Algorithms with Simulation-Based Calibration*, arXiv preprint 2018. https://arxiv.org/abs/1804.06788
