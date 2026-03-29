login-use-cases.md

I think... A stored tuple means "logged in".  Evaluate that critically.  Session storage is
for an endpoint, like https://festschedule.org.

(Feature creep, consider)
Words should not have one or two letter differences to other words.  Words should allow
1 letter misspellings (berthe vs bertha) but correct the user when the incorrect ones are used.  Word order (there ARE? three distinct word pools) should matter by sorting the triple -- funky berthe gazebo SAME AS berthe-funky-gazebo SAME as funky bertha gazebe.  Dashes don't matter whitespace ok instead.  Capitalization doesn't matter.

1. Arrive at festschedule.org/fqf2026 -- no stored triple
   Buttons:
   "Load schedule" italics "Load existing schedule if you have one".
         Text [grey "use your secret words"]
   "New Schedule"

2. Arrive at festschedule.org/fqf2026?share=xxxxx -- no stored triple
   Buttons:
   "Load schedule" italics "Load your existing schedule"
            Text [grey "use your secret words"]
   "New Schedule" italics "Create a schedule to allow comparing with <name>"
   "View <name's> schedule?" italics - "view only, no changes can be made"

   "View only goes to URL festschedule.org/fqf2026/xxxxxxx" (the hash key of the other user)
   The share tab is NOT shown, the all, My Schedule and Map are using the other user data

3. Arrive at festschedule.org/fqf2026?share=invalid -- no stored triple, no share exists
   Message, dark orange italic at bottom "(!) Share not found"
   Buttons: same as 1
   "Load schedule" italics "Load existing schedule if you have one".
         Text [grey "use your secret words"]
   "New Schedule"

4. Arrive at festschedule.org/fqf2026  stored tuple and counter
  Existing user wants to look at existing schedule.
  Buttons:
   "Load schedule" italics "Load existing schedule, or enter new one".
         Text [black, filled in "existing secret triple"]
   "New Schedule"
   Login presented, with triple and Name filled in.  Still have to say load
   New creates a new "signature" + counter (eg. 1)

5. Arrive at festschedule.org/fqf2026?share=xxxxxx -- stored triple, share exists
   This case, just skips the loginload pane completely.
   Add the "share" to shares, go to share tab
   Note, the URL is

6. Same as 4.
   Message, dark orange italic at bottom "(!) Share not found"
