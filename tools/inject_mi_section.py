#!/usr/bin/env python3
"""Insert a 'Prior Manhattan Institute work' section into each example brief.

Idempotent: looks for the sentinel '<h2 id="sec-mi"' before injecting.
Each brief gets its own brief-specific content; the section structure is identical.
"""

LL64_SECTION = """<h2 id="sec-mi">Prior Manhattan Institute work<span class="added-badge">Added</span></h2>

<p>The Manhattan Institute &mdash; through its main publishing arm, its in-house magazine <em>City Journal</em>, and the newer NYC-focused <em>Bigger Apple</em> Substack &mdash; has produced a substantial body of work on the housing-voucher and shelter-cost questions that sit underneath LL 64. The Institute's posture is generally skeptical of voucher expansion as a homelessness solution, but supportive of the operational reforms (like LL 64's EFT mandate) that make existing programs work better. The most directly relevant pieces:</p>

<h3>The cost case against unbounded voucher expansion</h3>
<ul>
  <li><strong>&ldquo;Housing Isn't Cheaper Than Shelter&rdquo;</strong> &mdash; <em>The Bigger Apple</em>. Argues that the <strong>$25M (FY19) &rarr; $1.3B (FY25) &rarr; possibly $3B (FY28)</strong> trajectory for CityFHEPS spending shows the program is no longer a substitute for shelter costs but an addition to them. The piece is the most-cited source for the cost-trajectory numbers used by program critics. <a class="more" href="https://thebiggerapple.manhattan.institute/p/housing-isnt-cheaper-than-shelter" target="_blank" rel="noopener">thebiggerapple.manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Don't Universalize Housing Vouchers&rdquo;</strong> &mdash; <em>City Journal</em>. Argues against the policy logic of expanding voucher eligibility to anyone below an income threshold; favors targeted use of vouchers for shelter exits and eviction prevention rather than universal entitlement. <a class="more" href="https://city-journal.org/dont-universalize-housing-vouchers" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;Vouching for Self-Sufficiency&rdquo;</strong> &mdash; <em>City Journal</em>. The Institute's longer-form case for prioritizing voucher use among formerly homeless populations &mdash; with attention to how source-of-income-discrimination enforcement and operational reforms (the LL 64 question) interact. <a class="more" href="https://www.city-journal.org/article/vouching-for-self-sufficiency" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<h3>The shelter system and homelessness operations</h3>
<ul>
  <li><strong>&ldquo;Benchmarking Homeless Shelter Performance: A Proposal for Easing America's Homeless Crisis&rdquo;</strong> &mdash; Manhattan Institute report. Proposes a federal benchmarking framework for shelter providers; the operational diagnostic complements LL 64's payment-rail focus. <a class="more" href="https://manhattan.institute/article/benchmarking-homeless-shelter-performance-a-proposal-for-easing-americas-homeless-crisis" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;The Future of Housing for the Homeless&rdquo;</strong> &mdash; Manhattan Institute. Argues for a shift toward permanent-supportive-housing and away from emergency shelter for the chronically homeless population. <a class="more" href="https://manhattan.institute/article/the-future-of-housing-for-the-homeless" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;New York's Homelessness Crucible&rdquo;</strong> &mdash; <em>City Journal</em>. A retrospective on how mayoral administrations from Dinkins through Adams have used rental subsidies as the primary shelter-exit lever &mdash; with cost framing similar to the Win testimony quoted in this brief. <a class="more" href="https://www.city-journal.org/article/new-yorks-homelessness-crucible" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;Social Democracy in New York: A Cautionary Tale&rdquo;</strong> &mdash; <em>City Journal</em>. Situates CityFHEPS and the broader rental-assistance expansion in the larger NYC social-welfare-spending picture. <a class="more" href="https://www.city-journal.org/article/new-york-city-social-democracy-welfare-programs-scandinavia" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<h3>NYCHA and the structural housing question</h3>
<ul>
  <li><strong>&ldquo;Ending NYCHA's Dependence Trap: Making Better Use of New York's Public Housing&rdquo;</strong> &mdash; Manhattan Institute. Argues that maximizing the use of existing NYCHA stock should precede further voucher expansion; the policy alternative the Institute generally prefers. <a class="more" href="https://manhattan.institute/article/ending-nychas-dependence-trap-making-better-use-of-new-yorks-public-housing" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;The New Housing Problem Facing Low-Income Renters&rdquo;</strong> &mdash; Manhattan Institute. Looks at the gap between subsidy availability and unit availability &mdash; a problem that LL 64 doesn't directly address but that constrains how much LL 64's operational improvements can move the needle. <a class="more" href="https://manhattan.institute/article/the-new-housing-problem-facing-low-income-renters" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Why Are 50,000 New York City Apartments Vacant?&rdquo;</strong> &mdash; <em>City Journal</em>. The supply-side complement: vouchers without units to rent are useless. <a class="more" href="https://www.city-journal.org/article/vacant-new-york-city-apartments-rent-control-housing" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<p>The throughline across these pieces: skepticism of voucher expansion as a primary homelessness strategy, paired with support for operational reforms that make existing programs work better. LL 64's narrow scope &mdash; converting paper checks to EFT rather than changing eligibility &mdash; sits squarely inside the Institute's preferred reform zone.</p>

"""

