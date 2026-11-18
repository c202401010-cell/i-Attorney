DAVE_STORY = {
    "attorney": "Dave",
    "client": "Elijah",
    "rival": "Tyrone",
    "title": "DAVE'S ROUTE: THE SHIELD OF TRUTH",
    "subtitle": "Defending Elijah • Rivalry vs. Tyrone",
    "evidence_db": {
        "SERVER_LOG": {
            "name": "Server Access Log (11:42 PM)",
            "desc": "Biometric entry log showing Kendall's executive badge unlocked the vault server room at 11:42 PM—two minutes before the Q3 audit logs vanished."
        },
        "MEMO_EMAIL": {
            "name": "Encrypted Board Memo",
            "desc": "Intercepted executive message from Kendall instructing the CFO to 'scrub the Q3 liabilities before Monday's investor call.'"
        },
        "WIRE_RECEIPT": {
            "name": "Offshore Wire Receipt ($2.4M)",
            "desc": "Bank trace proving $2.4M was wired from EK Global's R&D reserve to a Cayman shell company controlled solely by the CFO."
        },
        "WHISTLE_NOTE": {
            "name": "Deleted HR Complaint",
            "desc": "An internal compliance report filed by a junior accountant flagging phantom vendor payouts—stamped 'DISMISSED BY KENDALL'."
        },
        "SHIFT_ROSTER": {
            "name": "Night Security Roster",
            "desc": "Signed guard log confirming Elijah left the building at 7:15 PM for a public charity gala and never returned that night."
        },
        "PAYROLL_EXPORT": {
            "name": "Overtime & Bonus Ledger",
            "desc": "Shows unauthorized $180,000 'consulting bonuses' routed to shell accounts approved under the CFO's emergency override."
        },
        "DUAL_LEDGER": {
            "name": "Shadow Ledger USB Drive",
            "desc": "Contains two sets of books: a clean ledger signed by Elijah, and a hidden ledger signed by both Kendall and the CFO—plus notes showing Elijah ignored early metric warnings."
        }
    },
    "prologue": [
        ("Dave", "(Ten years ago, two best friends soldered their first server rack in a cramped garage. Tonight, EK Global Industries is tearing itself apart in open court.)", "think"),
        ("Elijah", "Look at my hands, Dave—I still review pull requests and debug kernel panics at three in the morning! Do I look like a man who skims R&D budgets into Cayman shell accounts?!", "think"),
        ("Elijah", "Three hundred engineers trust me with their livelihoods. Someone inside the C-suite spoofed my master override so they could pin a $2.4 million crater on the founder!", "think"),
        ("Dave", "Take a breath and keep your chin up, Elijah. You didn't retain a public-interest litigator to play polite—and I'm not letting anyone rewrite what you built.", "point"),
        ("Tyrone", "Spare us the garage-startup folklore, Dave. A courtroom is governed by chain-of-custody logs, and every cryptographic hash leads straight to your client's terminal.", "smile"),
        ("Dave", "Tyrone... So the rumors circulating through the bar association were true. Kendall really brought in the undefeated closer.", "think"),
        ("Tyrone", "I don't gamble on sympathies, Dave. Step aside before your sentimentality turns this preliminary hearing into a professional eulogy.", "smile"),
        ("Dave", "Not a chance, Tyrone! Put Kendall under oath and watch how fast those manicured spreadsheets start bleeding!", "point")
    ],
    "chapters": [
        {
            "title": "CASE 1: THE VANISHING AUDIT",
            "bg": "courtroom",
            "ethics_topic": "Corporate Data Integrity & Spoliation of Evidence",
            "brief_summary": (
                "Days before EK Global Industries' Series D closing, six months of Q3 financial records vanished from the company's secure servers. "
                "With CEO Elijah's master root credentials recorded on the system log, co-founder Kendall and attorney Tyrone point the finger at Elijah, "
                "while defense counsel Dave prepares to test Kendall's timeline on the witness stand."
            ),
            "acknowledgement": (
                "A decisive opening triumph for the defense! By pinpointing the exact timestamp discrepancy between Kendall's lobby departure and the server vault's "
                "biometric entry sensor, Dave shattered the prosecution's timeline in open court. Today's proceedings upheld the core principle of Corporate Data Integrity "
                "and Spoliation of Evidence—proving that executive status cannot shield a witness when digital access logs tell the true story."
            ),
            "evidence": ["SERVER_LOG", "SHIFT_ROSTER", "MEMO_EMAIL"],
            "intro": [
                ("Dwyane", "Court is now in session for the preliminary hearing of EK Global Industries. Leave your press statements on the courthouse steps and proceed.", "idle"),
                ("Tyrone", "With pleasure, Your Honor. Last Thursday at 11:44 PM, EK Global's Q3 audit partition was zeroed out using CEO Elijah's master root key.", "smile"),
                ("Tyrone", "Six months of liability records erased in four seconds—conveniently forty-eight hours before Series D due diligence.", "smile"),
                ("Dave", "Objection! That's a half-truth masquerading as a confession, Tyrone! My client was three miles across town delivering a charity keynote when those drives were formatted!", "point"),
                ("Kendall", "It genuinely hurts to testify against my co-founder, Dave—Elijah and I built that valuation from two folding tables. That's why I stayed late to lock down the server floor myself at 9:00 PM.", "smile"),
                ("Kendall", "I badged out at the lobby turnstile, stepped into my town car, and went straight home. Nobody else held root clearance except Elijah.", "smile"),
                ("Elijah", "How do you sleep at night telling a bold-faced lie like that, Kendall?! I was the one begging for an independent audit!", "think"),
                ("Dwyane", "I have zero patience for founders' therapy, gentlemen. Mr. Dave, cross-examine the witness!", "sigh"),
                ("Dave", "(Kendall is staking his entire credibility on leaving the tower at 9:00 PM sharp... Let's see what the vault's biometric sensor recorded.)", "think")
            ],
            "cross_exam": {
                "witness": "Kendall",
                "default_pose": "smile",
                "statements": [
                    {
                        "text": "I locked the server floor at 9:00 PM sharp, badged out at the lobby, and never returned that night.",
                        "witness_pose": "smile",
                        "press": [
                            ("Dave", "Hold it! You're willing to swear under penalty of perjury that your boots didn't touch that server floor after 9:00 PM?", "point"),
                            ("Kendall", "Subpoena my chauffeur's dashcam, pull the lobby turnstile feed—I was asleep before ten, Dave!", "smile"),
                            ("Tyrone", "Bluffing without hard logs is an amateur tell, Dave. Move on if you lack admissible exhibits.", "smile"),
                            ("Dave", "(He's way too confident about that lobby turnstile... Which means he used a biometric side door!)", "think")
                        ],
                        "contradiction": "SERVER_LOG",
                        "win_dialogue": [
                            ("Dave", "Then explain why your biometric thumbprint unlocked the vault server room at 11:42 PM—just TWO MINUTES before the Q3 audit vanished into thin air!", "point"),
                            ("Kendall", "W-What?! N-No, that's impossible—! The edge cache was configured to purge automatically at midnight—!", "think"),
                            ("Dave", "Look at the biometric hash, Kendall! A lobby turnstile only logs badge exits—it doesn't stop an executive from slipping up the freight elevator to the vault!", "point"),
                            ("Elijah", "11:42 PM?! You went back into that server vault yourself, Kendall—while I was standing on stage at the charity gala?!", "point"),
                            ("Kendall", "I—I only stepped inside to verify the cooling racks! You can't prove I touched a single partition!", "think"),
                            ("Dave", "Four seconds after your thumbprint cleared the vault door, six months of corporate liabilities were wiped off the planet! Your 9:00 PM alibi is dead!", "point"),
                            ("Tyrone", "Tch...! You held the mainframe mirror log in reserve until he locked himself into the 9:00 PM timestamp. Well calculated, Dave.", "think"),
                            ("Dwyane", "Order in the gallery! Silence! The witness's alibi has completely collapsed under the weight of biometric proof. The Server Access Log is entered into the record!", "stare")
                        ]
                    },
                    {
                        "text": "Only founding partners hold emergency root credentials capable of wiping financial partitions.",
                        "witness_pose": "idle",
                        "press": [
                            ("Dave", "Hold it! Doesn't the Chief Financial Officer receive temporary root privileges during quarterly close?", "point"),
                            ("Kendall", "For a forty-eight-hour tax window, yes. But our CFO treats compliance like scripture—he wouldn't breathe near an audit partition.", "think"),
                            ("Dave", "(Interesting... He's rushing to vouch for the CFO before anyone even asked.)", "think")
                        ]
                    },
                    {
                        "text": "Elijah was terrified our Series D lead syndicate would pull their term sheet if they saw the Q3 cash burn.",
                        "witness_pose": "smile",
                        "press": [
                            ("Dave", "Hold it! Funny—because YOU were the co-founder hosting the Series D syndicate breakfast on Monday morning, Kendall!", "point"),
                            ("Tyrone", "Objection! Reciting a client's social calendar does not establish criminal intent, Your Honor.", "point"),
                            ("Dwyane", "Sustained. Keep your questions tethered to the exhibits, Mr. Dave.", "sigh")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 2: PHANTOM VENDORS",
            "bg": "courtroom",
            "ethics_topic": "Whistleblower Protection & Internal Controls",
            "brief_summary": (
                "With Kendall's alibi discredited, attention shifts to $2.4 million missing from EK Global's research reserves. "
                "The Chief Financial Officer takes the stand claiming every external contractor payout passed internal review without objection, "
                "prompting Dave to examine whether compliance warnings inside the finance department were silenced."
            ),
            "acknowledgement": (
                "An extraordinary courtroom breakthrough! By recovering the suppressed HR compliance ticket from the deleted database, Dave exposed how internal "
                "fraud alerts were buried to keep investors in the dark. Today's proceedings reinforced the vital standard of Whistleblower Protection and "
                "Internal Controls—confirming that ethical governance depends on safeguarding employees who report financial irregularities."
            ),
            "evidence": ["SERVER_LOG", "WHISTLE_NOTE", "PAYROLL_EXPORT"],
            "intro": [
                ("Dwyane", "Court reconvenes. Mr. Kendall's alibi is in tatters, yet $2.4 million in R&D capital remains unaccounted for. Proceed.", "idle"),
                ("Tyrone", "A late-night server check does not equal grand larceny, Dave. Our Chief Financial Officer is prepared to testify under oath on who ordered those disbursements.", "smile"),
                ("CFO", "Your Honor, I've balanced corporate treasuries for twenty-two years without a single blemish. I only bypassed dual-signature controls because Mr. Elijah demanded immediate liquidity for 'stealth R&D contractors.'", "idle"),
                ("Dave", "Twenty-two years in corporate finance—and you wired $2.4 million on a hallway whisper without a single purchase order or tax ID?", "point"),
                ("CFO", "When a founder threatens to replace anyone who 'throttles product velocity,' you execute the wire and paper the compliance file afterward!", "angry"),
                ("Elijah", "I never once told you to bypass dual signatures! You told me those vendor retainers were already cleared by legal!", "think"),
                ("Dave", "(He's painting Elijah as a reckless tyrant... Wait—didn't a junior member of his own accounting team file a formal compliance warning weeks ago?!)", "think")
            ],
            "cross_exam": {
                "witness": "CFO",
                "default_pose": "laugh",
                "statements": [
                    {
                        "text": "Every contractor invoice cleared internal compliance without a single red flag or staff objection.",
                        "witness_pose": "laugh",
                        "press": [
                            ("Dave", "Hold it! Not one junior analyst, not one internal auditor, questioned two million dollars in shell invoices?", "point"),
                            ("CFO", "Our compliance ticketing system flags anomalies automatically, Counselor. The audit queue was spotless.", "laugh"),
                            ("Tyrone", "Zero open tickets on the compliance portal, Dave. You're swinging at shadows.", "smile"),
                            ("Dave", "(Zero open tickets—because someone with admin rights purged the complaint before the audit!)", "think")
                        ],
                        "contradiction": "WHISTLE_NOTE",
                        "win_dialogue": [
                            ("Dave", "Spotless?! The audit queue was only empty because someone purged THIS internal HR compliance report from the server!", "point"),
                            ("Dave", "Three weeks ago, a junior accountant flagged those exact phantom shell vendors—and look at the administrative override stamped across the bottom: 'DISMISSED BY KENDALL'!", "point"),
                            ("CFO", "Gah—!! Th-That ticket was wiped from the HR database! How could you possibly pull a deleted compliance log?!", "worried"),
                            ("Dave", "Because automated off-site backups don't care about executive override codes! You claimed not a single staff member objected—when your own clerk blew the whistle!", "point"),
                            ("Tyrone", "...Kendall. You assured me those compliance flags were harmless sandbox tests from IT.", "think"),
                            ("Kendall", "Keep your voice down, Tyrone—an open fraud investigation would have frozen our Series D escrow!", "think"),
                            ("Dwyane", "Order! Suppressing an internal whistleblower alert to conceal irregular payouts is a grave breach of corporate governance! Explain yourselves!", "stare")
                        ]
                    },
                    {
                        "text": "Those disbursements funded specialized offshore GPU clusters essential to our AI training pipeline.",
                        "witness_pose": "idle",
                        "press": [
                            ("Dave", "Hold it! Strange how those 'offshore GPU clusters' share a billing address with a vacant PO box in Georgetown!", "point"),
                            ("CFO", "Stealth infrastructure vendors routinely use registered mail drops to shield proprietary hardware maps, Counselor.", "angry")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 3: THE SILENCED CLERK",
            "bg": "courtroom",
            "ethics_topic": "Workplace Retaliation & Duty to Report Fraud",
            "brief_summary": (
                "Following the revelation of the deleted compliance report, the junior accounting clerk who originally raised the alarm takes the witness stand. "
                "Though management insists his departure was part of a routine hiring freeze, Dave seeks to corroborate the clerk's account of irregular payroll "
                "disbursements before his credentials were revoked."
            ),
            "acknowledgement": (
                "A resounding victory for workplace integrity! By backing the whistleblower's testimony with his preserved payroll backup, Dave proved that "
                "executive emergency overrides were used to siphon company reserves while silencing honest staff. Today's proceedings honored the principles of "
                "Workplace Retaliation Protection and the Duty to Report Fraud—demonstrating that courage and careful recordkeeping can overcome institutional intimidation."
            ),
            "evidence": ["WHISTLE_NOTE", "PAYROLL_EXPORT", "WIRE_RECEIPT"],
            "intro": [
                ("Dave", "To show this bench how aggressively the truth was suppressed, the defense calls the junior clerk who filed that deleted HR warning!", "point"),
                ("Tyrone", "Objection! Calling a former clerk terminated during routine restructuring invites textbook workplace grudge testimony.", "smile"),
                ("Dave", "He wasn't restructured, Tyrone—he was marched out by building security forty-eight hours after refusing to reconcile fake payroll bonuses!", "point"),
                ("Dwyane", "Overruled. Let's hear what the clerk actually uncovered before his badge was revoked.", "idle"),
                ("Employee", "I... I double-checked every ledger line three times before I ever submitted that HR ticket. I didn't want to believe people at the top were stealing from our own team.", "worried"),
                ("CFO", "Absurd! An entry-level accounts clerk doesn't even hold read-permissions for executive payroll reserves!", "angry"),
                ("Dave", "(He kept a backup export before HR locked his terminal. Let's back up his testimony with the Overtime & Bonus Ledger!)", "think")
            ],
            "cross_exam": {
                "witness": "Employee",
                "default_pose": "worried",
                "statements": [
                    {
                        "text": "Every Friday afternoon, six-figure 'consulting bonuses' vanished from the payroll reserve under an emergency override!",
                        "witness_pose": "worried",
                        "press": [
                            ("Dave", "Hold it! Did those Friday bonus transfers carry Elijah's CEO approval signature?", "point"),
                            ("Employee", "No! They bypassed CEO sign-off completely—someone pushed them through with an executive finance override! Check the Overtime & Bonus Ledger!", "shocked")
                        ],
                        "contradiction": "PAYROLL_EXPORT",
                        "win_dialogue": [
                            ("Dave", "Look right here in the Overtime & Bonus Ledger! $180,000 in phantom 'consulting bonuses'—every single transfer stamped with the CFO's personal override ID!", "point"),
                            ("CFO", "Th-That's impossible!! Raw payroll override logs are restricted exclusively to senior administrators!", "worried"),
                            ("Employee", "I exported a timestamped backup CSV to my local drive ten minutes before HR killed my credentials—because I knew nobody would believe me without proof!", "relief"),
                            ("Dave", "Every Friday at 4:55 PM, while the engineering floor was wrapping up sprints, the CFO drained the payroll reserve into shell accounts!", "point"),
                            ("Tyrone", "So the CFO was skimming directly from payroll reserves behind Kendall's back as well...", "think"),
                            ("Dwyane", "Order! The ledger speaks for itself! Those unauthorized bonus transfers lead straight to the CFO's terminal!", "stare")
                        ],
                        "unlocks": {
                            "text": "I saved the Overtime & Bonus Ledger before they locked me out—it proves the CFO's override ID authorized every shell bonus!",
                            "witness_pose": "smile",
                            "press": [
                                ("Dave", "Hold it! That backup ledger is sitting right in our Court Record! Let's present it to the bench!", "point"),
                                ("Employee", "Yes! Open the Court Record and present the Overtime & Bonus Ledger!", "smile")
                            ],
                            "contradiction": "PAYROLL_EXPORT",
                            "win_dialogue": [
                                ("Dave", "Look right here in the Overtime & Bonus Ledger! $180,000 in phantom 'consulting bonuses'—every single transfer stamped with the CFO's personal override ID!", "point"),
                                ("CFO", "Th-That's impossible!! Raw payroll override logs are restricted exclusively to senior administrators!", "worried"),
                                ("Employee", "I exported a timestamped backup CSV to my local drive ten minutes before HR killed my credentials—because I knew nobody would believe me without proof!", "relief"),
                                ("Dave", "Every Friday at 4:55 PM, while the engineering floor was wrapping up sprints, the CFO drained the payroll reserve into shell accounts!", "point"),
                                ("Tyrone", "So the CFO was skimming directly from payroll reserves behind Kendall's back as well...", "think"),
                                ("Dwyane", "Order! The ledger speaks for itself! Those unauthorized bonus transfers lead straight to the CFO's terminal!", "stare")
                            ]
                        }
                    },
                    {
                        "text": "When HR deactivated my badge, they claimed my role was eliminated due to a company-wide hiring freeze.",
                        "witness_pose": "worried",
                        "press": [
                            ("Dave", "A classic retaliatory firing disguised as budget cuts. Let's prove his discovery with the Overtime & Bonus Ledger!", "point"),
                            ("Employee", "Please show the judge the Overtime & Bonus Ledger so everyone sees why they really fired me!", "worried")
                        ],
                        "contradiction": "PAYROLL_EXPORT",
                        "win_dialogue": [
                            ("Dave", "They didn't eliminate his position for budget cuts—they marched him out to bury THIS Overtime & Bonus Ledger!", "point"),
                            ("Dave", "$180,000 in fraudulent consulting payouts, all authorized under the CFO's private emergency override key!", "point"),
                            ("CFO", "Gah—!! You had no right to retain internal accounting exports after termination!", "angry"),
                            ("Employee", "Thank you for putting the real numbers on the record, Counselor!", "relief"),
                            ("Tyrone", "Threatening a whistleblower for preserving evidence isn't helping your defense, CFO.", "think"),
                            ("Dwyane", "Admitted! The retaliatory motive behind this termination is crystal clear!", "stare")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 4: THE CAYMAN TRAIL",
            "bg": "courtroom",
            "ethics_topic": "Anti-Money Laundering & Executive Self-Dealing",
            "brief_summary": (
                "Cornered by domestic payroll discrepancies, the CFO insists that no company funds ever left the country under his watch "
                "and attempts to shift responsibility for international wires back onto Elijah. Dave prepares to follow the cross-border banking trail "
                "to uncover where EK Global's missing $2.4 million truly landed."
            ),
            "acknowledgement": (
                "A landmark victory in financial forensics! By tracing the $2.4 million SWIFT transfer from EK Global's research reserve directly into an "
                "offshore shell entity, Dave dismantled the CFO's final line of denial. Today's proceedings upheld the standards of Anti-Money Laundering "
                "and Executive Self-Dealing accountability—proving that shell companies cannot hide stolen corporate assets from rigorous audit trails."
            ),
            "evidence": ["PAYROLL_EXPORT", "WIRE_RECEIPT", "MEMO_EMAIL"],
            "intro": [
                ("Dwyane", "The CFO's financial excuses are collapsing under their own weight. Mr. Tyrone, does your client still stand behind this officer?", "sigh"),
                ("Tyrone", "My client stands behind due process, Your Honor. If the CFO diverted payroll funds, he operated as a rogue embezzler—without Kendall's authorization.", "smile"),
                ("Kendall", "It makes me sick! I trusted him to safeguard our treasury, and he was looting Elijah and me the entire quarter!", "smile"),
                ("Dave", "Objection! Save the sudden moral outrage, Kendall—especially when YOU deleted the clerk's warning!", "point"),
                ("CFO", "Y-You're throwing me overboard, Kendall?! After I scrubbed the Q3 liabilities so your Series D valuation wouldn't crater?!", "angry"),
                ("Tyrone", "Silence on the stand! Answer only the questions put to you by counsel!", "point"),
                ("Dave", "(The CFO just admitted why the books were scrubbed! Now let's trace the $2.4 million offshore wire straight to his Cayman shell!)", "think")
            ],
            "cross_exam": {
                "witness": "CFO",
                "default_pose": "angry",
                "statements": [
                    {
                        "text": "Not a single cent ever left domestic corporate accounts—Elijah controlled every international wire!",
                        "witness_pose": "angry",
                        "press": [
                            ("Dave", "Hold it! Still pointing at Elijah when the offshore shell company was incorporated under your own nominee director?!", "point"),
                            ("CFO", "Offshore banking registries are sealed, Counselor! You're bluffing without a federal subpoena!", "laugh"),
                            ("Tyrone", "Without authenticated wire routing records, that accusation has zero standing, Dave.", "smile")
                        ],
                        "contradiction": "WIRE_RECEIPT",
                        "win_dialogue": [
                            ("Dave", "Bluffing?! International wire compliance flagged THIS $2.4 million SWIFT transfer routed straight from EK Global's R&D reserve into your Cayman shell account!", "point"),
                            ("CFO", "N-NO!! H-How did you pull a SWIFT trace on a numbered Cayman depository?!", "worried"),
                            ("Elijah", "$2.4 million... That was our entire next-generation hardware budget!", "point"),
                            ("Dave", "Look at the beneficiary signature and routing timestamp—not a single cent went to domestic servers! You wired the entire R&D reserve straight to your own offshore shell!", "point"),
                            ("CFO", "I... I never meant for it to go this far—the Series D valuation was supposed to cover the hole before anyone noticed!", "worried"),
                            ("Dwyane", "Order! The Offshore Wire Receipt is admitted into evidence! Bailiff, secure the courtroom doors and keep a close eye on the witness!", "stare")
                        ]
                    },
                    {
                        "text": "Kendall never asked me to alter quarterly figures—he left all accounting policy to my discretion.",
                        "witness_pose": "worried",
                        "press": [
                            ("Dave", "Hold it! Left everything to your discretion? Then why was he unlocking the server vault at 11:42 PM?", "point"),
                            ("CFO", "I... I don't monitor Mr. Kendall's late-night schedule!", "worried")
                        ]
                    }
                ]
            }
        },
        {
            "title": "CASE 5: THE SHADOW LEDGER",
            "bg": "courtroom",
            "ethics_topic": "Fiduciary Duty vs. Blind Client Loyalty",
            "brief_summary": (
                "In the final session of the EK Global trial, the CFO's embezzlement stands exposed, yet deeper questions remain about executive "
                "complicity and governance failures at the top. Armed with recovered communications and a dual-ledger drive, Dave must confront the "
                "ultimate test of legal ethics and fiduciary truth."
            ),
            "acknowledgement": (
                "A historic culmination to the EK Global trial! In the final hour of cross-examination, Dave pierced the executive veil to establish "
                "the complete chain of accountability in open court. Today's proceedings honored the highest ideal of Fiduciary Duty vs. Blind Client Loyalty—"
                "proving that true advocacy serves justice, transparency, and the hundreds of people who rely on honest leadership."
            ),
            "evidence": ["MEMO_EMAIL", "WIRE_RECEIPT", "DUAL_LEDGER"],
            "intro": [
                ("Dwyane", "We reach the final hour of the EK Global trial. Both counsel will present their decisive closing proof.", "idle"),
                ("Tyrone", "Your Honor, the CFO's theft is beyond dispute. Yet one stubborn legal fact remains: CEO Elijah signed the public SEC filings.", "point"),
                ("Tyrone", "Signing off on inflated quarterly numbers without verifying them is textbook fiduciary negligence!", "point"),
                ("Dave", "He signed those filings because Kendall and the CFO fed him a sanitized ledger while hiding the real books!", "point"),
                ("Elijah", "(Dave... wait. Before you hand that Shadow Ledger USB to the clerk, look at the appendix folder on the drive...)", "think"),
                ("Dave", "(What is this...? Internal Slack exports showing Elijah knew active user metrics were padded with free-trial bots last quarter?!)", "think"),
                ("Elijah", "(If you submit the whole drive, Kendall and the CFO go down—but the SEC will nail me for signing off on inflated user growth too...)", "think"),
                ("Dave", "(This is the hardest call of my career. Do I expose the entire unvarnished truth—or protect my client by holding back the appendix?)", "think")
            ],
            "cross_exam": {
                "witness": "Kendall",
                "default_pose": "smile",
                "statements": [
                    {
                        "text": "I never instructed anyone to falsify EK Global's liabilities—the CFO cooked the books entirely on his own!",
                        "witness_pose": "smile",
                        "press": [
                            ("Dave", "Hold it! You expect this court to believe a veteran CFO risked federal prison without a direct order from a founder?", "point"),
                            ("Kendall", "Produce one email, one text, one memo where I told him to alter a single figure, Dave! You can't!", "smile"),
                            ("Tyrone", "Put your proof on the bench, Dave, or withdraw the charge against my client.", "point")
                        ],
                        "contradiction": "MEMO_EMAIL",
                        "ending_trigger": "FULL_TRUTH",
                        "win_dialogue": [
                            ("Dave", "Read your own words aloud to this entire courtroom, Kendall! 'Scrub the Q3 liabilities before Monday's investor call'!", "point"),
                            ("Kendall", "N-No... NO!! That executive relay used ephemeral encryption—how did you decrypt it?!", "think"),
                            ("Dave", "Every encrypted relay leaves a recovery key on the compliance server you forgot to wipe at 11:42 PM! You didn't just look the other way—you gave the order!", "point"),
                            ("Elijah", "You told me our numbers were clean, Kendall! You ordered the books cooked behind my back!", "point"),
                            ("Tyrone", "...Checkmate. Even I cannot argue around a direct written order to falsify corporate liabilities, Kendall.", "think"),
                            ("Dave", "This wasn't one rogue CFO, Your Honor—it was a boardroom conspiracy to deceive investors and frame an innocent founder!", "point"),
                            ("Dwyane", "Order in the gallery! The Encrypted Board Memo is entered into the permanent record! The truth of this conspiracy is finally laid bare!", "stare")
                        ]
                    },
                    {
                        "text": "The $2.4 million Cayman theft proves Elijah's careless oversight let the CFO rob our treasury!",
                        "witness_pose": "point",
                        "press": [
                            ("Dave", "Hold it! Trying to blame Elijah for a wire transfer the CFO hid behind encrypted channels?!", "point"),
                            ("Kendall", "The CEO's name is on the charter! Acquit me and let Elijah answer for the missing funds!", "smile")
                        ],
                        "contradiction": "WIRE_RECEIPT",
                        "ending_trigger": "SHIELD_CLIENT",
                        "win_dialogue": [
                            ("Dave", "This wire receipt proves the CFO bypassed every executive sign-off using his private root key—clearing Elijah of every single cent!", "point"),
                            ("CFO", "I... Kendall promised me a severance shield if I took the heat alone!", "worried"),
                            ("Dave", "Not a single authorization token came from Elijah's terminal! The financial trail begins and ends with the CFO!", "point"),
                            ("Elijah", "You did it, Dave! You cleared my name and proved I never touched a dollar of that reserve!", "smile"),
                            ("Dwyane", "Order! The Offshore Wire Receipt conclusively absolves Mr. Elijah of the embezzlement transfers!", "stare")
                        ]
                    }
                ]
            },
            "decision": {
                "prompt": "The Shadow Ledger USB proves Kendall and the CFO orchestrated the fraud—but also reveals Elijah signed off on padded user growth metrics. How will you present it?",
                "options": [
                    {
                        "label": "Submit the FULL unedited ledger—uphold total transparency even if Elijah faces regulatory penalties.",
                        "truth_delta": 3,
                        "shield_delta": 0,
                        "response": [
                            ("Dave", "Your Honor, I am submitting the complete, unredacted Shadow Ledger. Justice doesn't edit the record to spare anyone!", "point"),
                            ("Elijah", "...You're right, Dave. If I want EK Global to stand for integrity again, I have to own my shortcuts too.", "think"),
                            ("Tyrone", "Hmph... Respect, Dave. Very few defense attorneys have the backbone to put truth ahead of a spotless win.", "smile")
                        ]
                    },
                    {
                        "label": "Present ONLY the pages implicating the CFO and Kendall—protect Elijah from any liability.",
                        "truth_delta": 0,
                        "shield_delta": 3,
                        "response": [
                            ("Dave", "These verified ledger extracts prove beyond a shadow of a doubt that Elijah was kept completely in the dark!", "point"),
                            ("Elijah", "Thank you, Dave! You saved my company, my name, and everything we built!", "smile"),
                            ("Tyrone", "Surgical editing, Dave... You won the verdict, even if you left half the truth locked in your briefcase.", "think")
                        ]
                    }
                ]
            }
        }
    ]
}