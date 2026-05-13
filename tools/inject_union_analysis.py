#!/usr/bin/env python3
"""Inject a 'Union Analysis' section into the teacher-CBA brief.

The section sits between 'Where the unions stand' (existing) and the next
section, weaving financial-incentive analysis and post-Janus membership
trends through the brief's existing analytical threads.

Idempotent: looks for the sentinel 'id="sec-union-analysis"' before injecting.
"""
import sys

PATH = '/Users/danielgolliher/projects/teacher-cba-student-outcomes/index.html'

SECTION = """<h2 id="sec-union-analysis">Union analysis: the money behind the positions<span class="added-badge">Added</span></h2>

<p>The policy positions described in the previous section &mdash; NEA's blanket opposition to outcome-tied compensation; AFT's more permissive but still litigation-leading posture &mdash; do not exist in a vacuum. They are downstream of a specific financial architecture that has been under sustained pressure since 2018. Understanding the financial machinery and the membership trends makes the policy positions easier to read.</p>

<h3>The financial machinery</h3>

<p>The two national teachers' unions are large, dues-funded organizations. Their headline financials for the most recent reporting periods<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup>:</p>

<div class="stat-grid">
  <div class="stat">
    <span class="num">$381M</span>
    <span class="lbl">NEA dues revenue (FY 2024)<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup></span>
  </div>
  <div class="stat">
    <span class="num">$399M</span>
    <span class="lbl">NEA total annual budget (FY 2023)<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup></span>
  </div>
  <div class="stat">
    <span class="num">$428M</span>
    <span class="lbl">NEA endowment (most recent disclosure)<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup></span>
  </div>
  <div class="stat">
    <span class="num">$202M</span>
    <span class="lbl">AFT national dues revenue from locals (FY 2025, per LM-2)<sup class="factref"><a class="fact" href="#fact-47" data-fact="47">47</a></sup></span>
  </div>
</div>

<p class="cite">Sources: NEA Strategic Framework &amp; Budget; AFT LM-2 filings with U.S. Department of Labor; The 74 / Mike Antonucci analyses.</p>

<p>Per-member, the national portion of NEA dues for an active classroom teacher is <strong>$208 per year</strong> for the 2023&ndash;24 school year &mdash; <em>before</em> state and local affiliate dues, which typically multiply the total to roughly <strong>$700&ndash;$1,000 annually</strong> depending on the affiliate<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup>. These dues are most commonly collected via payroll deduction (&ldquo;dues check-off&rdquo;), which is itself a CBA-negotiated provision. The mechanism matters: payroll deduction makes the dues invisible to most members month-to-month, which historically suppressed turnover.</p>

<h3>The Janus rupture</h3>

<p>On June 27, 2018, the U.S. Supreme Court decided <strong><em>Janus v. AFSCME Council 31</em></strong>, 5&ndash;4, holding that public-sector unions could no longer collect &ldquo;agency fees&rdquo; from non-member employees they bargained on behalf of. Before <em>Janus</em>, in 22 states a teacher who declined to join the union still had to pay a reduced fee covering the union's bargaining costs. After <em>Janus</em>, those fees became unconstitutional &mdash; effectively making the entire United States a &ldquo;right-to-work&rdquo; jurisdiction for public employees<sup class="factref"><a class="fact" href="#fact-48" data-fact="48">48</a></sup>.</p>

<p>The financial consequences have been substantial but not catastrophic. Across 66 public-sector unions in 22 non-RTW states, membership fell from <strong>3,360,000 pre-Janus to 2,980,000 by 2022</strong> &mdash; a 11.3% loss. The combined NEA + AFT + AFSCME total fell from <strong>5,292,481 in 2018 to 4,743,397 by the most recent reporting</strong> &mdash; a 10.4% decline, or roughly 549,000 lost members. Aggregate annual union revenue is down an estimated <strong>$733 million</strong>, based on roughly 1.2 million public-sector workers who have resigned or declined membership since the ruling<sup class="factref"><a class="fact" href="#fact-48" data-fact="48">48</a></sup>.</p>

<p>The state-level numbers are more dramatic in places that paired <em>Janus</em> with prior or simultaneous state-law changes:</p>

<table class="timeline">
  <tr><td class="date">Michigan</td><td>Lost approximately <strong>215,000 members since 2018</strong> (the MEA-and-MFT decline). Michigan also passed right-to-work in 2012 (repealed 2023), so the post-2018 drop compounds an earlier exit<sup class="factref"><a class="fact" href="#fact-49" data-fact="49">49</a></sup>.</td></tr>
  <tr><td class="date">Wisconsin</td><td>Even larger percentage decline than Michigan. Membership compounded by Act 10 (2011), which had already gutted collective bargaining for most public unions outside public safety<sup class="factref"><a class="fact" href="#fact-36" data-fact="36">36</a></sup>.</td></tr>
  <tr><td class="date">Oregon</td><td>OEA density fell from <strong>85.6% to 81.2%</strong> in three years; 40,634 dues-payers in 2021&ndash;22<sup class="factref"><a class="fact" href="#fact-49" data-fact="49">49</a></sup>.</td></tr>
  <tr><td class="date">Minnesota</td><td>Education Minnesota went from <strong>95,389 to 86,676</strong> dues-payers in six years &mdash; a 9% decline<sup class="factref"><a class="fact" href="#fact-49" data-fact="49">49</a></sup>.</td></tr>
  <tr><td class="date">Indiana / Michigan / Wisconsin combined</td><td>Among states that dropped agency fees pre-Janus, membership has shrunk <strong>17%&ndash;59%</strong> since 2010<sup class="factref"><a class="fact" href="#fact-48" data-fact="48">48</a></sup>.</td></tr>
</table>

<p>The pattern: <em>Janus</em> by itself produces gradual attrition. <em>Janus</em> + a state-law change that eliminates dues check-off, scope of bargaining, or contract scope produces a cliff.</p>

<h3>How the unions are responding financially</h3>

<p>Three observable responses to the dues-revenue squeeze:</p>

<ol>
  <li><strong>Higher per-member dues.</strong> Despite membership falling, NEA's total dues revenue keeps rising &mdash; from a 2023&ndash;24 collection of $379 million to FY24's $381 million<sup class="factref"><a class="fact" href="#fact-46" data-fact="46">46</a></sup>. The math requires that the per-member rate has been raised to outpace the membership decline. The 74 has tracked this in repeat coverage: &ldquo;NEA membership continued to drop in 2024 as revenue from dues hit $381 million.&rdquo;</li>
  <li><strong>Member-retention investment.</strong> Bloomberg Law reported in 2020 that public-sector unions had &ldquo;fend[ed] off membership exodus in 2 years since Janus ruling&rdquo; &mdash; partly through aggressive recommitment campaigns and partly through legal challenges to opt-out procedures. NEA and AFT both spent significantly on internal organizing and member-services upgrades during 2018&ndash;2022<sup class="factref"><a class="fact" href="#fact-48" data-fact="48">48</a></sup>.</li>
  <li><strong>Continued political-spending ramp.</strong> The NEA Advocacy Fund raised <strong>$27.9 million for the 2023&ndash;24 election cycle</strong>, including $2.5 million to Future Forward USA Action (pro-Harris super PAC) and $1.5 million each to the House Majority PAC and the Senate Majority PAC<sup class="factref"><a class="fact" href="#fact-50" data-fact="50">50</a></sup>. The political ramp has not slowed proportionally to membership.</li>
</ol>

<h3>Why this matters for the CBA-and-outcomes question</h3>

<p>The financial-incentive lens reframes several of the positions documented earlier in this brief:</p>

<h4>NEA's blanket opposition to outcome-tied compensation</h4>

<p>Outcome-tied pay creates within-member inequality: some teachers earn more than others under the same contract. That inequality is solvent for the employer but corrosive for collective member identification with the union &mdash; the &ldquo;we're all in this together&rdquo; framing that supports voluntary dues payment under <em>Janus</em>. An NEA local that bargains a merit-pay system is harder to organize than one that bargains a flat salary schedule. The financial incentive runs strongly against differentiated pay regardless of how the empirical research on its effectiveness turns out<sup class="factref"><a class="fact" href="#fact-24" data-fact="24">24</a></sup>.</p>

<h4>AFT's more permissive posture</h4>

<p>AFT has a larger share of urban / mixed-profession membership and a smaller share of suburban classroom-only locals than NEA does. Its dues revenue base is more diverse and its members are more accustomed to differentiated pay structures (NYC HRA workers, hospital staff, etc., are AFT-affiliated). That permits AFT to take a slightly more open position on outcome-tied compensation without immediately threatening its dues base &mdash; though it remains the lead plaintiff in <em>HFT v. HISD</em>, the case that effectively ended VAM-based termination<sup class="factref"><a class="fact" href="#fact-25" data-fact="25">25</a></sup>.</p>

<h4>LIFO defense</h4>

<p>Layoff-by-seniority is the single most defended contract provision in U.S. teacher CBAs &mdash; even where its disparate impact on high-poverty schools is well-documented<sup class="factref"><a class="fact" href="#fact-16" data-fact="16">16</a></sup>. The financial logic: senior members are the union's reliable dues-payers (longer track record, less likely to exit). LIFO protects them by definition. A performance-based layoff system would, in expectation, lay off a mix of newer and older teachers &mdash; reducing the &ldquo;rational dues-payer&rdquo; pool faster than LIFO does. The same Goldhaber finding that &ldquo;LIFO is not very good for kids&rdquo; is, from the union's revenue-maximization perspective, very good for the dues base.</p>

<h4>The ATR and the &ldquo;paid not to work&rdquo; problem</h4>

<p>The NYC Absent Teacher Reserve costs roughly <strong>$136 million per year</strong>. ATR members continue paying UFT dues during their time in the pool. From the union's perspective, a member in the ATR is financially equivalent to a member in a classroom; only the union dues column matters for revenue. The disposition of the ATR is therefore not, from the union's standpoint, a problem to be solved &mdash; it is a stable equilibrium to be defended<sup class="factref"><a class="fact" href="#fact-14" data-fact="14">14</a></sup>.</p>

<h4>The pension dimension</h4>

<p>The financial incentive also runs the other way: <strong>median U.S. teacher pension systems are only ~70% funded</strong>, and the national public-employee-pension shortfall stands at roughly <strong>$3 trillion</strong><sup class="factref"><a class="fact" href="#fact-51" data-fact="51">51</a></sup>. Active members contribute the cash flow that keeps these systems running. A shrinking active membership directly threatens the actuarial assumptions of the pension funds &mdash; which is why unions oppose policy changes (vouchers, charter expansion, alternative certification) that would reduce district-employed-teacher headcount regardless of those changes' effect on student outcomes. AFT has reportedly used pension-board influence to apply pressure on fund managers it disfavors<sup class="factref"><a class="fact" href="#fact-51" data-fact="51">51</a></sup>, which extends the financial-incentive analysis into a less-visible but equally consequential domain.</p>

<h3>What the union-decline trend implies for the next five years</h3>

<p>Three plausible trajectories:</p>

<ol>
  <li><strong>Continued slow attrition.</strong> 2018&ndash;2024 trend continues: ~1&ndash;2% membership loss per year in non-RTW states, larger in RTW or state-restricted states. National dues revenue stays flat or grows slightly via per-member-rate increases. Political spending unchanged. <em>This is the modal scenario absent a major shock.</em></li>
  <li><strong>Acceleration via state-law changes.</strong> Tennessee enacted teacher-union restrictions in 2024 (the &ldquo;Tampa Bay&rdquo; pattern in Florida); other RTW Republican states could follow with bargaining-scope limits modeled on Wisconsin Act 10. Each new restrictive state adds a step-function loss to NEA / AFT revenue. <em>Conditional on continued Republican gains in state legislatures.</em></li>
  <li><strong>Stabilization via a labor-coded shift.</strong> The unions reposition toward labor-political issues that resonate with younger workforce-entry teachers &mdash; AI-and-worker-displacement (see the New York chatbot bill, sponsored by AFT-aligned senators<sup class="factref"><a class="fact" href="#fact-15" data-fact="15">15</a></sup>); class-size limits; safety provisions. This is the trajectory implied by Hinchey's Workforce Stabilization Act and the broader 2026 AI package. <em>Plausible if the 2026 election cycle reshapes the political map.</em></li>
</ol>

<p>The bottom line: the policy positions documented in this brief are stable not because the empirical evidence supports them but because the financial machinery rewards them. The financial machinery has been weakened since 2018 but not broken. Until either membership declines steepen meaningfully or the dues check-off mechanism is undone in non-RTW states, the contract provisions that the empirical research most criticizes &mdash; LIFO, tenure-by-default, forced placement, ATR-style salary-without-placement &mdash; will remain the unions' default bargaining demands. The contract is not in the textbooks; it is on the dues spreadsheet.</p>

"""

