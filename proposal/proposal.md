# Inferring Synaptic Competition Dynamics from Static Connectomic Snapshots: A Simulation-Based Inference Framework

**Aarush Kandukoori** (Carnegie Mellon University) — Lead Student Author  
**Aditya Kandukoori** (Poolesville High School) — Co-Author

> **Status: early-stage research proposal.** No experimental results
> are claimed. We are actively seeking expert feedback.

## Abstract

Connectomic electron-microscopy volumes give highly detailed but static views of neural wiring, whereas developmental synaptic competition, such as the elimination of multiple axonal inputs onto single targets, unfolds over time. We outline an early-stage framework that treats cross-sectional connectomic snapshots at different ages as samples from an underlying stochastic competition process. A simple replicator-style model of input-share dynamics at each target cell is paired with simulation-based Bayesian inference to recover the competition parameters that are identifiable from snapshot statistics. We describe the model, work out which parameter combinations are and are not identifiable, and plan an evaluation on clearly-labeled synthetic data only. No experiments have been run, and we are seeking expert feedback on whether the formulation matches how connectomics researchers think about synapse elimination. AI tools (Claude) were used for literature synthesis, ideation, and draft preparation, and the authors reviewed and take responsibility for all content.

## Introduction & Motivation

During early postnatal development, many target cells (for example muscle fibers) are initially innervated by several axons, and most of these inputs are later eliminated until one remains. This process is called synaptic competition. Time-lapse in vivo imaging can watch it directly, but only in accessible preparations and for limited durations. Serial-section EM connectomics instead gives complete wiring diagrams, but each animal contributes only one frozen moment.

This proposal is **early-stage** and asks one narrow question: *given connectomic snapshots from animals at several ages, which parameters of a competition process can be recovered, and with what uncertainty?* We do not claim to answer it. We want feedback on whether the question is well posed, whether the model is too simple to be useful, and what data a connectomics group would actually have available.

Contributions we aim for, to our knowledge as a small and modest step: (1) a minimal, mathematically checkable competition model; (2) an explicit identifiability analysis; (3) a plan for amortized simulation-based inference with calibration checks, all on synthetic data.

## Related Work

**Connectomic reconstruction.** Saturated EM reconstruction of neural tissue [kasthuri2015] and automated segmentation methods such as flood-filling networks [januszewski2018] and 3D convolutional approaches [lee2017] produce the axon-to-target wiring and synapse-size data that our framework would take as input. We treat segmentation errors as out of scope initially, and list them under limitations.

**Activity-dependent plasticity theory.** Competition-style rules in synaptic plasticity have a long history, for example the BCM theory [bienenstock1982]. Our replicator-style model is far simpler and is intended as a statistical scaffold rather than a biophysical claim.

**Learning on graphs.** Wiring data is naturally a bipartite graph (axons and targets). Inductive graph neural networks such as GraphSAGE [hamilton2017] provide a baseline summary network.

**Simulation-based inference.** When a likelihood is intractable but a simulator exists, neural conditional density estimation [papamakarios2016] and the broader SBI toolkit [cranmer2020] allow posterior estimation, and simulation-based calibration [talts2018] provides a check that posteriors are self-consistent.

## Proposed Framework

**Setup.** Consider one target cell $j$ with a set of competing axonal inputs $i \in \{1,\dots,n\}$ and positive input strengths $w_i(t)$ (for instance, summed synaptic area). Let $W=\sum_i w_i$ and the share $p_i = w_i / W$.

