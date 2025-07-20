Interpreting results FAQS
-------------------------

Where do assertions fail
^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** How do I see what is causing my assertion to fail?

**A:** If an assertion is failing, SBY will provide a counterexample trace.
Provided you are not using the ``append`` option, the final cycle in this trace
is the cycle in which the assertion does not hold.  Check out our `quickstart
guide <https://yosyshq.readthedocs.io/projects/sby/en/latest/quickstart.html>`_
for a worked example of examining and fixing a failing assertion.


Overconstraint due to assumptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Q:** Is it possible for assumptions to hide counterexamples even when they do not share
any logic with assertions?

**A:** Yes, if all counterexamples to the assertions also violate the assumptions they
would be hidden. This normally happens if the assumptions make it impossible for the design
to progress without violating them meaning assertions can vacuously pass even though they
can never be witnessed to hold. `Witness cover traces`_ can be used to try to guard against
this type of failure, but care should be taken when applying assumptions, preferring
assumptions on top-level I/O over internal signals. An extreme example of overconstraint
would be a design that fails the `PREUNSAT check`_.


PREUNSAT check
^^^^^^^^^^^^^^

**Q:** Can SBY detect when assumptions prevent any progress for the design?

**A:** The ``smtbmc`` engine is able to perform ``PREUNSAT`` checks for each
bound. These check that there is at least one trace of that length that obeys
all of the assumptions. Failure of the ``PREUNSAT`` check is clear evidence of
overconstraint, however there are many cases of overconstraint it is unable
to catch. For example, if the design is able to stall indefinitely in one state,
this allows arbitrary length traces so PREUNSAT will pass even if the design is
subsequently overconstrained.


Witness cover traces
^^^^^^^^^^^^^^^^^^^^

**Q:** How do I produce witness cover traces for a passing assertion?

**A:** Check out the `witness cover section
<https://yosyshq.readthedocs.io/projects/ap120/en/latest/#witness-cover>`_ of our
whitepaper, `Weak precondition cover and witness for SVA properties
<https://yosyshq.readthedocs.io/projects/ap120>`_.


Can liveness properties fail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
**Q:** Is it possible to have liveness property to fail? Or will it just get stuck in formal run 

**A:** We don't recommend using liveness properties - it's almost always better to replace with an
assertion of something happening within a certain timeframe.

The example our CTO gives is of a design that is stuck in a deadlock, but it has a 64 bit counter
and when that overflows, things start up again. Liveness will tell you "yup, this design will do
things eventually" but it really doesn't help you because that 64 bit counter is so large that your
design will basically never start again.