TEACHER_SECTION = """<h2 id="sec-mi">Prior Manhattan Institute work<span class="added-badge">Added</span></h2>

<p>The Manhattan Institute has been one of the most consistent voices on teacher-contract reform for two decades. Its publishing has run across the Institute's main reports, <em>City Journal</em>, and (more recently) <em>The Bigger Apple</em>. The Institute's general posture: skeptical of seniority-based personnel rules (LIFO, tenure-by-default), favorable to performance-based compensation, and consistently critical of contract provisions that protect underperforming teachers in ways that fall hardest on disadvantaged students.</p>

<h3>Tenure, layoffs, and LIFO</h3>
<ul>
  <li><strong>&ldquo;Tackling NY Teacher Tenure&rdquo;</strong> &mdash; Manhattan Institute. Direct argument for raising the tenure bar in New York, with explicit attention to the &ldquo;due process so burdensome and with so little probability of success that most schools don't even attempt to remove the worst&rdquo; problem this brief covers in the dismissal-procedures sub-section. <a class="more" href="https://manhattan.institute/article/tackling-ny-teacher-tenure" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;One Small Strike Against Teacher Seniority&rdquo;</strong> &mdash; <em>City Journal</em>. Coverage of the Los Angeles court ruling against seniority-only layoff policies; argues the precedent could constrain LIFO contracts elsewhere. <a class="more" href="https://www.city-journal.org/article/one-small-strike-against-teacher-seniority" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;Life After Tenure&rdquo;</strong> &mdash; <em>City Journal</em>. Analysis of <em>Vergara v. California</em>, the Los Angeles Superior Court decision that voided California's teacher tenure, seniority, and dismissal statutes (later reversed on appeal). The Institute reads the case as the constitutional-challenge model for LIFO-and-tenure reform. <a class="more" href="https://www.city-journal.org/article/life-after-tenure" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;There's One Thing Worse Than Paying Bad Teachers Not to Work&rdquo;</strong> &mdash; Manhattan Institute. The Institute's most-cited piece on NYC's <strong>Absent Teacher Reserve</strong> &mdash; the same $136M-per-year artifact this brief covers in the teacher-protections section. <a class="more" href="https://manhattan.institute/article/theres-one-thing-worse-than-paying-bad-teachers-not-to-work" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
</ul>

<h3>Performance pay and outcome-tied compensation</h3>
<ul>
  <li><strong>&ldquo;The NYC Teacher Pay-for-Performance Program: Early Evidence from a Randomized Trial&rdquo;</strong> &mdash; Manhattan Institute report. Empirical evaluation of the NYC SPBP (School-wide Performance Bonus Program); finds limited first-year effects on proficiency or school environment. Methodologically the closest analogue in the MI corpus to the Goldhaber LIFO work cited elsewhere in this brief. <a class="more" href="https://manhattan.institute/article/the-nyc-teacher-pay-for-performance-program-early-evidence-from-a-randomized-trial" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Good Teachers Matter, So Pay the Best More&rdquo;</strong> &mdash; Manhattan Institute. The Institute's affirmative case for differentiated compensation tied to student-outcome measures &mdash; the same theoretical position Eric Hanushek (footnoted in this brief) developed empirically. <a class="more" href="https://manhattan.institute/article/good-teachers-matter-so-pay-the-best-more" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Merit Pay: A Tool for Teaching&rdquo;</strong> &mdash; Manhattan Institute. Survey of merit-pay-program designs (Cincinnati, TAP, others). <a class="more" href="https://manhattan.institute/article/merit-pay-a-tool-for-teaching" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Merit Pay Will Improve N.Y.'s Schools&rdquo;</strong> &mdash; Manhattan Institute (op-ed). The shorter affirmative case for NY-specific adoption. <a class="more" href="https://manhattan.institute/article/merit-pay-will-improve-n-y-s-schools" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
</ul>

<h3>Teacher quality, credentials, and measurement</h3>
<ul>
  <li><strong>&ldquo;Measuring Teacher Effectiveness: Credentials Unrelated to Student Achievement&rdquo;</strong> &mdash; Manhattan Institute. Finding: external teacher credentials predict next to nothing about classroom performance &mdash; the foundational claim that motivates outcome-tied evaluation in MI's framing. <a class="more" href="https://manhattan.institute/article/measuring-teacher-effectiveness-credentials-unrelated-to-student-achievement" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Rewarding Experienced Teachers: How Much Do Schools Really Pay?&rdquo;</strong> &mdash; Manhattan Institute. Quantifies the experience-based pay premium in conventional salary schedules. <a class="more" href="https://manhattan.institute/article/rewarding-experienced-teachers-how-much-do-schools-really-pay" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Better Pay, Fairer Pensions: Reforming Teacher Compensation&rdquo;</strong> &mdash; Manhattan Institute. Pairs salary-schedule critique with pension-design critique. <a class="more" href="https://manhattan.institute/article/better-pay-fairer-pensions-reforming-teacher-compensation" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;The Teacher-Pay Myth&rdquo;</strong> &mdash; Manhattan Institute. The standing rebuttal to the &ldquo;teachers are underpaid&rdquo; framing that dominates union messaging. <a class="more" href="https://manhattan.institute/article/the-teacher-pay-myth" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
</ul>

<h3>Union power and political economy</h3>
<ul>
  <li><strong>&ldquo;The Union That Devoured Education Reform&rdquo;</strong> &mdash; <em>City Journal</em>. The Institute's most-cited historical piece on the UFT's contract pattern and how Bloomberg-era reforms (mutual consent in hiring, end of seniority transfers) were rolled back. <a class="more" href="https://www.city-journal.org/article/the-union-that-devoured-education-reform" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;How Teachers' Unions Handcuff Schools&rdquo;</strong> &mdash; <em>City Journal</em>. Maps the contract provisions (uniform pay, seniority, work-day limits) back to the 1961 UFT contract that established them. <a class="more" href="https://www.city-journal.org/article/how-teachers-unions-handcuff-schools" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;The Fight over Flunked-Out Teachers&rdquo;</strong> &mdash; <em>City Journal</em>. The reporting that established the ATR-as-political-artifact narrative this brief uses. <a class="more" href="https://www.city-journal.org/article/the-fight-over-flunked-out-teachers" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;Students vs. Status Quo&rdquo;</strong> &mdash; <em>City Journal</em>. Source for the &ldquo;high-poverty schools lose 30% more teachers in seniority-based layoffs&rdquo; empirical claim that aligns with Goldhaber's LIFO research cited in this brief. <a class="more" href="https://www.city-journal.org/html/students-vs-status-quo-11033.html" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;New York's Teachers' Unions Are So Progressive, They're Even Alienating Teachers&rdquo;</strong> &mdash; <em>City Journal</em>. Recent piece on intra-union political tension. <a class="more" href="https://www.city-journal.org/article/new-york-teachers-unions-activism-collective-bargaining" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<p>The throughline: MI's argument is that contract provisions that are facially about teacher protection &mdash; LIFO, tenure-by-default, ATR-style paid-but-unplaced pools &mdash; have disparate impact on the students least able to absorb the cost. The empirical case in this brief (Goldhaber, Kraft, NCTQ) and the Institute's longer-running case point at the same conclusion through different methodologies.</p>

"""