**Replicator-style competition.** Suppose each input has an effective advantage $a_i$ (a latent scalar summarizing, e.g., how well its activity is correlated with the target's other inputs; we do not assume a mechanism). Let
$$\frac{dw_i}{dt} = \eta\, w_i\,(a_i - \bar a),\qquad \bar a = \sum_k p_k a_k .$$
Checks: (i) $\frac{dW}{dt} = \eta \sum_i w_i (a_i-\bar a) = \eta W(\bar a - \bar a)=0$, so total strength is conserved. (ii) Shares then obey the replicator equation $\dot p_i = \eta\, p_i (a_i-\bar a)$.

**Closed form.** For constant $a_i$, $p_i(t) = p_i(0)e^{\eta a_i t} / \sum_k p_k(0)e^{\eta a_k t}$. Hence for any pair, $\log\frac{p_i(t)}{p_k(t)} = \log\frac{p_i(0)}{p_k(0)} + \eta (a_i-a_k)\,t$.

**Elimination.** An input is deemed eliminated once $p_k < \theta$. For two inputs with $x(t)=\log(p_1/p_2)$, $p_2 = 1/(1+e^{x})$, so $p_2<\theta \iff x > \log\frac{1-\theta}{\theta}$. With $\Delta=a_1-a_2>0$ and $x(0)=x_0$, the elimination time is
$$t^* = \frac{\log\frac{1-\theta}{\theta} - x_0}{\eta\,\Delta}.$$

**Identifiability.** The dynamics have two symmetries. (1) *Scaling:* $(\eta, a)\to(c\eta, a/c)$ for any $c>0$ leaves every product $\eta a_i$, and hence every $p_i(t)$, unchanged. (2) *Shift:* $a_i \to a_i + c$ for all $i$ at a target leaves $p_i(t)$ unchanged, because $\bar a$ moves by the same constant $c$ and $a_i-\bar a$ is unchanged (equivalently, the common factor $e^{\eta c t}$ cancels in the closed form). Therefore, from snapshots, at most the scaled within-target differences $\eta(a_i-a_k)$ are identifiable; $\eta$ is not separately identifiable without time-lapse data or an independent time scale, and the overall level of the advantages is not identifiable at all.

We therefore parameterize directly in terms of identifiable quantities. For each target, define the relative advantages $\beta_i = \eta\,(a_i - \bar a_{\text{target}})$, where $\bar a_{\text{target}} = \frac1n\sum_{k=1}^n a_k$ is the unweighted mean advantage over the inputs of that target, so that $\sum_i \beta_i = 0$ within each target and $p_i(t)\propto p_i(0)\,e^{\beta_i t}$. In the simulator we draw $b_i \sim \mathcal N(0,\sigma_\beta^2)$ independently and set $\beta_i = b_i - \frac1n\sum_k b_k$, which places the population prior on within-target differences only. The observation time $t_{\text{age}}$ is known from animal age. The parameters of interest are $\phi=(\sigma_\beta,\theta,\sigma_0)$: $\sigma_\beta$ is the spread of relative advantages, $\theta$ the elimination threshold, and $\sigma_0$ the spread of initial log-shares, where $\log p_i(0)$ is drawn as $\mathcal N(0,\sigma_0^2)$ before normalizing to sum to one. A population mean of the advantages is not part of $\phi$ because it is not identifiable from snapshots.

**Observation model.** At age $t$, a snapshot yields for each target $j$ the number of surviving inputs and their size shares, with measurement noise from segmentation (multiplicative log-normal noise on $w_i$, and a small probability of missed or falsely merged inputs). The summary of a snapshot is the empirical distribution of innervation numbers and of the largest-to-second-largest log ratio per target, by age.

**Inference.** Because the likelihood marginalizes over latent $\beta_i$ and thresholded elimination, we use simulation-based inference: draw $\phi$ from a prior, simulate snapshot data at the observed ages, and train a conditional density estimator $q_\psi(\phi \mid s)$ on summaries $s$ [papamakarios2016, cranmer2020]. The summary network is either hand-built statistics or a graph network over the axon-target bipartite graph [hamilton2017].

## Methodology

**Simulator.** Implement the closed-form share dynamics above for many targets in parallel, with per-target random initial shares, random number of initial inputs (e.g., 2 to 6), and elimination at threshold $\theta$. Add a segmentation-noise layer.

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

Baselines (moment matching, ABC) are the simple reference points. Any claim of improvement would be made only after these experiments are actually run.

## Limitations & Open Questions

- **Model simplicity.** Constant per-input advantages and total-strength conservation are strong assumptions. Real competition likely depends on activity patterns, position, and molecular factors.
- **Cross-sectional inference.** Different animals at different ages are not a trajectory; between-animal variability is confounded with dynamics.
- **Identifiability.** Only scaled within-target differences of advantages are identifiable from snapshots, as shown above. Absolute rates need other data, and the mean (overall level) of the advantages is not recoverable at all because of the shift symmetry.
- **Segmentation error.** Input counts and sizes depend on reconstruction quality, which we model only crudely.
- **Generality.** The model is framed around many-to-one convergence; other connectivity-development settings may need different formulations.
- **Open questions for experts.** What snapshot summaries are routinely available? Which ages would be sampled? Is the elimination threshold a sensible abstraction? Would this be useful alongside existing analyses of ordered activity and network formation?

## References

- [kasthuri2015] Kasthuri et al., *Saturated Reconstruction of a Volume of Neocortex*, Cell 2015. https://doi.org/10.1016/j.cell.2015.06.054
- [januszewski2018] Januszewski et al., *High-precision automated reconstruction of neurons with flood-filling networks*, Nature Methods 2018. https://doi.org/10.1038/s41592-018-0049-4
- [lee2017] Lee et al., *Superhuman Accuracy on the SNEMI3D Connectomics Challenge*, arXiv preprint 2017. https://arxiv.org/abs/1706.00120
- [hamilton2017] Hamilton et al., *Inductive Representation Learning on Large Graphs*, NeurIPS 2017. https://arxiv.org/abs/1706.02216
- [bienenstock1982] Bienenstock et al., *Theory for the development of neuron selectivity: orientation specificity and binocular interaction in visual cortex*, Journal of Neuroscience 1982. https://doi.org/10.1523/JNEUROSCI.02-01-00032.1982
- [cranmer2020] Cranmer et al., *The frontier of simulation-based inference*, Proceedings of the National Academy of Sciences 2020. https://arxiv.org/abs/1911.01429
- [papamakarios2016] Papamakarios et al., *Fast $ε$-free Inference of Simulation Models with Bayesian Conditional Density Estimation*, NeurIPS 2016. https://arxiv.org/abs/1605.06376
- [talts2018] Talts et al., *Validating Bayesian Inference Algorithms with Simulation-Based Calibration*, arXiv preprint 2018. https://arxiv.org/abs/1804.06788