NEW_FACTS = '''  "46": {s:"NEA dues / budget / membership — The 74 coverage and NEA Strategic Framework", u:"https://www.the74million.org/article/nea-membership-continued-to-drop-in-2024-as-revenue-from-dues-hit-381-million/", n:"FY24: 2.83M members, $381M dues revenue, $399M budget, $428M endowment, $208/year active-teacher national-portion dues."},
  "47": {s:"AFT LM-2 filings (US DOL)", u:"https://www.aft.org/about/financial", n:"$202M dues revenue from locals to AFT national in FY 2025 per LM-2 filing."},
  "48": {s:"Janus v. AFSCME Council 31 financial-impact synthesis", u:"https://www.empirecenter.org/publications/the-janus-effect/", n:"5-4 SCOTUS ruling 6/27/2018. 11.3% membership decline across 66 public-sector unions in 22 non-RTW states (2018-2022). $733M annual revenue loss. NEA+AFT+AFSCME combined: 5.29M → 4.74M (-10.4%, ~549K)."},
  "49": {s:"State-by-state teacher union decline data", u:"https://www.americanexperiment.org/teacher-union-exodus-reaches-nearly-double-digit-percentage-since-2018/", n:"Minnesota: 95K → 86K (-9% in 6 yrs). Oregon: 85.6% → 81.2% density. Michigan: -215K since 2018. Mackinac Center tracking."},
  "50": {s:"NEA Advocacy Fund political spending — OpenSecrets / The 74", u:"https://www.the74million.org/article/national-education-association-pac-raised-roughly-27-million-for-2024-election/", n:"$27.9M raised for 2023-24 cycle. $2.5M to Future Forward USA Action; $1.5M each to House Majority PAC and Senate Majority PAC. NEA + AFT combined ~$669M to leftwing political entities since August 2015 per Defending Education investigation."},
  "51": {s:"Teacher-pension underfunding analysis", u:"https://manhattan.institute/article/the-politics-of-public-pension-boards", n:"Median teacher pension only 70% funded (2019); $3T national shortfall for government-employee pensions. Brookings + Manhattan Institute analyses. AFT has used pension-board influence to pressure fund managers per Heritage Foundation reporting."}'''