CHATBOT_SECTION = """<h2 id="sec-mi">Prior Manhattan Institute work<span class="added-badge">Added</span></h2>

<p>The Manhattan Institute's AI-policy work has been published primarily on its main site and in <em>City Journal</em>, with broader anti-licensing-restriction work spanning two decades. The Institute's general posture on AI regulation is innovation-friendly and federalist-skeptical of state patchworks &mdash; which puts it on the critical side of S.7263 / A.6545, though without published commentary on this specific bill (yet). The most directly relevant pieces:</p>

<h3>The case against state-by-state AI regulation</h3>
<ul>
  <li><strong>&ldquo;Blue State AI Regulations Could Threaten U.S. Competitiveness&rdquo;</strong> &mdash; <em>City Journal</em> (July 25, 2025). The Institute's headline statement of position: &ldquo;more than 1,000 AI-related state and local laws are now pending nationwide, risking a patchwork of costly and confusing regulations.&rdquo; Notes that one 2024 survey of state proposals identified 57 different definitions of &ldquo;artificial intelligence&rdquo; or &ldquo;automated decision system&rdquo; &mdash; directly relevant to S.7263's broad &ldquo;chatbot&rdquo; / &ldquo;substantive response&rdquo; definitional ambiguity flagged by Holland &amp; Knight in this brief. <a class="more" href="https://www.city-journal.org/article/artificial-intelligence-regulations-blue-states" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;The White House's AI Strategy Is Too Little, Too Late&rdquo;</strong> &mdash; <em>City Journal</em> (March 24, 2026). Argues for federal preemption of state AI rules &mdash; the same federalist concern that figures in this brief's "factors that swing the outcome" subsection. <a class="more" href="https://www.city-journal.org/article/ai-risks-data-centers-legislation" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;On AI, More Understanding, Less Regulation&rdquo;</strong> &mdash; <em>City Journal</em> (August 1, 2024). The general MI line: that regulatory rush gets ahead of technical understanding. <a class="more" href="https://www.city-journal.org/article/on-ai-more-understanding-less-regulation" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
  <li><strong>&ldquo;A Conflict of AI Visions&rdquo;</strong> &mdash; <em>City Journal</em>. Frames the federalist-vs-state-regulation debate as a contest between two distinct theories of how AI's risks materialize. <a class="more" href="https://www.city-journal.org/article/artificial-intelligence-safety-legislation-data-centers" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<h3>AI-policy primers</h3>
<ul>
  <li><strong>&ldquo;A Playbook for AI Policy&rdquo;</strong> &mdash; Manhattan Institute report by fellow Nick Whitaker. Primer on AI development history and four principles for guiding AI policy: methods for evaluating AI capability, controlling AI systems, the role of AI agents, and global competition. The Institute's most systematic statement of position. <a class="more" href="https://manhattan.institute/article/a-playbook-for-ai-policy-2" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;Balancing AI Innovation with National Security&rdquo;</strong> &mdash; Manhattan Institute. Frames AI regulation as a national-security question and argues against rules that constrain U.S. firms while leaving foreign competitors unconstrained. <a class="more" href="https://manhattan.institute/article/balancing-ai-innovation-with-national-security" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;New Report Finds Bias in ChatGPT&rdquo;</strong> &mdash; Manhattan Institute. Empirical work on political/demographic bias in chatbot outputs &mdash; relevant to the consumer-protection framing that motivates S.7263 but pointed in a different direction. <a class="more" href="https://manhattan.institute/article/new-report-finds-bias-in-chatgpt" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;AI Can Help Struggling Students&rdquo;</strong> &mdash; <em>City Journal</em>. The educational-equity case for AI access &mdash; directly relevant to the &ldquo;AI advice vs. no advice at all&rdquo; argument in this brief's critique section. <a class="more" href="https://www.city-journal.org/article/artificial-intelligence-education-students-equity" target="_blank" rel="noopener">city-journal.org &rarr;</a></li>
</ul>

<h3>The longer line on occupational licensing</h3>

<p>The bill's structural form &mdash; importing professional-licensure law into a new statutory cause of action &mdash; runs into a critique the Institute has been making for two decades:</p>

<ul>
  <li><strong>&ldquo;Occupational Licensing Reduces Interstate Mobility&rdquo;</strong> &mdash; Manhattan Institute. Foundational finding: people in state-specific licensed occupations have an interstate migration rate 36% lower than other workers. The MI version of the public-choice critique that Tabarrok applies to S.7263 in this brief's critique section. <a class="more" href="https://manhattan.institute/article/occupational-licensing-reduces-interstate-mobility" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
  <li><strong>&ldquo;How Occupational Licensing Harms the Young&rdquo;</strong> &mdash; Manhattan Institute. Distributional analysis: the costs of licensing fall hardest on young, low-income, and minority workers. <a class="more" href="https://manhattan.institute/article/how-occupational-licensing-harms-the-young-2" target="_blank" rel="noopener">manhattan.institute &rarr;</a></li>
</ul>

<h3>The new live precedent: <em>Pennsylvania v. Character.AI</em></h3>

<p>This precedent post-dates the Manhattan Institute's published commentary on S.7263 but is directly load-bearing for the bill's legal architecture. On <strong>May 1, 2026</strong>, the <strong>Pennsylvania Department of State sued Character Technologies, Inc.</strong> in Commonwealth Court &mdash; alleging that a Character.AI chatbot named &ldquo;Emilie&rdquo; held itself out as a licensed psychiatrist with a fabricated Pennsylvania license number, in violation of state medical-practice statutes. The case underscores that <strong>regulators are already willing to apply existing medical-practice law to AI &mdash; without any AI-specific statute</strong>, which is exactly the question S.7263 is structured to settle. Sources covering the suit: <a href="https://www.npr.org/2026/05/05/nx-s1-5812861/characterai-chatbot-medical-advice-pennsylvania-lawsuit" target="_blank" rel="noopener">NPR</a>; <a href="https://www.washingtontimes.com/news/2026/may/5/pennsylvania-suing-ai-company-saying-chatbots-illegally-hold-licensed/" target="_blank" rel="noopener">Washington Times</a>; <a href="https://www.cbsnews.com/news/pennsylvania-character-ai-lawsuit-chatbot-posed-as-medical-professional/" target="_blank" rel="noopener">CBS News</a>; <a href="https://thehill.com/policy/healthcare/5864427-pennsylvania-lawsuit-ai-chatbots-doctors-therapists/" target="_blank" rel="noopener">The Hill</a>. Lexology has paired analyses: <a href="https://www.lexology.com/library/detail.aspx?g=14422250-16b9-4c0b-8d55-666d8b350a06" target="_blank" rel="noopener">&ldquo;No AI Law, No Problem&rdquo;</a> and <a href="https://www.lexology.com/library/detail.aspx?g=fd86e605-efc1-4dd1-afbd-23a58dd4e9a2" target="_blank" rel="noopener">&ldquo;Pennsylvania Targets AI Chatbot for the Unauthorized Practice of Medicine&rdquo;</a>.</p>

<p>The Pennsylvania action complicates S.7263's positioning. The case demonstrates that existing professional-practice statutes can reach chatbot impersonation without new legislation; the question S.7263 / A.6545 actually decides is whether to add a <em>private right of action</em> on top of (or in place of) the existing AG-enforcement track that Pennsylvania is using.</p>

<p>The Manhattan Institute has not yet published commentary on either S.7263 or the Pennsylvania action. Given the Institute's positioning on AI regulation (federalist-skeptical, innovation-favoring, licensing-skeptical) and on occupational licensing (broadly critical), one would expect any forthcoming commentary to land in the Tabarrok / Cato Institute / Abundance Institute camp documented in this brief's critique section &mdash; though the Pennsylvania case has shifted the question from &ldquo;should AI face liability?&rdquo; to &ldquo;through which procedural channel?&rdquo;.</p>

"""


