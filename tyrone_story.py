TYRONE_STORY = {
    "attorney": "Tyrone",
    "client": "Kendall",
    "rival": "Dave",
    "title": "TYRONE'S ROUTE: CHECKMATE IN COURT",
    "subtitle": "Defending Kendall • Rivalry vs. Dave",
    "evidence_db": {
        "AUTH_TOKEN": {
            "name": "Elijah's Hardware Key Log",
            "desc": "Cryptographic audit log showing Elijah's physical YubiKey authenticated the Q3 public earnings release at 8:15 PM."
        },
        "VALUATION_DECK": {
            "name": "Inflated Growth Pitch Deck",
            "desc": "Series D presentation authored on Elijah's workstation promising 300% user growth—using unverified free-trial signups."
        },
        "CFO_CHAT": {
            "name": "Encrypted Signal Messages",
            "desc": "Recovered messages between the CFO and an offshore broker arranging a $2.4M transfer without Kendall's authorization."
        },
        "AUDIT_SIGN": {
            "name": "CEO Certification Form (SOX-404)",
            "desc": "Federal compliance form signed in ink by Elijah certifying that all internal financial controls were verified and accurate."
        },
        "BOARD_MINUTES": {
            "name": "Emergency Board Minutes",
            "desc": "Official minutes showing Kendall formally moved for an independent external audit two weeks ago—which Elijah vetoed."
        },
        "EXPENSE_CARD": {
            "name": "Executive Corporate Card Log",
            "desc": "Shows $340,000 in unapproved luxury travel and private jet charters billed to R&D under the CFO's discretionary code."
        },
        "REFORM_CHARTER": {
            "name": "Governance Reform Charter",
            "desc": "Draft compliance restructuring plan requiring both founding partners to surrender unilateral financial control to an independent board."
        }
    },
    "prologue": [
        ("Tyrone", "(In a courtroom, sentiment is dead weight. Leverage, timing, and airtight documentation decide who walks out intact.)", "think"),
        ("Kendall", "Tyrone, Dave's PR machine is already painting me as the ruthless co-founder who threw his college roommate to the wolves!", "think"),
        ("Kendall", "We built EK Global from two folding tables and a loaned server! If institutional investors think I'm crooked, our Series D round evaporates tomorrow!", "think"),
        ("Tyrone", "Let Dave play for sympathy in the press, Kendall. He litigates with his heart exposed—which makes every move he makes predictable.", "smile"),
        ("Dave", "Don't engrave your trophy yet, Tyrone! No amount of legal sleight-of-hand can erase what happened to EK Global!", "point"),
        ("Tyrone", "It isn't sleight-of-hand, Dave. It's simply calculating five moves deeper than your opponent before the first witness takes the oath.", "smile")
    ],
    "chapters": [
        {
            "title": "CASE 1: THE CEO'S SIGNATURE",
            "bg": "courtroom",
            "ethics_topic": "Executive Accountability & Sarbanes-Oxley Compliance",
            "brief_summary": (
                "EK Global's public Q3 earnings report has been exposed as inaccurate, threatening the company's upcoming Series D round. "
                "While CEO Elijah insists he was away at a charity gala when the release went live, defense strategist Tyrone prepares to "
                "examine the cryptographic and statutory trail bearing the CEO's credentials."
            ),
            "acknowledgement": (
                "A clinical opening checkmate by Tyrone! By dismantling Elijah's physical alibi through cryptographic authentication logs and "
                "federal certification records, the defense established clear statutory responsibility on the record. Today's proceedings upheld "
                "the core standard of Executive Accountability and Sarbanes-Oxley Compliance—demonstrating that corporate officers bear legal duty for the disclosures they certify."
            ),
            "evidence": ["AUTH_TOKEN", "AUDIT_SIGN", "BOARD_MINUTES"],
            "intro": [
                ("Dwyane", "Court is in session. Mr. Tyrone, open your examination regarding the fraudulent Q3 earnings release.", "idle"),
                ("Dave", "Your Honor, Elijah was blindsided by the accounting discrepancies! A product-focused CEO relies on his finance department to verify the books!", "point"),
                ("Tyrone", "Delegation does not erase a statutory signature, Dave. Under federal compliance law, the CEO owns every figure he certifies.", "smile"),
                ("Elijah", "I'm telling the truth! Someone pushed that Q3 earnings report live while I was speaking at a charity gala! I never approved it!", "think"),
                ("Dave", "My client has two hundred gala attendees confirming he was nowhere near a computer at 8:15 PM!", "point"),
                ("Tyrone", "(Nowhere near a computer... yet the release server authenticated a physical hardware token hanging from his own keychain. Time to close the trap.)", "think")
            ],
            "cross_exam": {
                "witness": "Elijah",
                "default_pose": "idle",
                "statements": [
                    {
                        "text": "Someone in finance published the Q3 earnings report while I was at the gala—without my personal authentication!",
                        "witness_pose": "point",
                        "press": [
                            ("Tyrone", "Hold it! Are you testifying under oath that your physical security key was stolen that evening, Elijah?", "point"),
                            ("Elijah", "No, it stayed in my tuxedo pocket the entire night! Which proves I couldn't have been sitting at my office terminal!", "think"),
                            ("Dave", "Even you can't bend geography, Tyrone! He was three miles away!", "point")
                        ],
                        "contradiction": "AUTH_TOKEN",
                        "win_dialogue": [
                            ("Tyrone", "You don't need to sit at a desk to tap an NFC-enabled YubiKey! Your personal hardware token authenticated that Q3 release at 8:15 PM sharp!", "point"),
                            ("Elijah", "Gah—!! W-Wait... I only tapped my key against my phone because the CFO texted me saying it was an urgent security certificate renewal!", "think"),
                            ("Tyrone", "And in doing so, you authorized the public release of unverified Q3 earnings to institutional investors without reading a single line!", "point"),
                            ("Dave", "Tch...! You baited him into confirming the token never left his pocket, then dropped the cryptographic log on his head!", "think"),
                            ("Tyrone", "Precision is everything in cross-examination, Dave. A CEO who blindly taps his master key cannot plead ignorance afterward.", "smile"),
                            ("Dwyane", "Order! The witness's claim of an unauthorized release is conclusively refuted by his own hardware key! Continue, Mr. Tyrone!", "stare")
                        ]
                    },
                    {
                        "text": "As CEO, my focus is product engineering—I never signed any personal guarantees regarding internal accounting controls.",
                        "witness_pose": "think",
                        "press": [
                            ("Tyrone", "Hold it! Never signed ANY compliance guarantees? Think carefully before perjuring yourself over a federal filing.", "point"),
                            ("Elijah", "General counsel sends over stacks of routine paperwork every quarter—I don't memorize every rider!", "think")
                        ],
                        "contradiction": "AUDIT_SIGN",
                        "win_dialogue": [
                            ("Tyrone", "Look at Exhibit B: a federal SOX-404 CEO Certification bearing your ink signature! By law, you personally attested that internal controls were verified!", "point"),
                            ("Elijah", "I... I signed it because I trusted my finance team! I didn't know the ledger was cooked!", "think"),
                            ("Tyrone", "Trust is not a statutory defense under Sarbanes-Oxley, Elijah. You certified the accuracy of those controls to every shareholder in the market.", "point"),
                            ("Dave", "Objection! Signing a compliance form in good faith does not prove criminal conspiracy, Tyrone!", "point"),
                            ("Tyrone", "Not criminal conspiracy, Dave—just textbook executive negligence. And that distinction changes everything.", "smile"),
                            ("Dwyane", "The SOX-404 Certification is admitted into the record! The witness's testimony stands corrected!", "stare")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 2: THE ILLUSION OF GROWTH",
            "bg": "courtroom",
            "ethics_topic": "Investor Transparency & Misleading Projections",
            "brief_summary": (
                "Dave accuses Kendall of deliberately blocking independent external auditors to protect the Series D fundraising valuation. "
                "As EK Global's Senior Accountant takes the stand to recount how the audit was postponed and how growth metrics were compiled, "
                "Tyrone looks to the official board record to clarify who truly opposed transparency."
            ),
            "acknowledgement": (
                "A decisive reversal of the narrative! By producing the official Emergency Board Minutes and growth pitch documentation, Tyrone "
                "proved that Kendall championed an independent external audit while inflated user projections originated in the CEO's growth team. "
                "Today's proceedings reinforced the principle of Investor Transparency and Misleading Projections—affirming that accurate governance records are essential to corporate truth."
            ),
            "evidence": ["VALUATION_DECK", "BOARD_MINUTES", "AUDIT_SIGN"],
            "intro": [
                ("Dave", "Even if Elijah signed the compliance forms, Kendall fought tooth and nail to keep outside auditors away from the books!", "point"),
                ("Dave", "He wanted the numbers kept dark until the Series D wire cleared!", "point"),
                ("Tyrone", "An interesting hypothesis, Dave. Let's ask EK Global's Senior Accountant who actually killed the external audit.", "smile"),
                ("Accountant", "Um... Mr. Elijah instructed us to postpone hiring an outside audit firm until after the Series D round closed.", "worried"),
                ("Dave", "Only because Kendall warned him an outside audit would spook our lead venture investors!", "point"),
                ("Tyrone", "(Let's check the official boardroom minutes and see who actually demanded transparency—and who exercised the veto.)", "think")
            ],
            "cross_exam": {
                "witness": "Accountant",
                "default_pose": "worried",
                "statements": [
                    {
                        "text": "Both founding partners agreed unanimously in the boardroom to delay the external audit until next quarter.",
                        "witness_pose": "worried",
                        "press": [
                            ("Tyrone", "Hold it! Check your memory against the official board minutes. Was that vote genuinely unanimous?", "point"),
                            ("Accountant", "I... I was seated at the back table taking notes, Counselor. Nobody raised their voice, so I assumed both founders agreed.", "worried"),
                            ("Dave", "Exactly! Both founders wanted a smooth closing!", "point")
                        ],
                        "contradiction": "BOARD_MINUTES",
                        "win_dialogue": [
                            ("Tyrone", "Incorrect! The Emergency Board Minutes prove Kendall formally MOVED for an immediate external audit—and Elijah used his CEO veto to kill it!", "point"),
                            ("Accountant", "Oh! R-Right—yes! Looking at the roll call, Mr. Kendall's motion was overruled by the CEO's tie-breaking vote!", "shocked"),
                            ("Dave", "What?! Elijah, you vetoed an external audit two weeks before the scandal broke?!", "think"),
                            ("Elijah", "We were forty-eight hours from closing $150 million! Bringing in outside auditors would have frozen the wire!", "think"),
                            ("Tyrone", "So the man Dave accused of hiding the books was actually the ONLY founder fighting to open them to independent investigators!", "point"),
                            ("Accountant", "I'm relieved the official minutes cleared up what actually happened in that boardroom...", "relief"),
                            ("Kendall", "Thank you, Tyrone. At least the official record finally shows who fought for institutional accountability.", "smile"),
                            ("Dwyane", "Order! The Emergency Board Minutes are entered into evidence! That puts an end to the claim that Mr. Kendall blocked the audit!", "stare")
                        ]
                    },
                    {
                        "text": "The investor pitch deck metrics were grounded strictly in verified paying enterprise accounts.",
                        "witness_pose": "idle",
                        "press": [
                            ("Tyrone", "Hold it! Verified paying accounts—or unverified free-trial signups dressed up as recurring revenue?", "point"),
                            ("Accountant", "Well... the definition of 'active enterprise user' was supplied directly by the CEO's growth team.", "worried")
                        ],
                        "contradiction": "VALUATION_DECK",
                        "win_dialogue": [
                            ("Tyrone", "This Series D pitch deck inflates user growth by 300% using unverified beta signups—authored directly on Elijah's workstation!", "point"),
                            ("Accountant", "Eek! That's the exact raw export the growth team handed me before the investor roadshow!", "shocked"),
                            ("Tyrone", "Vanity metrics packaged as enterprise revenue—and not a single slide came from Kendall's office!", "point"),
                            ("Dave", "Aggressive startup projections aren't embezzlement, Tyrone! Tell this court where the missing $2.4 million went!", "point"),
                            ("Dwyane", "The Inflated Growth Pitch Deck is admitted! Proceed with your examination, Mr. Tyrone!", "stare")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 3: THE PAPER TRAIL",
            "bg": "courtroom",
            "ethics_topic": "Corporate Expense Abuse & Internal Controls",
            "brief_summary": (
                "With governance responsibility clarified, Tyrone turns the spotlight onto EK Global's missing $2.4 million. "
                "The Chief Financial Officer takes the stand claiming strict fiscal austerity across his department, "
                "prompting Tyrone to scrutinize corporate expense statements for signs of unauthorized self-dealing."
            ),
            "acknowledgement": (
                "A surgical takedown of financial misconduct! By exposing $340,000 in unauthorized private aviation and luxury travel buried inside "
                "R&D expense ledgers, Tyrone shattered the CFO's facade of fiscal austerity. Today's proceedings upheld the principle of Corporate "
                "Expense Abuse and Internal Controls—proving that discretionary override codes cannot conceal personal enrichment."
            ),
            "evidence": ["EXPENSE_CARD", "BOARD_MINUTES", "VALUATION_DECK"],
            "intro": [
                ("Dave", "You've spent two sessions nitpicking Elijah's management style, Tyrone—yet you still haven't accounted for the missing $2.4 million!", "point"),
                ("Tyrone", "Patience, Dave. A competent tactician clears the pawns before trapping the king.", "smile"),
                ("Tyrone", "Now that we've established Elijah's lax oversight, let's examine who exploited that blind spot to loot the company treasury.", "smile"),
                ("CFO", "I've already explained myself! I only disbursed R&D funds that the CEO verbally greenlit!", "angry"),
                ("Tyrone", "(Verbally greenlit? Let's compare his frugal story against the corporate card statements.)", "think")
            ],
            "cross_exam": {
                "witness": "CFO",
                "default_pose": "laugh",
                "statements": [
                    {
                        "text": "Every single dollar drawn from the R&D reserve went strictly toward cloud servers and engineering contracts!",
                        "witness_pose": "laugh",
                        "press": [
                            ("Tyrone", "Hold it! Not a single personal luxury or private charter was ever charged to the R&D reserve?", "point"),
                            ("CFO", "I run an austere finance department, Counselor! Every corporate card is reconciled down to the penny!", "laugh")
                        ],
                        "contradiction": "EXPENSE_CARD",
                        "win_dialogue": [
                            ("Tyrone", "Reconciled down to the penny?! Then explain $340,000 in private jet charters and five-star resorts billed to R&D under YOUR discretionary card code!", "point"),
                            ("CFO", "Gah—!! Th-Those were high-level investor hospitality retreats!", "worried"),
                            ("Tyrone", "Investor retreats in Monaco during an engineering sprint—with zero investors on the flight manifest and your own override code approving every invoice?!", "point"),
                            ("Dave", "What?! The CFO was burning R&D money on private jets while our engineers worked overtime?!", "point"),
                            ("CFO", "I—I intended to reimburse the discretionary account once the Series D closing bonuses cleared!", "worried"),
                            ("Dwyane", "Order! Charging private aviation to an engineering reserve is blatant self-dealing! The Executive Corporate Card Log is admitted!", "stare")
                        ],
                        "unlocks": {
                            "text": "Even my discretionary executive card had zero charges exceeding five thousand dollars this quarter!",
                            "witness_pose": "angry",
                            "press": [
                                ("Tyrone", "Hold it! Zero charges over five thousand dollars? Let's present the Executive Corporate Card Log and test that claim!", "point"),
                                ("CFO", "Go right ahead! You won't find a single improper swipe!", "angry")
                            ],
                            "contradiction": "EXPENSE_CARD",
                            "win_dialogue": [
                                ("Tyrone", "Reconciled down to the penny?! Then explain $340,000 in private jet charters and five-star resorts billed to R&D under YOUR discretionary card code!", "point"),
                                ("CFO", "Gah—!! Th-Those were high-level investor hospitality retreats!", "worried"),
                                ("Tyrone", "Investor retreats in Monaco during an engineering sprint—with zero investors on the flight manifest and your own override code approving every invoice?!", "point"),
                                ("Dave", "What?! The CFO was burning R&D money on private jets while our engineers worked overtime?!", "point"),
                                ("CFO", "I—I intended to reimburse the discretionary account once the Series D closing bonuses cleared!", "worried"),
                                ("Dwyane", "Order! Charging private aviation to an engineering reserve is blatant self-dealing! The Executive Corporate Card Log is admitted!", "stare")
                            ]
                        }
                    },
                    {
                        "text": "Kendall reviewed and countersigned every monthly expense ledger before it was archived.",
                        "witness_pose": "idle",
                        "press": [
                            ("Tyrone", "Hold it! Funny how none of those statements bear Kendall's digital signature—only yours!", "point"),
                            ("CFO", "He delegated routine sign-off authority to save time!", "angry")
                        ],
                        "contradiction": "EXPENSE_CARD",
                        "win_dialogue": [
                            ("Tyrone", "The Executive Corporate Card Log proves every single one of those $340,000 luxury charges was self-approved under YOUR override code alone!", "point"),
                            ("CFO", "Gah—!! Th-Those were urgent client entertainment expenses!", "worried"),
                            ("Tyrone", "Not a single countersignature from Kendall, not a single audit receipt—just your personal override draining the R&D budget!", "point"),
                            ("Dave", "So the CFO was using the company reserve as his personal travel fund!", "point"),
                            ("Dwyane", "The witness's credibility is severely compromised! Proceed, Mr. Tyrone!", "sigh")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 4: THE WHISTLEBLOWER SPIN",
            "bg": "courtroom",
            "ethics_topic": "Administrative Due Diligence & Governance",
            "brief_summary": (
                "Dave challenges Kendall's dismissal of an internal HR compliance ticket filed by a junior accounting clerk who was later terminated. "
                "As the former clerk testifies about being shut out of the building, Tyrone examines the sequence of boardroom actions to determine "
                "whether Kendall suppressed the investigation or sought outside oversight."
            ),
            "acknowledgement": (
                "A masterful clarification of corporate governance! By aligning the clerk's timeline with the Emergency Board Minutes, Tyrone "
                "demonstrated that Kendall sought an independent external audit immediately after questioning the CFO's assurances. Today's proceedings "
                "upheld the principle of Administrative Due Diligence and Governance—showing that verifying facts matters more than assumptions."
            ),
            "evidence": ["BOARD_MINUTES", "EXPENSE_CARD", "CFO_CHAT"],
            "intro": [
                ("Dave", "Even if the CFO abused his corporate card, Kendall STILL dismissed an internal HR complaint warning about fake vendor invoices!", "point"),
                ("Dave", "Answer that, Tyrone! Why did your client bury a whistleblower report?!", "point"),
                ("Kendall", "I didn't bury anything! The CFO assured me that ticket was a glitched duplicate from a clerk who was already scheduled for severance!", "think"),
                ("Employee", "I wasn't glitched! I flagged phantom shell vendors—and two days later, HR deactivated my badge and walked me out!", "worried"),
                ("Tyrone", "(Dave is trying to tie Kendall to that retaliatory firing. Time to show the court who actually demanded an independent investigation.)", "think")
            ],
            "cross_exam": {
                "witness": "Employee",
                "default_pose": "worried",
                "statements": [
                    {
                        "text": "After my HR ticket was closed, management refused to allow anyone outside the executive team to inspect the books.",
                        "witness_pose": "worried",
                        "press": [
                            ("Tyrone", "Hold it! Are you certain BOTH co-founders opposed bringing in outside investigators?", "point"),
                            ("Employee", "All I know is my ticket was marked dismissed and no outside auditors ever arrived before I was escorted out!", "worried"),
                            ("Dave", "Because Kendall slammed the door on any outside review!", "point")
                        ],
                        "contradiction": "BOARD_MINUTES",
                        "win_dialogue": [
                            ("Tyrone", "Incorrect! Forty-eight hours after closing that ticket, Kendall formally moved for an independent external audit—and Elijah vetoed it!", "point"),
                            ("Employee", "W-Wait... Mr. Kendall actually tried to bring in outside auditors after I was let go?!", "shocked"),
                            ("Tyrone", "He trusted the CFO's 'glitched ticket' excuse at first, realized the numbers still didn't reconcile, and moved to open the entire company to outside investigators!", "smile"),
                            ("Employee", "I had no idea Mr. Kendall pushed for an external audit... I thought everyone at the top was trying to silence me!", "relief"),
                            ("Dave", "Tch...! You turned my own witness's timeline into a shield for Kendall!", "think"),
                            ("Dwyane", "Order! The record reflects that Mr. Kendall formally petitioned for an independent audit! Continue, Mr. Tyrone!", "stare")
                        ]
                    },
                    {
                        "text": "The Friday consulting bonuses I discovered were pushed through using an emergency finance override.",
                        "witness_pose": "idle",
                        "press": [
                            ("Tyrone", "An override key held exclusively by the CFO—not by my client.", "smile"),
                            ("Employee", "Yes... the override ID belonged to the finance office.", "smile")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 5: THE REAL ARCHITECT",
            "bg": "courtroom",
            "ethics_topic": "Corporate Reform vs. Strategic Scapegoating",
            "brief_summary": (
                "The EK Global trial reaches its decisive final session as the court demands conclusive proof of who orchestrated the $2.4 million "
                "offshore embezzlement. Armed with recovered encrypted communications and board governance records, Tyrone prepares to expose the "
                "true architect of the fraud and define the future of EK Global."
            ),
            "acknowledgement": (
                "Checkmate in open court! In the decisive closing session of the EK Global trial, Tyrone unmasked the true architect of the $2.4 million "
                "offshore embezzlement and brought the financial conspiracy to an end. Today's proceedings illuminated the enduring tension between "
                "Corporate Reform and Strategic Scapegoating—proving that lasting enterprise strength requires structural accountability."
            ),
            "evidence": ["CFO_CHAT", "BOARD_MINUTES", "REFORM_CHARTER"],
            "intro": [
                ("Dwyane", "We reach the climax of this trial. Counsel, the court demands conclusive proof of who orchestrated the $2.4 million offshore theft.", "stare"),
                ("Dave", "Whether Kendall wanted an audit later or not, both founders let EK Global's governance rot while chasing a unicorn valuation!", "point"),
                ("Tyrone", "And today we expose the true architect of that theft—the man who looted EK Global while pitting two friends against each other!", "point"),
                ("Kendall", "(Tyrone... listen closely. Pin 100% of this scandal on the CFO. If I walk out spotless, I take sole control of EK Global.)", "think"),
                ("Tyrone", "(The decrypted Signal logs prove the CFO masterminded the $2.4M theft... yet the broader record also shows both Kendall and Elijah cut ethical corners to inflate their valuation.)", "think"),
                ("Tyrone", "(Do I deliver a ruthless, unconditional acquittal for Kendall—or demand binding governance reform for BOTH co-founders?)", "think")
            ],
            "cross_exam": {
                "witness": "CFO",
                "default_pose": "laugh",
                "statements": [
                    {
                        "text": "I never touched a single cent of EK Global's R&D reserves—every offshore wire was ordered by the founders!",
                        "witness_pose": "angry",
                        "press": [
                            ("Tyrone", "Hold it! You expect this bench to believe you had zero contact with the Cayman Islands broker?", "point"),
                            ("CFO", "I don't even use encrypted messaging apps, Counselor! You're bluffing without a shred of proof!", "laugh"),
                            ("Dave", "If you have proof of an offshore broker, Tyrone, put it on the bench right now!", "point")
                        ],
                        "contradiction": "CFO_CHAT",
                        "ending_trigger": "FULL_TRUTH",
                        "win_dialogue": [
                            ("Tyrone", "Bluffing? Read these decrypted Signal messages pulled from YOUR private burner phone arranging the $2.4 million Cayman kickback!", "point"),
                            ("CFO", "N-NO!! Th-Those messages had a sixty-second auto-delete timer! How could you recover encrypted burner logs?!", "worried"),
                            ("Tyrone", "Cloud key-escrow backups don't vanish just because a timer expires on your screen! You negotiated the shell routing, took a 35% cut, and framed both founders!", "point"),
                            ("Dave", "So it really WAS the CFO who drained the R&D reserve and pitted Elijah and Kendall against each other!", "point"),
                            ("CFO", "I... I thought nobody would ever trace a numbered Cayman depository...", "worried"),
                            ("Tyrone", "Checkmate. The embezzlement begins and ends with your signature on those offshore transfers!", "smile"),
                            ("Dwyane", "Order in the gallery! The Encrypted Signal Messages are entered into the permanent record! Bailiff, take this witness into custody!", "stare")
                        ]
                    },
                    {
                        "text": "Kendall knew every detail of the offshore transfer and promised me immunity if I stayed quiet!",
                        "witness_pose": "worried",
                        "press": [
                            ("Tyrone", "Hold it! Back up that desperate accusation with a single fact, or withdraw it immediately!", "point"),
                            ("CFO", "He's the one who tried to cover up the audit trail!", "angry")
                        ],
                        "contradiction": "BOARD_MINUTES",
                        "ending_trigger": "SHIELD_CLIENT",
                        "win_dialogue": [
                            ("Tyrone", "Lies! Kendall is the ONLY executive who voted FOR an independent external audit—proving he had nothing to hide!", "point"),
                            ("CFO", "Gah...!!", "worried"),
                            ("Tyrone", "A co-conspirator doesn't demand independent forensic auditors to inspect the very books he is looting!", "point"),
                            ("Kendall", "Brilliant, Tyrone! You just dismantled every single accusation against me!", "smile"),
                            ("Dwyane", "Order! The witness's desperate attempt to implicate Mr. Kendall is thoroughly refuted!", "stare")
                        ]
                    }
                ]
            },
            "decision": {
                "prompt": "The CFO's embezzlement is exposed—but your evidence also shows both Kendall and Elijah cut ethical corners to inflate EK Global's valuation. What is your closing argument?",
                "options": [
                    {
                        "label": "Call for full regulatory oversight and governance reform on BOTH founders alongside the CFO's indictment.",
                        "truth_delta": 3,
                        "shield_delta": 0,
                        "response": [
                            ("Tyrone", "The CFO is guilty of grand embezzlement—but both Kendall and Elijah must submit to independent governance reform to restore public trust.", "point"),
                            ("Dave", "...I didn't expect that from you, Tyrone. Putting EK Global's employees above a personal victory takes real integrity.", "smile"),
                            ("Kendall", "Tch... A harsh pill to swallow, Tyrone—but you're right. No more shortcuts.", "think")
                        ]
                    },
                    {
                        "label": "Pin 100% of the blame on the CFO and secure total, unconditional acquittal for Kendall.",
                        "truth_delta": 0,
                        "shield_delta": 3,
                        "response": [
                            ("Tyrone", "With the CFO's private Signal logs on record, my client stands completely exonerated of all wrongdoing.", "smile"),
                            ("Kendall", "Unmatched as always, Tyrone. EK Global is officially back in business—under my leadership.", "smile"),
                            ("Dave", "You got your spotless acquittal, Tyrone... even if Kendall walks away untouched by his own mistakes.", "think")
                        ]
                    }
                ]
            }
        }
    ]
}