NEW_CITATIONS = '''    <li id="fact-46"><span class="src-name">NEA financial overview — The 74 (Mike Antonucci) + NEA Strategic Framework</span>. <a href="https://www.the74million.org/article/nea-membership-continued-to-drop-in-2024-as-revenue-from-dues-hit-381-million/" target="_blank" rel="noopener">the74million.org</a>; <a href="https://www.nea.org/about-nea/governance-policies/nea-strategic-framework" target="_blank" rel="noopener">nea.org</a>; <a href="https://projects.propublica.org/nonprofits/organizations/530115260" target="_blank" rel="noopener">ProPublica Nonprofit Explorer</a>. <span class="src-note">FY24: 2.83M members, $381M dues revenue, $399M budget, $428M endowment, $208/year active-teacher national-portion dues.</span></li>
    <li id="fact-47"><span class="src-name">AFT LM-2 filings (US Department of Labor)</span>. <a href="https://www.aft.org/about/financial" target="_blank" rel="noopener">aft.org/about/financial</a>; alternate compilation at <a href="https://americansforfairtreatment.org/resources-and-data/aft-where-do-your-union-dues-go/" target="_blank" rel="noopener">Americans for Fair Treatment</a>. <span class="src-note">$202M dues revenue from locals to AFT national in FY 2025 per LM-2 filing; $283M total revenue in FY 2022-23.</span></li>
    <li id="fact-48"><span class="src-name">Empire Center for Public Policy — "The Janus Effect"</span>. <a href="https://www.empirecenter.org/publications/the-janus-effect/" target="_blank" rel="noopener">empirecenter.org</a>; complementary analysis at <a href="https://manhattan.institute/article/the-legal-aftermath-of-janus-v-afscme" target="_blank" rel="noopener">Manhattan Institute</a> and <a href="https://www.mackinac.org/S2023-05" target="_blank" rel="noopener">Mackinac Center</a>. <span class="src-note">5-4 SCOTUS ruling 6/27/2018. 11.3% membership decline across 66 public-sector unions in 22 non-RTW states (2018-2022). $733M annual revenue loss. NEA+AFT+AFSCME combined: 5.29M → 4.74M (-10.4%).</span></li>
    <li id="fact-49"><span class="src-name">State-by-state teacher-union decline data</span>. American Experiment <a href="https://www.americanexperiment.org/teacher-union-exodus-reaches-nearly-double-digit-percentage-since-2018/" target="_blank" rel="noopener">aggregate analysis</a>; <a href="https://www.mackinac.org/blog/2024/membership-plunges-again-for-michigan-and-national-teachers-unions" target="_blank" rel="noopener">Mackinac Center on Michigan</a>; <a href="https://www.freedomfoundation.com/oregon/oregon-teachers-union-has-lost-20-percent-of-its-membership-2/" target="_blank" rel="noopener">Freedom Foundation on Oregon</a>. <span class="src-note">Minnesota -9% in 6 yrs; Oregon density 85.6% → 81.2%; Michigan -215K since 2018; IN/MI/WI combined 17-59% decline since 2010.</span></li>
    <li id="fact-50"><span class="src-name">NEA / AFT political spending</span>. <a href="https://www.the74million.org/article/national-education-association-pac-raised-roughly-27-million-for-2024-election/" target="_blank" rel="noopener">The 74 — NEA Advocacy Fund 2024 totals</a>; <a href="https://www.opensecrets.org/orgs/national-education-assn/totals?id=d000000064" target="_blank" rel="noopener">OpenSecrets NEA profile</a>; <a href="https://defendinged.org/investigations/teachers-unions-spending/" target="_blank" rel="noopener">Defending Education — "DivertED" investigation</a>. <span class="src-note">$27.9M NEA Advocacy Fund 2023-24 cycle; $2.5M to Future Forward USA Action, $1.5M each to House Majority PAC and Senate Majority PAC; ~$669M combined NEA+AFT to leftwing entities since Aug 2015 per Defending Education.</span></li>
    <li id="fact-51"><span class="src-name">Teacher-pension underfunding and union political influence</span>. <a href="https://manhattan.institute/article/the-politics-of-public-pension-boards" target="_blank" rel="noopener">Manhattan Institute — "The Politics of Public Pension Boards"</a>; <a href="https://www.brookings.edu/articles/teachers-states-and-public-pension-reform/" target="_blank" rel="noopener">Brookings — "Teachers, states, and public pension reform"</a>; <a href="https://www.heritage.org/jobs-and-labor/commentary/government-union-misusing-teachers-pensions" target="_blank" rel="noopener">Heritage Foundation</a>; <a href="https://www.nctq.org/wp-content/uploads/2025/03/NCTQ_NoOneBenefits_FINAL.pdf" target="_blank" rel="noopener">NCTQ — "How teacher pension systems are failing both teachers and taxpayers"</a>. <span class="src-note">Median teacher pension 70% funded (2019); $3T national public-employee-pension shortfall. AFT has used pension-board influence to pressure fund managers.</span></li>'''