import sys

SECTIONS = {
    'electronic-rent-payments': LL64_SECTION,
    'teacher-cba-student-outcomes': TEACHER_SECTION,
    'ny-chatbot-liability': CHATBOT_SECTION,
}

TOC_BEFORE = {
    'electronic-rent-payments': '<li><a href="#footnotes">People mentioned</a></li>',
    'teacher-cba-student-outcomes': '<li><a href="#footnotes">People mentioned</a></li>',
    'ny-chatbot-liability': '<li><a href="#footnotes">People mentioned</a></li>',
}

# Where to insert the section in body — right before the People-mentioned footnotes section
BODY_INSERTION_MARKER = '<section class="footnotes" id="footnotes">'


def inject(slug, path):
    with open(path) as f: html = f.read()
    if 'id="sec-mi"' in html:
        print(f'  · MI section already present in {path}, skipping')
        return

    # 1. TOC entry — insert a new TOC li right before the People-mentioned entry
    toc_marker = TOC_BEFORE[slug]
    new_toc_entry = '<li class="toc-new"><a href="#sec-mi">Prior MI work</a></li>\n    ' + toc_marker
    if toc_marker in html:
        html = html.replace(toc_marker, new_toc_entry, 1)
        print('  + TOC entry inserted')
    else:
        print(f'  ! TOC marker not found: {toc_marker[:50]}')

    # 2. Body section — insert before the footnotes section
    section_content = SECTIONS[slug]
    if BODY_INSERTION_MARKER in html:
        html = html.replace(BODY_INSERTION_MARKER, section_content + '\n' + BODY_INSERTION_MARKER, 1)
        print('  + Section body inserted')
    else:
        print(f'  ! Body marker not found')

    with open(path, 'w') as f: f.write(html)
    print(f'OK: {path}')


if __name__ == '__main__':
    targets = [
        ('electronic-rent-payments', '/Users/danielgolliher/projects/electronic-rent-payments/index.html'),
        ('teacher-cba-student-outcomes', '/Users/danielgolliher/projects/teacher-cba-student-outcomes/index.html'),
        ('ny-chatbot-liability', '/Users/danielgolliher/projects/ny-chatbot-liability/index.html'),
    ]
    for slug, path in targets:
        print(f'\nProcessing {slug}: {path}')
        inject(slug, path)