def inject(path):
    with open(path) as f: html = f.read()

    if 'id="sec-union-analysis"' in html:
        print('  · Union analysis already present, skipping')
        return

    # 1. TOC entry — insert right after "Where the unions stand"
    toc_old = '<li><a href="#sec-unions">Where the unions stand</a></li>'
    toc_new = '<li><a href="#sec-unions">Where the unions stand</a></li>\n    <li class="toc-new"><a href="#sec-union-analysis">Union analysis</a></li>'
    assert toc_old in html, 'sec-unions TOC entry not found'
    html = html.replace(toc_old, toc_new, 1)
    print('  + TOC entry inserted')

    # 2. Section — insert between sec-unions section close and sec-partisan
    insert_marker = '<h2 id="sec-partisan">'
    assert insert_marker in html, 'sec-partisan header not found'
    html = html.replace(insert_marker, SECTION + '\n' + insert_marker, 1)
    print('  + Section body inserted')

    # 3. FACTS dict — add fact-46..51 right before the closing brace
    facts_old_end = '"45": {s:"AERA Statement on Value-Added Models (Nov 11, 2015) — full text",'
    if facts_old_end in html:
        # Find the closing brace of fact 45's entry, then insert new entries after
        idx = html.find(facts_old_end)
        # find the line end and the closing of this entry
        line_end = html.find('}\n};', idx)
        if line_end == -1:
            line_end = html.find('}\n}', idx)
        # Insert new entries between fact-45 and the closing
        end_of_45 = html.find('}', idx)
        # Walk to find the right closing brace
        # Actually simpler: find the line `};` after FACTS and insert before it
        # Use the closing-brace landmark of the FACTS object instead of trying to match the full fact-45 line
        facts_close = '\n};'
        # Find the FACTS = { ... }; block and insert before its closing
        facts_start = html.find('const FACTS = {')
        if facts_start != -1:
            facts_end = html.find('\n};', facts_start)
            if facts_end != -1:
                html = html[:facts_end] + ',\n' + NEW_FACTS + html[facts_end:]
                print('  + FACTS dict updated (46-51)')
            else:
                print('  ! FACTS closing brace not found')
        else:
            print('  ! FACTS dict not found')
    else:
        print('  ! fact-45 marker not found in JS')

    # 4. Citations <ol> — add fact-46..51 at the end
    cit_old = '<li id="fact-45"><span class="src-name">AERA &mdash; full Statement on the Use of Value-Added Models (Nov 11, 2015)</span>.'
    # Find the closing </li> of fact-45 and insert new <li>s after it
    if cit_old in html:
        # Find end of </li> for fact-45
        start = html.find(cit_old)
        li_end = html.find('</li>', start) + len('</li>')
        html = html[:li_end] + '\n' + NEW_CITATIONS + html[li_end:]
        print('  + Citations updated (46-51)')
    else:
        print('  ! fact-45 citation li not found')

    with open(path, 'w') as f: f.write(html)


if __name__ == '__main__':
    inject(PATH)
    print(f'OK: {PATH}')
